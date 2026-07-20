#!/usr/bin/env bash
# shellcheck shell=bash

init_config() {
    has_supervisor='false'
    if [[ -n "${SUPERVISOR_TOKEN:-}" ]]; then
        has_supervisor='true'
    fi
}

read_config() {
    local key=$1
    local value

    value=''
    if [[ "${has_supervisor}" == 'true' ]]; then
        value="$(bashio::config "${key}" 2>/dev/null || true)"
    fi

    if [[ -z "${value}" || "${value}" == "null" ]] && [[ -f /data/options.json ]]; then
        value="$(jq -er ".${key}" /data/options.json 2>/dev/null || true)"
    fi

    printf '%s' "${value}"
}

config_or_default() {
    local key=$1
    local default_value=$2
    local value

    value="$(read_config "${key}")"
    if [[ -z "${value}" ]] || [[ "${value}" == "null" ]]; then
        printf '%s' "${default_value}"
        return
    fi

    printf '%s' "${value}"
}

is_reserved_extra_env_name() {
    local env_name=$1

    case "${env_name}" in
        ACTUAL_PORT | \
        ACTUAL_HOSTNAME | \
        ACTUAL_UPLOAD_FILE_SYNC_SIZE_LIMIT_MB | \
        ACTUAL_UPLOAD_SYNC_ENCRYPTED_FILE_SYNC_SIZE_LIMIT_MB | \
        ACTUAL_UPLOAD_FILE_SIZE_LIMIT_MB | \
        ACTUAL_HTTPS_KEY | \
        ACTUAL_HTTPS_CERT | \
        ACTUAL_DATA_DIR | \
        ACTUAL_CONFIG_PATH | \
        ACTUAL_SERVER_FILES | \
        ACTUAL_USER_FILES | \
        ACTUAL_WEB_ROOT | \
        APP_VERSION | \
        BASHIO_LOG_LEVEL | \
        NODE_ENV | \
        NODE_OPTIONS | \
        PATH | \
        LD_PRELOAD | \
        LD_LIBRARY_PATH)
            return 0
            ;;
        S6_*)
            return 0
            ;;
    esac

    return 1
}

validate_extra_env_name() {
    local env_name=$1

    if ! [[ "${env_name}" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
        bashio::log.error \
            "Invalid environment variable name in extra_env_vars: '${env_name}'"
        exit 1
    fi

    if is_reserved_extra_env_name "${env_name}"; then
        bashio::log.error \
            "Reserved environment variable in extra_env_vars: '${env_name}'. Use the app option for managed settings or choose a supported Actual advanced setting."
        exit 1
    fi
}
