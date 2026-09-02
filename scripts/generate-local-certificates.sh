#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
package_dir="$repo_root/framework/XSSApp-1.1.0/XSSApp"
certificate="$package_dir/server.crt"
private_key="$package_dir/server.key"

openssl req \
  -x509 \
  -newkey ec \
  -pkeyopt ec_paramgen_curve:prime256v1 \
  -sha256 \
  -nodes \
  -days 30 \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1" \
  -keyout "$private_key" \
  -out "$certificate"

chmod 600 "$private_key"
printf 'Generated %s and %s\n' "$certificate" "$private_key"
