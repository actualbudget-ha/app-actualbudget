#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "app-actualbudget"
IMAGE_NAME = "app-actualbudget:smoke-test"
DEFAULT_CONTAINER = "app-actualbudget-smoke-default"
OPTIONS_CONTAINER = "app-actualbudget-smoke-options"
INGRESS_COMPAT_CONTAINER = "app-actualbudget-smoke-ingress-compat"


def run_cmd(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    printable = " ".join(args)
    print(f"+ {printable}")
    return subprocess.run(
        list(args),
        check=check,
        text=True,
        capture_output=True,
    )


def docker_rm(container: str) -> None:
    run_cmd("docker", "rm", "-f", container, check=False)


def cleanup_temp_dir(path: Path) -> None:
    try:
        shutil.rmtree(path)
        return
    except OSError as err:
        print(
            f"Warning: initial temp dir cleanup failed for {path}: {err}",
            file=sys.stderr,
        )

    # In CI, Docker may create root-owned files in bind mounts. Try fixing
    # permissions in-container, then retry cleanup.
    run_cmd(
        "docker",
        "run",
        "--rm",
        "-v",
        f"{path}:/data",
        "alpine:3.22",
        "sh",
        "-c",
        "chmod -R a+rwx /data || true",
        check=False,
    )

    try:
        shutil.rmtree(path)
    except OSError as err:
        print(
            f"Warning: final temp dir cleanup failed for {path}: {err}",
            file=sys.stderr,
        )


def wait_http(url: str, timeout_seconds: int = 90) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                if 200 <= response.status < 500:
                    return True
        except Exception:
            time.sleep(1)
    return False


def wait_internal_http(container: str, port: int, timeout_seconds: int = 90) -> bool:
    deadline = time.time() + timeout_seconds
    check_script = (
        "const http=require('http');"
        "const req=http.get('http://127.0.0.1:' + process.argv[1],res=>{"
        "process.exit((res.statusCode>=200 && res.statusCode<500)?0:1);"
        "});"
        "req.on('error',()=>process.exit(1));"
        "setTimeout(()=>process.exit(1),3000);"
    )

    while time.time() < deadline:
        result = run_cmd(
            "docker",
            "exec",
            container,
            "node",
            "-e",
            check_script,
            str(port),
            check=False,
        )
        if result.returncode == 0:
            return True
        time.sleep(1)
    return False


def get_logs(container: str, lines: int = 30) -> str:
    result = run_cmd("docker", "logs", "--tail", str(lines), container, check=False)
    return (result.stdout + result.stderr).strip()


def ensure_docker_available() -> None:
    if shutil.which("docker") is None:
        raise RuntimeError("docker CLI is not installed or not available on PATH")
    result = run_cmd("docker", "info", check=False)
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"Docker daemon is not available:\n{message}")


def build_image() -> None:
    run_cmd(
        "docker",
        "build",
        "--pull",
        "-t",
        IMAGE_NAME,
        "-f",
        str(APP_DIR / "Dockerfile"),
        str(APP_DIR),
    )


def run_default_test(timeout_seconds: int) -> None:
    docker_rm(DEFAULT_CONTAINER)
    run_cmd(
        "docker",
        "run",
        "-d",
        "--name",
        DEFAULT_CONTAINER,
        "-p",
        "15006:5006",
        IMAGE_NAME,
    )
    try:
        if not wait_http("http://127.0.0.1:15006", timeout_seconds=timeout_seconds):
            raise RuntimeError(
                "Default startup test failed: server did not respond on port 5006.\n"
                f"Container logs:\n{get_logs(DEFAULT_CONTAINER)}"
            )
    finally:
        docker_rm(DEFAULT_CONTAINER)


def run_options_test(timeout_seconds: int) -> None:
    docker_rm(OPTIONS_CONTAINER)
    tmp_dir = Path(tempfile.mkdtemp(prefix="app-actualbudget-smoke-"))
    try:
        options_path = tmp_dir / "options.json"
        options_path.write_text(
            json.dumps(
                {
                    "port": 5011,
                    "hostname": "0.0.0.0",
                    "upload_file_sync_size_limit_mb": 21,
                    "upload_sync_encrypted_file_sync_size_limit_mb": 51,
                    "upload_file_size_limit_mb": 22,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        run_cmd(
            "docker",
            "run",
            "-d",
            "--name",
            OPTIONS_CONTAINER,
            "-p",
            "15011:5011",
            "-v",
            f"{tmp_dir}:/data",
            IMAGE_NAME,
        )
        try:
            if not wait_http("http://127.0.0.1:15011", timeout_seconds=timeout_seconds):
                raise RuntimeError(
                    "Options startup test failed: server did not respond on mapped port 5011.\n"
                    f"Container logs:\n{get_logs(OPTIONS_CONTAINER)}"
                )

            logs = get_logs(OPTIONS_CONTAINER)
            if "Listening on 0.0.0.0:5011" not in logs:
                raise RuntimeError(
                    "Options startup test failed: expected overridden bind/port log line missing.\n"
                    f"Container logs:\n{logs}"
                )
        finally:
            docker_rm(OPTIONS_CONTAINER)
    finally:
        cleanup_temp_dir(tmp_dir)


def run_ingress_compat_test(timeout_seconds: int) -> None:
    docker_rm(INGRESS_COMPAT_CONTAINER)
    run_cmd(
        "docker",
        "run",
        "-d",
        "--name",
        INGRESS_COMPAT_CONTAINER,
        IMAGE_NAME,
    )
    try:
        if not wait_internal_http(
            INGRESS_COMPAT_CONTAINER, 5006, timeout_seconds=timeout_seconds
        ):
            raise RuntimeError(
                "Ingress compatibility test failed: service not reachable on container internal port 5006.\n"
                f"Container logs:\n{get_logs(INGRESS_COMPAT_CONTAINER)}"
            )
    finally:
        docker_rm(INGRESS_COMPAT_CONTAINER)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and smoke-test the app-actualbudget add-on image."
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=90,
        help="HTTP wait timeout for each container test.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        ensure_docker_available()
        build_image()
        run_default_test(timeout_seconds=args.timeout_seconds)
        run_options_test(timeout_seconds=args.timeout_seconds)
        run_ingress_compat_test(timeout_seconds=args.timeout_seconds)
    except Exception as err:  # noqa: BLE001 - CLI wrapper
        print(f"Smoke test FAILED: {err}", file=sys.stderr)
        return 1

    print("Smoke test PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
