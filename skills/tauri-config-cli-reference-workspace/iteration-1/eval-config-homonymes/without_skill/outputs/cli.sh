#!/usr/bin/env bash
# Valide le bloc in-app plugins.cli de tauri.conf.json
# Usage: ./cli.sh [path/to/tauri.conf.json]
set -euo pipefail
CONF="${1:-$(dirname "$0")/tauri.conf.json}"

echo "== check $CONF =="
jq -e '.plugins.cli.description | type=="string"' "$CONF" >/dev/null \
  && echo "OK plugins.cli.description" \
  || { echo "FAIL plugins.cli.description"; exit 1; }

jq -e '.plugins.cli.args[] | select(.name=="verbose" and .short=="v" and .takes_value==false)' "$CONF" >/dev/null \
  && echo "OK args verbose (-v, takes_value=false)" \
  || { echo "FAIL args verbose (-v)"; exit 1; }

jq -e '.plugins.cli.subcommands.run.description | type=="string"' "$CONF" >/dev/null \
  && echo "OK subcommands.run.description" \
  || { echo "FAIL subcommands.run"; exit 1; }

jq -e '.plugins.cli.subcommands.run.args | map(.name) | contains(["debug","release"])' "$CONF" >/dev/null \
  && echo "OK subcommands.run args debug/release" \
  || { echo "FAIL subcommands.run args"; exit 1; }

jq -e '."$schema" | test("gen/schemas")' "$CONF" >/dev/null \
  && echo 'OK $schema gen/schemas' \
  || { echo 'FAIL $schema (attendu gen/schemas)'; exit 1; }

echo "== rappel homonymes =="
echo "dev (host):  tauri add cli / tauri dev / tauri build"
echo "in-app (runtime): getMatches() / CliExt + permission cli:default"
echo "ALL CHECKS PASSED"
