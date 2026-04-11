# Home Assistant App Repository: app-actualbudget

Apps (formerly known as add-ons) for Home Assistant allow you to extend your
Home Assistant installation with additional services.

This repository provides an app for running the official Actual Budget server.

[![Home Assistant - A project from the Open Home Foundation](https://www.openhomefoundation.org/badges/home-assistant.png)](https://www.openhomefoundation.org/)

## Apps provided by this repository

- **[Actual Budget](./app-actualbudget/README.md)**

  Self-hosted Actual Budget server for Home Assistant.

## Install from this repository

1. In Home Assistant, go to **Settings** > **Apps** > **Repositories**.
2. Add this repository URL.
3. Find **app-actualbudget** in the app store and install it.

## Validation

For manual Home Assistant validation steps, see the add-on docs:
[app-actualbudget/DOCS.md](./app-actualbudget/DOCS.md).

## Local development and QA

This repository uses `uv` for local tooling.

```bash
uv sync --group dev
uv run yamllint repository.yaml app-actualbudget/config.yaml app-actualbudget/build.yaml app-actualbudget/translations/en.yaml .github/workflows/*.yaml .github/dependabot.yaml .hadolint.yaml
uv run python scripts/smoke_test.py
```

## Publishing checklist

1. Update `app-actualbudget/config.yaml`:
   - `image` to your GHCR namespace.
   - `url` to this repository.
2. Keep `version` in `app-actualbudget/config.yaml` and `app-actualbudget/CHANGELOG.md` aligned.
3. Keep `app-actualbudget/build.yaml` and `app-actualbudget/Dockerfile` aligned with tested upstream Actual server and runtime bootstrap versions.
4. Ensure GHCR package visibility and GitHub Actions permissions are configured.

## Support

Got questions?

- Home Assistant Community Forum: <https://community.home-assistant.io>
- Home Assistant Discord: <https://discord.gg/c5DvZ4e>
- Repository issues: <https://github.com/actualbudget-ha/app-actualbudget/issues>
