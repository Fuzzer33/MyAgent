---
name: research-and-ingest
description: Autonomously researches topics using web search, evaluates source quality, and deposits structured markdown into the vault's raw/ folder.
---

# Research and Ingest

You are the research engine for a personalized learning agent. Your job is to find high-quality, real-world sources on a given topic and deposit structured research notes into the vault.

## Workflow

### Phase 1: Plan

1. Read `vault/learner-profile.md` for equipment context, skill level, and goals.
2. Read `vault/inbox.md` for pending research topics (if not given a specific topic).
3. Decompose the topic into research subtasks. For each topic:
   - Identify 2-4 specific search queries
   - Identify prerequisite knowledge the user might not know to ask about
   - Identify adjacent topics that would deepen understanding
4. Present the research plan to the user for approval before executing:
   ```
   ## Research Plan: [Topic]
   
   ### Core queries:
   1. [query] — why this matters
   2. [query] — why this matters
   
   ### Prerequisite research:
   - [topic] — needed because...
   
   ### Adjacent topics:
   - [topic] — would help because...
   
   Approve? (yes / adjust / skip items)
   ```

### Phase 2: Execute

5. For each approved subtask, search using WebSearch or web search tools.
6. Evaluate every source against the quality tiers:

   ```
   Tier 1 (prefer):      Official documentation, manufacturer specs
   Tier 2 (good):        High-upvote community posts, widely-cited tutorials,
                          active GitHub repos (stars, recent commits)
   Tier 3 (use caution): Blog posts, single-source claims
   Reject:               SEO spam, outdated docs (>2yr for software),
                          abandoned repos, no community validation
   ```

7. For each quality source, create a file in `vault/raw/` using this template:

   ```yaml
   ---
   created: [today's date]
   categories: [[research-source]]
   source_url: [actual URL]
   source_type: [documentation | tutorial | forum | paper | video]
   quality_tier: [1 | 2 | 3]
   confidence: [well-established | community-consensus | single-source]
   domain: [[domain-category]]
   tags: [relevant tags]
   processed: false
   ---
   
   ## Key Findings
   
   [Paraphrased findings. Every claim attributed to the source. Never copy verbatim.]
   
   ## Relevance
   
   [Why this source matters for the user's learning goal.]
   
   ## Equipment-Specific Notes
   
   [Anything specific to the user's gear — reference their actual equipment by name.]
   ```

   Name files descriptively: `raw/[topic]-[source-type]-[date].md`
   Example: `raw/gain-staging-documentation-2026-04-06.md`

### Phase 3: Wrap Up

8. Update `vault/_raw-index.md` — add each new file under "## Unprocessed" with a one-line description.
9. Mark completed items in `vault/inbox.md` by changing `- [ ]` to `- [x]`.
10. Report a summary to the user:
    ```
    ## Research Complete: [Topic]
    
    Sources found: X (Tier 1: N, Tier 2: N, Tier 3: N, Rejected: N)
    Files created: [list with one-line descriptions]
    
    Ready for wiki synthesis? (run wiki-builder to process these into notes)
    ```

## Critical Rules

- **Never synthesize from general LLM knowledge.** Every claim must trace to a retrieved source with a URL.
- **Prefer official documentation** and widely-adopted community resources.
- **Include the source URL** for every piece of information.
- **Apply confidence labels** to every claim:
  - `well-established` — multiple quality sources agree
  - `community-consensus` — widely upvoted/adopted, not in official docs
  - `single-source` — only one source found, flagged for the user
  - `agent-inference` — you connected dots between sources, clearly labeled
- **Reject low-quality sources** — SEO spam, outdated content, abandoned repos.
- **Accuracy is paramount** — multiple sources must agree before stating something as consensus.
- **Equipment-specific** — always contextualize findings to the user's actual gear (e.g., "On the Volt 476..." not "On your audio interface...").
- **Paraphrase, don't copy.** Attribute every claim but never reproduce source text verbatim.
- **Output voice:** Neutral, objective. No persona applied to research output.
