#!/usr/bin/env bash
set -euo pipefail
TASK_ID="${1:?TASK_ID required}"   # e.g., W123-step-01
ROLE="${2:?ROLE required}"         # builder|tester|integrator|planner|refiner
CMD="${3:-acquire}"                # acquire|beat
OWNER="${OWNER_TAG:-agent-$ROLE}"  # set OWNER_TAG env or via prompt
TTL="${TTL:-3600}"                 # seconds

LEASE=".leases/${TASK_ID}.json"
mkdir -p .leases

now_iso() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
to_epoch() { date -u -d "$1" +%s; }

acquire() {
  if [ -f "$LEASE" ]; then
    HB=$(jq -r '.heartbeat_at // empty' "$LEASE" || true)
    TS=$(jq -r '.ttl_seconds // 0' "$LEASE" || echo 0)
    if [ -n "$HB" ] && [ -n "$TS" ]; then
      NOW=$(date -u +%s)
      HB_E=$(to_epoch "$HB")
      if [ $((NOW - HB_E)) -lt "$TS" ]; then
        echo "Lease is live; cannot acquire ($LEASE)"; exit 1
      else
        echo "Taking over stale lease for $TASK_ID"
      fi
    fi
  fi
  cat > "$LEASE" <<JSON
{
  "task_id": "$TASK_ID",
  "role": "$ROLE",
  "owner": "$OWNER",
  "started_at": "$(now_iso)",
  "ttl_seconds": $TTL,
  "heartbeat_at": "$(now_iso)"
}
JSON
  echo "Acquired lease $LEASE as $OWNER"
}

heartbeat() {
  [ -f "$LEASE" ] || (echo "No lease to heartbeat"; exit 1)
  TMP="$(mktemp)"
  jq --arg now "$(now_iso)" '.heartbeat_at=$now' "$LEASE" > "$TMP" && mv "$TMP" "$LEASE"
  echo "Heartbeat $(now_iso) for $LEASE"
}

case "$CMD" in
  acquire) acquire ;;
  beat) heartbeat ;;
  *) echo "Usage: $0 TASK_ID ROLE [acquire|beat]"; exit 1 ;;
esac

