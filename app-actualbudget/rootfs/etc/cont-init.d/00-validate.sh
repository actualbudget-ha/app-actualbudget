#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
# ==============================================================================
# Validate app configuration before starting Actual Budget
# ==============================================================================
set -euo pipefail

declare https_key
declare https_cert
declare extra_env_count
declare env_entry
declare env_name
declare has_supervisor

# shellcheck source=/dev/null
source /usr/share/actualbudget/config.sh

validate_path_option() {
    local option_value=$1
    local option_name=$2

    if [[ "${option_value}" != /ssl/* ]] && [[ "${option_value}" != /share/* ]]; then
        bashio::log.error \
            "Invalid ${option_name} path '${option_value}'. Use a path in /ssl or /share."
        exit 1
    fi

    if [[ ! -f "${option_value}" ]]; then
        bashio::log.error \
            "Configured ${option_name} file does not exist: ${option_value}"
        exit 1
    fi
}

init_config

https_key="$(config_or_default 'https_key' '')"
https_cert="$(config_or_default 'https_cert' '')"

if [[ -n "${https_key}" ]] || [[ -n "${https_cert}" ]]; then
    if [[ -z "${https_key}" ]] || [[ -z "${https_cert}" ]]; then
        bashio::log.error \
            "Both https_key and https_cert must be set together."
        exit 1
    fi

    validate_path_option "${https_key}" "https_key"
    validate_path_option "${https_cert}" "https_cert"
fi

extra_env_count="$(read_config 'extra_env_vars | length')"
if ! [[ "${extra_env_count}" =~ ^[0-9]+$ ]]; then
    extra_env_count=0
fi
for (( i=0; i < extra_env_count; i++ )); do
    env_entry="$(read_config "extra_env_vars[${i}]")"

    if [[ "${env_entry}" != *=* ]]; then
        bashio::log.error \
            "Invalid extra_env_vars entry '${env_entry}'. Expected KEY=VALUE format."
        exit 1
    fi

    env_name="${env_entry%%=*}"
    validate_extra_env_name "${env_name}"
done

bashio::log.info "Configuration validation completed"
