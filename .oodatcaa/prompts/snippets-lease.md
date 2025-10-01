# Lease Snippets (informational)

Agents should use the .oodatcaa/scripts/lease.sh script or manage JSON files directly in .leases/

Example lease file (.leases/W123-step-01.json):
```json
{
  "task_id": "W123-step-01",
  "role": "builder",
  "owner": "agent-builder-A",
  "started_at": "2025-10-01T08:45:00Z",
  "ttl_seconds": 5400,
  "heartbeat_at": "2025-10-01T09:00:00Z"
}
```

Lease lifecycle:
- Acquire: check if no live lease exists (heartbeat_at + ttl_seconds > now)
- Heartbeat: update heartbeat_at field every ~10 minutes
- Release: delete lease file
- Takeover: if stale (heartbeat_at + ttl_seconds < now), note in AGENT_LOG.md and replace

