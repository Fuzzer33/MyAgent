---
name: reflection
description: Nightly reflection cycle. Reads episodic records from today, extracts patterns, creates daily-note summary, suggests next learning targets.
---

# Reflection

You run nightly (10 PM default) or when the user asks for reflection. Your job is to synthesize today's learning into patterns and vault updates.

## Startup

1. Read `vault/learner-profile.md` for learner context (domains, skill levels, current focus)
2. Read `vault/_CLAUDE.md` for vault structure rules
3. Determine today's date

## Phase 1: Gather Episodes

1. Scan `vault/daily/` for files created today (check `created` frontmatter)
2. Read each episode's topic, learner_confidence, patterns_noticed, next_actions
3. Group by domain and topic area

## Phase 2: Extract Patterns

From grouped episodes, identify:

1. **Recurring themes** — What concept appeared in multiple episodes?
2. **Misconceptions** — What did the learner struggle with?
3. **Skill progression** — Did confidence improve in any topic?
4. **Cross-domain connections** — What insights linked multiple domains?
5. **Equipment-specific patterns** — Any struggles with the user's actual gear?

## Phase 3: Process Unprocessed Sources

1. Read `vault/_raw-index.md` for unprocessed sources
2. If any exist, invoke `/obsidian-synthesize` to process them into wiki notes

## Phase 4: Detect 30-Day Patterns

1. Invoke `/obsidian-emerge` to surface patterns from recent episodes
2. If new [[evergreen]] notes are suggested, create them

## Phase 5: Create/Update Daily Note

1. Create `vault/daily/YYYY-MM-DD.md` from template (or update if exists)
2. Populate all sections:
   - **Summary:** Domains studied, topics covered, activity count
   - **Patterns Noticed:** Recurring themes from Phase 2
   - **Cross-Domain Connections:** Analogies and links between domains
   - **Vault Health:** New notes created, sources processed, dangling links
   - **Tomorrow's Focus:** Based on patterns, what to study next

Format patterns as actionable insights:
```
- Asked about [topic] in [domain] multiple times → needs deeper coverage
- Connection: [[concept-A]] (domain 1) mirrors [[concept-B]] (domain 2)
- [Equipment] came up repeatedly — may need dedicated practice drill
```

## Phase 6: Report

```
## Nightly Reflection Complete

### Today's Learning
- Studied [N] domains, [N] topics
- [Domain]: [topics], confidence: [levels]

### Patterns
- [Pattern] → [implication]

### Vault Updates
- Created: [N] notes
- Processed: [N] raw sources
- New [[evergreen]] notes: [list]

### Tomorrow's Focus
- **Recommended:** [topic] — [why]
- **Also consider:** [alternatives]

Daily note: [[daily/YYYY-MM-DD]]
```

## Manual Invocation

- "Reflect on today" → full Phase 1-6
- "What patterns do you see?" → Phase 2 only, report patterns
- "Vault health" → dispatch to `/obsidian-health`

## Rules

- **Read vault/_CLAUDE.md first** for deposit locations and frontmatter schema
- **Never write to learner-profile.md** — suggest profile updates to the user, route through learning-profile skill
- **Cite episode files** when reporting patterns: "Based on [[daily/2026-04-09-gain-staging-session]]..."
- **Patterns must have evidence** — link back to specific episodes or notes
- **Equipment-specific** — mention the user's actual gear by name
