FROM python:3.13-alpine AS builder

RUN apk add --no-cache git

WORKDIR /build
COPY .git .git
COPY stickers/manifest.json stickers/manifest.json
COPY tools/scripts/build_site_manifest.py tools/scripts/build_site_manifest.py
COPY site site

RUN python tools/scripts/build_site_manifest.py

FROM nginxinc/nginx-unprivileged:1.29-alpine

USER root

COPY --chmod=644 nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder --chmod=644 /build/site /usr/share/nginx/html
COPY --chmod=644 stickers /usr/share/nginx/html/stickers

RUN chmod 755 /usr/share/nginx/html/stickers

USER 101

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
