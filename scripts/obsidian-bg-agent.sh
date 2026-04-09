#!/bin/bash
# Obsidian Second Brain Background Agent
# Fires after context compact — extracts learnings, synthesizes sources, checks health
# Runs headless via claude -p

VAULT_PATH="$(cd "$(dirname "$0")/../vault" && pwd)"
LOG="$VAULT_PATH/log.md"

echo "[$(date '+%Y-%m-%d %H:%M')] BG Agent: starting post-compact maintenance" >> "$LOG"

claude -p "You are a background vault maintenance agent. Read vault/_CLAUDE.md for structure rules. Then:
1. Run /obsidian-save to extract any conversation insights into vault/daily/
2. Run /obsidian-synthesize to process unprocessed raw/ sources
3. Run /obsidian-health to detect vault issues
Report results to vault/log.md. Be brief." 2>/dev/null

echo "[$(date '+%Y-%m-%d %H:%M')] BG Agent: complete" >> "$LOG"
