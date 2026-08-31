#!/usr/bin/env bash
# Tests the rendered init script inside the same image the chart's init container
# uses (mikefarah/yq:4). Covers the /config/.storage/http seeding guards added for
# https://github.com/pajikos/home-assistant-helm-chart/issues/187:
#   - a fresh install gets a valid seeded storage file
#   - an existing .storage/http is never touched
#   - a configuration.yaml with an http block skips seeding (HA imports it itself)
#   - a pre-2026.8 render (no http-storage.json) seeds nothing
#
# Requires: helm, docker. Uses docker cp instead of volume mounts so it also works
# where the docker daemon cannot bind-mount the working directory.
set -euo pipefail

CHART_DIR="$(cd "$(dirname "$0")/../../charts/home-assistant" && pwd)"
IMAGE="mikefarah/yq:4"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

FAILURES=0

# yq from the test image, reading stdin, so the host needs no yq install
dyq() {
  docker run --rm -i --user 0 --entrypoint yq "$IMAGE" "$@"
}

fail() {
  echo "FAIL: $1"
  FAILURES=$((FAILURES + 1))
}

pass() {
  echo "PASS: $1"
}

# Renders the chart's init.sh plus config templates into $1, with extra helm args from $2...
render() {
  local dir="$1"
  shift
  mkdir -p "$dir/mnt-init" "$dir/config-templates"
  helm template "$CHART_DIR" --set configuration.enabled=true --set ingress.external=true "$@" \
    -s templates/configmap-init-script.yaml | dyq '.data["init.sh"]' - > "$dir/mnt-init/init.sh"
  helm template "$CHART_DIR" --set configuration.enabled=true --set ingress.external=true "$@" \
    -s templates/configmap-hass-config.yaml > "$dir/hass-config.yaml"
  dyq '.data["configuration.yaml"]' - < "$dir/hass-config.yaml" > "$dir/config-templates/configuration.yaml"
  if [ "$(dyq '.data | has("http-storage.json")' - < "$dir/hass-config.yaml")" = "true" ]; then
    dyq '.data["http-storage.json"]' - < "$dir/hass-config.yaml" > "$dir/config-templates/http-storage.json"
  fi
}

# Runs init.sh in the image against $1/config and $1/config-templates; output lands in $1/out
run_init() {
  local dir="$1"
  local cid
  cid=$(docker create --user 0 --entrypoint /bin/sh "$IMAGE" -c "/bin/sh /mnt/init/init.sh")
  docker cp "$dir/config" "$cid:/config" > /dev/null
  docker cp "$dir/config-templates" "$cid:/config-templates" > /dev/null
  docker cp "$dir/mnt-init" "$cid:/mnt/init" > /dev/null
  docker start "$cid" > /dev/null
  local rc
  rc=$(docker wait "$cid")
  docker logs "$cid" 2>&1 | sed 's/^/    | /'
  docker cp "$cid:/config" "$dir/out" > /dev/null
  docker rm -f "$cid" > /dev/null
  return "$rc"
}

echo "==> case 1: fresh install seeds /config/.storage/http"
CASE="$WORKDIR/fresh"
render "$CASE" --set configuration.trusted_proxies='{10.100.0.0/16}'
mkdir -p "$CASE/config"
if run_init "$CASE"; then pass "init script exits 0"; else fail "init script exited non-zero"; fi
[ -f "$CASE/out/configuration.yaml" ] && pass "configuration.yaml created" || fail "configuration.yaml missing"
if [ -f "$CASE/out/.storage/http" ]; then
  pass ".storage/http seeded"
  if dyq -o=json '.' - < "$CASE/out/.storage/http" > /dev/null; then pass "seeded file is valid JSON"; else fail "seeded file is not valid JSON"; fi
  [ "$(dyq '.data.stable.trusted_proxies[0]' - < "$CASE/out/.storage/http")" = "10.100.0.0/16" ] \
    && pass "trusted proxies rendered" || fail "trusted proxies wrong"
  [ "$(dyq '.data.stable.created_at' - < "$CASE/out/.storage/http")" != "null" ] \
    && pass "created_at stamped" || fail "created_at not stamped"
  [ "$(dyq '.data.yaml_migration_done' - < "$CASE/out/.storage/http")" = "true" ] \
    && pass "yaml migration marked done" || fail "yaml_migration_done not true"
