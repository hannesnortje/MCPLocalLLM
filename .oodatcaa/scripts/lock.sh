#!/usr/bin/env bash
set -euo pipefail
FILE="${1:?FILE required}"        # e.g., AGENT_LOG.md
CMD="${2:-acquire}"               # acquire|release
OWNER="${OWNER_TAG:-agent-locker}"
LOCK=".locks/${FILE}.lock"
mkdir -p .locks

now_iso() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
to_epoch() { date -u -d "$1" +%s; }

acquire() {
  if [ -f "$LOCK" ]; then
    CREATED=$(jq -r '.created_at // "1970-01-01T00:00:00Z"' "$LOCK")
    NOW=$(date -u +%s)
    CR_E=$(to_epoch "$CREATED")
    if [ $((NOW - CR_E)) -gt 300 ]; then
      echo "Breaking stale lock for $FILE"
    else
      echo "Lock is live; cannot acquire ($LOCK)"; exit 1
    fi
  fi
  printf '{ "owner": "%s", "created_at": "%s" }\n' "$OWNER" "$(now_iso)" > "$LOCK"
  echo "Acquired lock $LOCK"
}

release() {
  [ -f "$LOCK" ] && rm "$LOCK" || true
  echo "Released lock $LOCK"
}

case "$CMD" in
  acquire) acquire ;;
  release) release ;;
  *) echo "Usage: $0 FILE [acquire|release]"; exit 1 ;;
esac

