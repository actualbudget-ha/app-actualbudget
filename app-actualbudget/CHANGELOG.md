<!-- https://developers.home-assistant.io/docs/apps/presentation#keeping-a-changelog -->
# Changelog

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
