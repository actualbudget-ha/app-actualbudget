<!-- https://developers.home-assistant.io/docs/apps/presentation#keeping-a-changelog -->
# Changelog

## 0.1.9

- Bump upstream Actual Budget server image from `26.8.0` to `26.8.1`.

## 0.1.8

- Bump upstream Actual Budget server image from `26.7.0` to `26.8.0`.

## 0.1.7

- Bump upstream Actual Budget server image from `26.4.0` to `26.7.0`.

## 0.1.6

- Remove `logo.png` so the Home Assistant add-on page no longer shows a large logo header image.
- Reject reserved `extra_env_vars` names that would override app-managed network, TLS, upload limit, storage, or process runtime settings.

## 0.1.5

- Replace template `icon.png` and `logo.png` assets with Actual Budget branding assets.
- Update user-facing add-on naming from slug-style text to `Actual Budget`.
- Replace repository maintainer placeholder metadata.

## 0.1.4

- Bump upstream Actual Budget server image from `26.3.0` to `26.4.0`.

## 0.1.3

- Fix AppArmor policy for Node native modules by allowing memory mapping of `/app/**/*.node` files.

## 0.1.2

- Add a custom AppArmor profile (`apparmor.txt`) to improve add-on security posture.

## 0.1.1

- Disable Home Assistant Ingress by default and document direct port access as the supported mode.
- Change default hostname binding from `::` to `0.0.0.0` for common Home Assistant setups.
- Improve maintainer workflows with `workflow_dispatch` support and optional manual publish control.

## 0.1.0

- Initial Actual Budget Home Assistant app release (in development).
- Uses the official `actualbudget/actual-server` Docker image.
- Adds configurable server options for port, hostname, upload limits, and HTTPS cert/key.
- Adds Home Assistant native runtime lifecycle (s6-overlay + bashio + cont-init validation).
- Adds ingress support while keeping direct port access.
- Adds production metadata (`image`, `stage`) and build metadata (`build.yaml`).
- Adds configurable `log_level` and validated `extra_env_vars` passthrough options.
- Expands CI quality gates with hadolint, shellcheck, and version consistency checks.
