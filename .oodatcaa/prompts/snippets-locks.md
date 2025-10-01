# Lock Snippets (informational)

Agents should use the .oodatcaa/scripts/lock.sh script or manage JSON files directly in .locks/

Example lock file (.locks/AGENT_LOG.md.lock):
```json
{
  "owner": "agent-builder-A",
  "created_at": "2025-10-01T09:15:00Z"
}
```

Lock lifecycle:
- Acquire: check if no lock exists or lock is stale (created_at + 5 minutes < now)
- If stale: break lock and log note in AGENT_LOG.md
- Release: delete lock file after writing
- Locks protect shared files during writes (AGENT_LOG.md, SPRINT_QUEUE.json, etc.)

