# https://developers.home-assistant.io/docs/apps/configuration#app-dockerfile
ARG BUILD_FROM=docker.io/actualbudget/actual-server:26.4.0
FROM ${BUILD_FROM}

ENV \
    LANG="C.UTF-8" \
    DEBIAN_FRONTEND="noninteractive" \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_CMD_WAIT_FOR_SERVICES_MAXTIME=0 \
    S6_CMD_WAIT_FOR_SERVICES=1 \
    S6_SERVICES_READYTIME=50

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG \
    BUILD_ARCH \
    BUILD_VERSION \
    BASHIO_VERSION=0.17.1 \
    TEMPIO_VERSION=2024.11.2 \
    S6_OVERLAY_VERSION=3.1.6.2

RUN \
    set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        jq \
        xz-utils \
    && if [ -z "${BUILD_ARCH}" ]; then \
            DPKG_ARCH="$(dpkg --print-architecture)"; \
            if [ "${DPKG_ARCH}" = "amd64" ]; then \
                BUILD_ARCH="amd64"; \
            elif [ "${DPKG_ARCH}" = "arm64" ]; then \
                BUILD_ARCH="aarch64"; \
            else \
                BUILD_ARCH="${DPKG_ARCH}"; \
            fi; \
        fi \
    && if [ "${BUILD_ARCH}" = "amd64" ]; then \
            S6_ARCH="x86_64"; \
        elif [ "${BUILD_ARCH}" = "aarch64" ]; then \
            S6_ARCH="aarch64"; \
        else \
            S6_ARCH="${BUILD_ARCH}"; \
        fi \
    && curl -L -f -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-${S6_ARCH}.tar.xz" \
        | tar Jxvf - -C / \
    && curl -L -f -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz" \
        | tar Jxvf - -C / \
    && curl -L -f -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-arch.tar.xz" \
        | tar Jxvf - -C / \
    && curl -L -f -s "https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-noarch.tar.xz" \
        | tar Jxvf - -C / \
    && mkdir -p /etc/fix-attrs.d \
    && mkdir -p /etc/services.d \
    && curl -L -f -s -o /usr/bin/tempio \
        "https://github.com/home-assistant/tempio/releases/download/${TEMPIO_VERSION}/tempio_${BUILD_ARCH}" \
    && chmod a+x /usr/bin/tempio \
    && mkdir -p /usr/src/bashio \
    && curl -L -f -s "https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz" \
        | tar -xzf - --strip 1 -C /usr/src/bashio \
    && mv /usr/src/bashio/lib /usr/lib/bashio \
    && ln -s /usr/lib/bashio/bashio /usr/bin/bashio \
    && apt-get purge -y --auto-remove xz-utils \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/src/*

ENV APP_VERSION="${BUILD_VERSION}"

COPY rootfs /
RUN \
    find /etc/cont-init.d /etc/services.d -type f -exec sed -i 's/\r$//' {} + \
    && find /etc/cont-init.d /etc/services.d -type f -exec chmod a+x {} +

LABEL \
    io.hass.type="addon" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.version="${BUILD_VERSION}" \
    org.opencontainers.image.title="Home Assistant App: Actual Budget" \
    org.opencontainers.image.description="Self-hosted Actual Budget server for Home Assistant." \
    org.opencontainers.image.source="https://github.com/actualbudget-ha/app-actualbudget" \
    org.opencontainers.image.licenses="MIT"

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD s6-svstat /run/service/actualbudget | grep -q '^up ' || exit 1

CMD []
ENTRYPOINT ["/init"]
