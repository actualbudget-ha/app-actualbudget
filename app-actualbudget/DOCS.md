# Home Assistant App: app-actualbudget

This app runs the official Actual Budget server in Home Assistant.

## Installation

Follow these steps to install this app on Home Assistant:

1. In Home Assistant, go to **Settings** > **Apps** > **Repositories**.
2. Add your custom repository URL that contains this app.
3. Open **app-actualbudget** and click **Install**.

## Access

- **Direct port**: open `https://<home-assistant-host>:5006` (recommended), or `http://<home-assistant-host>:5006` for non-TLS local testing.

## Ports

- `5006/tcp`: Actual Budget web UI (direct access mode)

## Data storage

Actual stores all server data in `/data` by default. In Home Assistant this is
the app data folder, so your data persists across restarts and upgrades.

## Configuration

These options map directly to Actual server environment variables:

- `port` -> `ACTUAL_PORT`
- `hostname` -> `ACTUAL_HOSTNAME`
- `upload_file_sync_size_limit_mb` -> `ACTUAL_UPLOAD_FILE_SYNC_SIZE_LIMIT_MB`
- `upload_sync_encrypted_file_sync_size_limit_mb` -> `ACTUAL_UPLOAD_SYNC_ENCRYPTED_FILE_SYNC_SIZE_LIMIT_MB`
- `upload_file_size_limit_mb` -> `ACTUAL_UPLOAD_FILE_SIZE_LIMIT_MB`
- `https_key` -> `ACTUAL_HTTPS_KEY`
- `https_cert` -> `ACTUAL_HTTPS_CERT`
- `extra_env_vars` -> exported as additional `KEY=VALUE` env vars

For all server settings, see:
https://actualbudget.org/docs/config/

Default app options are optimized for common Home Assistant setups:

- `hostname` defaults to `0.0.0.0` (IPv4 bind on all interfaces)
- `port` defaults to `5006`
- `https_key`/`https_cert` are empty by default and should be set when you want HTTPS directly on the app port

## TLS Certificate Files

When setting `https_key` and `https_cert`:

- Set both values together.
- Use file paths in `/ssl` or `/share`.
- Ensure those files exist before starting the app.

## First start

1. Install and start the app.
2. Open the app using direct access at `https://<home-assistant-host>:5006` (or `http://<home-assistant-host>:5006`).
3. Complete Actual Budget onboarding and create your server password.

## Upgrade and persistence

- App upgrades do not remove your Actual data in `/data`.
- Keep regular Home Assistant backups for disaster recovery.

## Manual validation checklist

1. Install and start the app from your repository.
2. Open direct port access (`https://<ha-host>:5006`) and confirm it loads.
3. (Optional) Open `http://<ha-host>:5006` and confirm it loads for non-TLS testing.
4. Restart the app and confirm existing data is still present.
5. Set an invalid `https_key` or `https_cert` path and confirm startup fails fast with clear logs.
6. Restore valid TLS configuration and confirm clean startup logs with add-on and Actual server version lines.

## Troubleshooting

- Check app logs in Home Assistant first.
- For startup failures, verify:
  - `https_key`/`https_cert` are valid existing files.
  - `extra_env_vars` entries are valid `KEY=VALUE`.
  - port `5006` is not blocked by another service.

## Support

- Home Assistant Community: https://community.home-assistant.io
- Actual Budget docs: https://actualbudget.org/docs/
- Repository issues: https://github.com/actualbudget-ha/app-actualbudget/issues
