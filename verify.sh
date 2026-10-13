#!/bin/sh
set -eu
schema_root="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$schema_root/verify.py" "$@"