else
  fail ".storage/http not seeded"
fi
[ ! -f "$CASE/out/.storage/http.tmp" ] && pass "no temp file left behind" || fail "temp file left behind"

echo "==> case 2: existing .storage/http is never overwritten"
CASE="$WORKDIR/existing-storage"
render "$CASE"
mkdir -p "$CASE/config/.storage"
cp "$WORKDIR/fresh/config-templates/configuration.yaml" "$CASE/config/configuration.yaml"
echo '{"sentinel": true}' > "$CASE/config/.storage/http"
if run_init "$CASE"; then pass "init script exits 0"; else fail "init script exited non-zero"; fi
if diff -q <(echo '{"sentinel": true}') "$CASE/out/.storage/http" > /dev/null; then
  pass "existing storage untouched"
else
  fail "existing storage was modified"
fi

echo "==> case 3: configuration.yaml with an http block skips seeding"
CASE="$WORKDIR/yaml-http"
render "$CASE"
mkdir -p "$CASE/config"
printf 'default_config:\nhttp:\n  use_x_forwarded_for: true\n  trusted_proxies:\n    - 192.168.0.0/16\n' > "$CASE/config/configuration.yaml"
if run_init "$CASE"; then pass "init script exits 0"; else fail "init script exited non-zero"; fi
[ ! -f "$CASE/out/.storage/http" ] && pass "seeding skipped for upgrader" || fail "storage seeded despite http block in configuration.yaml"

echo "==> case 4: pre-2026.8 render seeds nothing"
CASE="$WORKDIR/old-ha"
render "$CASE" --set image.tag=2026.7.4
[ ! -f "$CASE/config-templates/http-storage.json" ] || fail "old HA render unexpectedly produced http-storage.json"
mkdir -p "$CASE/config"
if run_init "$CASE"; then pass "init script exits 0"; else fail "init script exited non-zero"; fi
[ ! -f "$CASE/out/.storage/http" ] && pass "no storage seeded on old HA" || fail "storage seeded on old HA"
grep -q "use_x_forwarded_for: true" "$CASE/out/configuration.yaml" \
  && pass "old HA keeps the http yaml block" || fail "http yaml block missing on old HA"

echo "==> case 5: pre-existing configuration.yaml skips seeding even without an http block"
CASE="$WORKDIR/existing-config"
render "$CASE"
mkdir -p "$CASE/config"
printf 'default_config:\n' > "$CASE/config/configuration.yaml"
if run_init "$CASE"; then pass "init script exits 0"; else fail "init script exited non-zero"; fi
[ ! -f "$CASE/out/.storage/http" ] && pass "seeding skipped for pre-existing configuration" \
  || fail "storage seeded despite pre-existing configuration.yaml (http may be configured via packages or includes)"

echo "==> case 6: fresh install with a custom templateConfig containing http skips seeding"
CASE="$WORKDIR/custom-template"
render "$CASE"
printf 'default_config:\nhttp:\n  use_x_forwarded_for: true\n' > "$CASE/config-templates/configuration.yaml"
mkdir -p "$CASE/config"
if run_init "$CASE"; then pass "init script exits 0"; else fail "init script exited non-zero"; fi
[ ! -f "$CASE/out/.storage/http" ] && pass "seeding skipped for custom template with http block" \
  || fail "storage seeded despite http block in the config template"

echo
if [ "$FAILURES" -gt 0 ]; then
  echo "$FAILURES assertion(s) failed"
  exit 1
fi
echo "All init-script tests passed"
