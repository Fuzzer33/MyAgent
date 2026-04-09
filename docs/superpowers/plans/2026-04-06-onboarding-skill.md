# Onboarding Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first-time setup and domain intake flow that distills a user's existing knowledge from a verbal dump into a structured learner profile with knowledge classification, gap analysis, and a goal-derived learning path.

**Architecture:** New `onboarding` skill handles two flows: (1) first-time user setup (identity + preferences + first domain) and (2) deep domain intake (repeatable). The session-router detects first-time vs returning users and routes accordingly. The learner-profile schema gains `partial_topics`, `misconceptions`, and `learning_path` fields. The tutor skill gains a review mode for partial-knowledge topics.

**Tech Stack:** Claude Code skills (SKILL.md prompt files), YAML frontmatter in Obsidian vault markdown files.

---

## File Structure

| File | Action | Responsibility |
|---|---|---|
| `.claude/skills/onboarding/SKILL.md` | **Create** | New skill: first-time setup + deep domain intake with knowledge distillation |
| `.claude/skills/session-router/SKILL.md` | **Modify** | Add first-time detection logic, onboarding route |
| `.claude/skills/learning-profile/SKILL.md` | **Modify** | Update §4 to delegate deep intake to onboarding; add schema for new fields |
| `.claude/skills/tutor/SKILL.md` | **Modify** | Add review mode for partial-knowledge topics; handle misconception correction |
| `vault/learner-profile.md` | **Modify** | Update schema to include `partial_topics`, `misconceptions`, `learning_path` |
| `vault/templates/learner-profile-template.md` | **Create** | Blank profile template for new users |
| `CLAUDE.md` | **Modify** | Add `onboarding` skill to architecture list |

---

### Task 1: Create the Learner Profile Template

**Why:** The onboarding skill needs a blank-slate template to generate new profiles from. Currently `learner-profile.md` is pre-populated with hardcoded data. A template gives new users a clean starting point and documents the full schema including the new fields.

**Files:**
- Create: `vault/templates/learner-profile-template.md`

- [ ] **Step 1: Create the template file**

This template defines the complete schema for a learner profile, including the new `partial_topics`, `misconceptions`, and `learning_path` fields that don't exist in the current profile.

```markdown
---
name: ""
created: {{date}}

learning_style:
  input_mode: ""          # verbal-stream | structured | visual
  conceptual_approach: "" # big-picture-first | details-first | example-first
  learning_mode: ""       # build-then-learn | theory-first | mixed
  analogy_preference: ""  # cross-domain | within-domain | minimal
  overwhelm_sensitivity: "" # high | medium | low
  momentum_style: ""      # burst | steady | scheduled

tutor_persona:
  name: ""
  personality: ""         # direct-mentor | patient-coach | enthusiastic-peer | dry-wit-professor
  verbosity: ""           # concise | moderate | detailed
  celebrate_progress: true
  use_cross_domain_analogies: true

domains: []
# Domain entry schema:
#  - name: "[[domain-name]]"
#    skill_level: beginner | intermediate | advanced
#    equipment: ["[[tool1]]", "[[tool2]]"]
#    goals: [goal1, goal2]
#    completed_topics:
#      - { topic: "topic name", confidence: solid }
#    partial_topics:
#      - { topic: "topic name", note: "what they know vs what's missing" }
#    misconceptions:
#      - { topic: "topic name", note: "what they believe vs what's correct" }
#    current_focus: null
#    queued_topics: []
#    learning_path:
#      - goal: "goal name"
#        path: ["topic1 ✓", "topic2 ~", "topic3", "topic4"]

last_updated: {{date}}
---
```

- [ ] **Step 2: Commit**

```bash
git add vault/templates/learner-profile-template.md
git commit -m "feat: add learner profile template with extended schema"
```

---

### Task 2: Create the Onboarding Skill

**Why:** This is the core new skill. It handles two distinct flows: first-time user setup (identity, preferences, persona selection, first domain) and deep domain intake (knowledge distillation from verbal dumps, goal decomposition, learning path generation). The domain intake flow is repeatable — users invoke it each time they add a new subject.

**Files:**
- Create: `.claude/skills/onboarding/SKILL.md`

- [ ] **Step 1: Create the skill directory**

```bash
mkdir -p .claude/skills/onboarding
```

- [ ] **Step 2: Write the SKILL.md**

```markdown
---
name: onboarding
description: First-time user setup and deep domain intake. Distills verbal knowledge dumps into structured profiles with classified topics, gap analysis, and goal-derived learning paths.
---

# Onboarding

You handle two flows for the personalized learning agent: **first-time setup** (new user, no profile) and **deep domain intake** (adding a new subject area). The session-router dispatches you when it detects either case.

## Flow A: First-Time Setup

Triggered when `vault/learner-profile.md` does not exist or contains no `name` value.

### Step 1 — Welcome & Identity

Greet the user warmly (no persona yet — that comes in Step 2). Explain what this agent does in 2-3 sentences:
- "I'm a learning agent that researches real sources, builds you a personal knowledge base, and teaches from it."
- "First, I need to learn about you so I can tailor everything."

Ask for their name.

### Step 2 — Learning Style Discovery

Rather than presenting a checklist of options, have a brief conversation to infer learning style. Ask 2-3 natural questions:

1. "When you're learning something new, do you prefer to understand the big picture first, or jump straight into details and examples?"
   - Maps to `conceptual_approach`: big-picture-first | details-first | example-first
2. "Do you prefer to try building something and learn as you go, or understand the theory before you start?"
   - Maps to `learning_mode`: build-then-learn | theory-first | mixed
3. "When things get complex, do you prefer I slow down and break it into small pieces, or keep the pace up as long as you're following?"
   - Maps to `overwhelm_sensitivity`: high | medium | low
   - Also informs `momentum_style`: burst (prefers pace when engaged) | steady | scheduled

Set defaults for fields not directly asked:
- `input_mode`: default to `verbal-stream` (can be adjusted later)
- `analogy_preference`: default to `cross-domain` (can be adjusted later)

### Step 3 — Persona Selection

Present the four tutor persona options with a short sample of each:

```
Pick a teaching style that suits you:

1. **Direct Mentor** — Efficient, cuts to the point. No hand-holding.
   → "Here's the deal with gain staging. Three things matter..."

2. **Patient Coach** — Warm, encouraging, checks in frequently.
   → "Let's take this step by step. How's that landing so far?"

3. **Enthusiastic Peer** — High energy, fellow-learner vibe.
   → "Okay so this is actually really cool once it clicks!"

4. **Dry-Wit Professor** — Structured, methodical, occasional dry humor.
   → "Riveting topic, I know. But get this wrong and everything suffers."
```

Ask what name they want to call their tutor (default: "Tutor").

Ask verbosity preference: concise, moderate, or detailed.

### Step 4 — First Domain

Transition to Flow B (Deep Domain Intake) for their first subject area. They must set up at least one domain to complete onboarding.

### Step 5 — Write Profile

1. Read `vault/templates/learner-profile-template.md` for the schema.
2. Populate all fields from Steps 1-4.
3. Write the completed profile to `vault/learner-profile.md`.
4. Update `last_updated` to today's date.

### Step 6 — Handoff

Summarize what was set up. Suggest next actions:
- "Want me to start researching [first topic from learning path]?"
- "Or ask me to teach you about something you already have partial knowledge on."

---

## Flow B: Deep Domain Intake

Triggered when a returning user wants to add a new domain, OR as part of first-time setup (Step 4). This is the **repeatable** flow.

### Step 1 — Domain Basics

Ask three questions:
1. "What subject do you want to learn?" → domain name
2. "What are your goals — what do you want to be able to *do*?" → goals list
3. "What tools, equipment, or software do you already have for this?" → equipment list

### Step 2 — The Knowledge Dump

This is the core differentiator. Prompt the user to tell you everything they know:

> "Now tell me everything you already know about [domain]. Don't worry about being organized — just talk. Ramble is fine. Tell me what you've learned, what you've tried, what you've watched videos about, what confuses you, what you think you understand but aren't sure about. The more you give me, the better I can figure out where to start."

**Critical rules for processing the dump:**
- Let them talk. Do NOT interrupt with clarifying questions until they're done.
- If they pause and seem finished, ask: "Anything else? Even half-remembered things help."
- Accept messy, stream-of-consciousness, contradictory input. That's the signal.

### Step 3 — Knowledge Distillation

After the user finishes their dump, analyze it and produce a structured classification. For each identifiable concept or topic they mentioned:

**Classification tiers:**

| Confidence | Criteria | Profile field | Agent behavior |
|---|---|---|---|
| `solid` | They explained it correctly with detail, used correct terminology, described practical experience | `completed_topics` | Skip in teaching. Available for cross-domain analogies. |
| `partial` | They mentioned it but with gaps, uncertainty, or no hands-on experience. "I've seen videos about X but never tried it." | `partial_topics` | Review mode — don't teach from scratch, but fill gaps and assign practice. |
| `misconception` | They stated something factually incorrect or have a flawed mental model. | `misconceptions` | Correct gently during tutoring. Flag as high-priority. |

**How to classify — be generous but honest:**
- If they can explain *why* something works, not just *what* it is → `solid`
- If they know the term and rough concept but can't explain the mechanism → `partial`
- If they describe something that contradicts established knowledge → `misconception`
- When in doubt between solid and partial, choose `partial` — better to review than to skip

**Present the classification back to the user for validation:**

```
## Here's what I heard:

### ✅ Solid — you know this well:
- [Topic] — [brief evidence from their words]

### 🔶 Partial — you've been exposed but have gaps:
- [Topic] — [what they know] / [what's missing]

### ⚠️ Misconception — we should correct this:
- [Topic] — you said [X], but actually [Y]. We'll address this.

### 🔍 Not mentioned — foundational topics for your goals:
- [Topic] — needed for [goal], wasn't in your description

Does this look right? Anything I miscategorized?
```

Let them correct the classification. Move topics between tiers as needed.

### Step 4 — Skill Level Inference

Based on the distillation results, infer an overall skill level:

- **beginner**: Mostly unmentioned topics, few solid, several misconceptions
- **intermediate**: Mix of solid and partial, few misconceptions, understands core concepts
- **advanced**: Mostly solid, partial only on niche topics, no misconceptions on fundamentals

State the inferred level and let the user adjust it.

### Step 5 — Learning Path Generation

For each stated goal, decompose it into an ordered sequence of topics:

1. Identify all topics needed to achieve the goal
2. Order them by prerequisites (foundational → advanced)
3. Mark each topic with its status from distillation:
   - `✓` = solid (will be skipped)
   - `~` = partial (review mode)
   - `✗` = misconception (correction priority)
   - (unmarked) = not yet learned

```
## Learning Path

### Goal: [goal name]
1. [Topic A] ✓ (you've got this)
2. [Topic B] ~ (quick review needed)
3. [Topic C] ✗ (we need to fix a misconception here)
4. [Topic D] (new — this is where real learning starts)
5. [Topic E] (new)
6. [Topic F] (new — this achieves your goal)

**Starting point:** [Topic B] — quick review, then on to [Topic D].
```

Set `current_focus` to the first non-solid topic in the highest-priority goal's path.
Populate `queued_topics` with the next 3-5 topics after current_focus.

### Step 6 — Write to Profile

1. Read current `vault/learner-profile.md`.
2. Append the new domain entry with all classified fields.
3. Update `last_updated`.
4. Write the updated file.

**Important:** This is an exception to the "only learning-profile writes to learner-profile.md" rule. During onboarding, this skill writes the initial domain data directly because it has the full distillation context. After onboarding, all updates go through learning-profile.

### Step 7 — Seed the Vault

1. Create a category note in vault root: `vault/[domain-name].md` using the category template.
2. Add the first 3-5 unknown topics from the learning path to `vault/inbox.md` as research items.
3. Update `vault/_master-index.md` to include the new category.

### Step 8 — Report & Handoff

```
## Domain Setup Complete: [Domain]

**Skill level:** [level]
**Topics classified:** [N] solid, [N] partial, [N] misconceptions, [N] new
**Learning path:** [N] topics across [N] goals
**Current focus:** [topic]
**Research seeded:** [N] topics added to inbox

Ready to start? Options:
1. "Research [first unknown topic]" — kicks off research-and-ingest
2. "Review [first partial topic]" — quick review session with tutor
3. "Correct [first misconception]" — address a misconception
4. "Add another domain" — set up another subject area
```

---

## Critical Rules

- **Let them ramble.** The verbal dump is the most valuable input. Never cut it short or ask them to be more organized.
- **Classify generously but honestly.** When in doubt, `partial` over `solid`. Better to review than to create false confidence.
- **Always validate the classification.** Show the user what you heard and let them correct it. They know themselves better than you do.
- **Misconceptions are not failures.** Frame them as "things to straighten out" not "things you got wrong."
- **Learning paths are goal-driven.** Every topic in the path must connect to a stated goal. No "nice to know" padding.
- **This skill writes to `learner-profile.md` during onboarding only.** After initial setup, all profile writes go through the learning-profile skill.
- **Preserve existing data.** When adding a new domain to an existing profile, read the full file first and preserve all other domains and settings.
- **Equipment names matter.** Store the exact names they give you. "My Canon R6" becomes `[[Canon R6]]`, not `[[camera]]`.
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/onboarding/SKILL.md
git commit -m "feat: add onboarding skill with first-time setup and knowledge distillation"
```

---

### Task 3: Update Session Router for First-Time Detection

**Why:** The session-router currently assumes a profile exists. It needs to detect new users (no profile or empty profile) and route them to onboarding. It also needs a new intent for "I want to add a new domain" which should route to onboarding Flow B.

**Files:**
- Modify: `.claude/skills/session-router/SKILL.md`

- [ ] **Step 1: Add first-time detection to the Startup section**

Replace the current Startup section (lines 10-18) with:

```markdown
## Startup

1. Check if `vault/learner-profile.md` exists.
2. **If it does not exist, or if the `name` field is empty, or if `domains` is an empty list:**
   - This is a first-time user. Invoke the `/onboarding` skill immediately. Do not greet or classify intent — go straight to onboarding.
   - Stop here. The onboarding skill handles everything.
3. **If the profile exists and has at least one domain:**
   - Read `vault/learner-profile.md` to load the user's profile, domains, equipment, skill levels, and tutor persona.
   - Greet the user using the configured `tutor_persona` tone:
     - `direct-mentor`: Brief, no fluff. "What are we working on?"
     - `patient-coach`: Warm check-in. "Hey! What would you like to focus on today?"
     - `enthusiastic-peer`: High energy. "Let's learn something awesome — what's on your mind?"
     - `dry-wit-professor`: Understated. "Class is in session. What's the topic?"
   - Check `vault/inbox.md` for pending items. If there are pending items, briefly mention them as options.
```

- [ ] **Step 2: Add onboarding intent to the Intent Classification table**

Add a new row to the intent classification table (after the existing rows, before Ambiguous):

```markdown
| Onboard | "I want to learn [new field]", "add a new subject", "new domain", "set up [topic]" | `/onboarding` (Flow B) |
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/session-router/SKILL.md
git commit -m "feat: add first-time detection and onboarding route to session-router"
```

---

### Task 4: Update Learning Profile Skill

**Why:** The learning-profile skill's §4 (New Domain Onboarding) currently handles domain setup with 3 quick questions. This should delegate to the onboarding skill for deep intake, while keeping a lightweight option for users who just want to quickly add a domain without the full verbal dump. The skill also needs to understand the new schema fields (`partial_topics`, `misconceptions`, `learning_path`).

**Files:**
- Modify: `.claude/skills/learning-profile/SKILL.md`

- [ ] **Step 1: Replace §4 (New Domain Onboarding) with updated version**

Replace the current section 4 (lines 66-83) with:

```markdown
### 4. New Domain Onboarding ("I want to learn [new field]")

**Two modes:**

**Deep intake (default):** Route to the `/onboarding` skill (Flow B). This runs the full knowledge distillation pipeline — verbal dump, classification, gap analysis, learning path. Use this when:
- The user is adding a domain they have existing knowledge in
- The user wants a structured learning path to specific goals
- It's the user's first time setting up any domain

Tell the user: "Let me switch you to the onboarding flow — it'll help me understand what you already know so I don't waste your time re-teaching things."

**Quick add (on request):** If the user explicitly asks for a quick/minimal setup, or says they know nothing about the topic, create a basic entry:
1. Ask about:
   - Equipment/tools they have for this domain
   - Goals (what do they want to be able to do?)
2. Create a new domain entry in `vault/learner-profile.md`:
   ```yaml
   - name: "[[new-domain]]"
     skill_level: beginner
     equipment: ["[[tool1]]", "[[tool2]]"]
     goals: [goal1, goal2]
     completed_topics: []
     partial_topics: []
     misconceptions: []
     current_focus: null
     queued_topics: []
     learning_path: []
   ```
3. Create a category note in vault root: `vault/[new-domain].md`
4. Add initial research topics to `vault/inbox.md`
5. Suggest: "Want me to research the fundamentals?"
```

- [ ] **Step 2: Update §2 (Progress Update) to handle the new topic types**

Add the following after the existing skill level milestone check (after line 46, before "5. Write updated"):

```markdown
   - When marking a `partial_topics` item as understood, move it to `completed_topics` with `confidence: solid`
   - When a `misconceptions` item is corrected (user demonstrates correct understanding), move it to `completed_topics` with `confidence: solid` and remove from `misconceptions`
   - Update `learning_path` entries: change status markers (`~` → `✓` for partials completed, `✗` → `✓` for misconceptions corrected)
```

- [ ] **Step 3: Update §1 (Status Overview) to report new fields**

Add to the per-domain report (after line 20, the existing report items):

```markdown
   - Partial topics needing review (count)
   - Active misconceptions needing correction (count)
   - Learning path progress per goal (e.g., "3/8 topics complete for [goal]")
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/learning-profile/SKILL.md
git commit -m "feat: update learning-profile to delegate deep intake and handle new schema fields"
```

---

### Task 5: Update Tutor Skill with Review Mode and Misconception Handling

**Why:** The tutor currently has one mode per action (explain, quiz, drill, clarify, connect). It needs to differentiate between teaching a brand-new topic vs reviewing a partial-knowledge topic vs correcting a misconception. These require different pedagogical approaches.

**Files:**
- Modify: `.claude/skills/tutor/SKILL.md`

- [ ] **Step 1: Add Review teaching mode**

Add the following after the existing "Connect" mode section (after line 68):

```markdown
### Review ("Brush up on X" / topic has confidence: partial)

Activated when the user asks to review, or when the topic appears in their `partial_topics` list.

**This is NOT teaching from scratch.** The user has been exposed to this concept. Your job is to:
1. Acknowledge what they already know (read the `note` field from `partial_topics`)
2. Fill the specific gap identified in the note
3. Assign a targeted hands-on exercise to cement the missing piece
4. Keep it short — this should take 1/3 the time of a full explain session

Example for `{ topic: "flexbox", note: "knows concept, hasn't built layouts" }`:
- Skip: "Flexbox is a CSS layout model..." (they know this)
- Do: "You know what flexbox does — let's put it to work. Open your editor and build this layout: [specific exercise]. Key things to notice while you do it: [2-3 specific gaps to fill]."

If `build-then-learn` is their learning mode, lead with the exercise. If `theory-first`, fill the conceptual gap first, then exercise.

After successful completion, suggest: "That clicks now? Want me to mark flexbox as solid in your profile?"
```

- [ ] **Step 2: Add Misconception Correction mode**

Add after the Review mode:

```markdown
### Correct ("Fix my understanding of X" / topic has misconception flag)

Activated when the user asks about a topic flagged in their `misconceptions` list, or when you encounter the misconception during another teaching mode.

**Approach:**
1. State what they currently believe (from the `note` field): "You mentioned that [their belief]."
2. Explain why it's a reasonable thing to think — don't make them feel stupid.
3. Present the correct model clearly and concisely.
4. Give a concrete example that demonstrates why the correct model works and the misconception doesn't.
5. Quick check: ask them to explain it back in their own words.

**Tone:** Matter-of-fact, not condescending. "Easy mistake — here's what actually happens" not "That's wrong, let me correct you."

After they demonstrate correct understanding: "Got it — want me to clear that flag from your profile?"
```

- [ ] **Step 3: Update the Startup section to load new fields**

Modify the Startup section (line 12-18). Add to the list of things to load:

```markdown
   - Their `partial_topics` (topics to review, not re-teach)
   - Their `misconceptions` (topics to correct gently)
   - Their `learning_path` (to understand where this topic fits in their goals)
```

- [ ] **Step 4: Update Fallback Behavior to check topic classification**

Add before the existing fallback section (before line 74):

```markdown
## Topic Classification Check

Before teaching any topic, check the user's profile for its classification:
1. If the topic is in `completed_topics` with `confidence: solid` → remind them they've covered this, offer a quick refresher only if asked
2. If the topic is in `partial_topics` → use **Review** mode, not Explain
3. If the topic is in `misconceptions` → use **Correct** mode
4. If the topic is not in any list → use the standard teaching modes (Explain, etc.)

This check happens automatically. Don't ask the user which mode — just use the right one.
```

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/tutor/SKILL.md
git commit -m "feat: add review mode and misconception correction to tutor skill"
```

---

### Task 6: Update the Existing Learner Profile

**Why:** The current `vault/learner-profile.md` uses the old schema (flat `completed_topics` list, no `partial_topics`, no `misconceptions`, no `learning_path`). It needs to be migrated to the new schema format so all skills can work with it consistently. Since this profile is Alex's existing profile (the developer), we migrate the data preserving everything.

**Files:**
- Modify: `vault/learner-profile.md`

- [ ] **Step 1: Update the profile to use the new schema**

Replace the entire file content with the migrated version. Note: `completed_topics` entries become objects with `confidence: solid`. Empty new fields are added.

```yaml
---
name: Alex
created: 2026-04-06

learning_style:
  input_mode: verbal-stream
  conceptual_approach: big-picture-first
  learning_mode: build-then-learn
  analogy_preference: cross-domain
  overwhelm_sensitivity: high
  momentum_style: burst

tutor_persona:
  name: "Jarvis"
  personality: direct-mentor
  verbosity: concise
  celebrate_progress: true
  use_cross_domain_analogies: true

domains:
  - name: "[[audio-engineering]]"
    skill_level: beginner
    equipment: ["[[Volt 476]]", "[[AT2035]]", "[[FL Key 37]]", "[[FL Studio]]"]
    goals: [live mixing, vocal recording, basic mastering]
    completed_topics: []
    partial_topics: []
    misconceptions: []
    current_focus: null
    queued_topics: []
    learning_path: []
  - name: "[[photography]]"
    skill_level: beginner
    equipment: ["[[Fujifilm X-T4]]", "[[Capture One Pro]]"]
    goals: [portrait editing, color grading, professional output]
    completed_topics: []
    partial_topics: []
    misconceptions: []
    current_focus: null
    queued_topics: []
    learning_path: []
  - name: "[[knowledge-management]]"
    skill_level: intermediate
    equipment: ["[[Obsidian]]"]
    goals: [Dataview mastery, automation, MIDI integration]
    completed_topics:
      - { topic: "basic vault setup", confidence: solid }
      - { topic: "YAML frontmatter", confidence: solid }
      - { topic: "tags", confidence: solid }
    partial_topics: []
    misconceptions: []
    current_focus: Dataview queries
    queued_topics: []
    learning_path: []

last_updated: 2026-04-06
---
```

- [ ] **Step 2: Commit**

```bash
git add vault/learner-profile.md
git commit -m "feat: migrate learner profile to extended schema with knowledge classification fields"
```

---

### Task 7: Update CLAUDE.md

**Why:** The project README needs to document the new skill and updated architecture.

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add onboarding skill to the Architecture section**

In the skill list under `## Architecture`, add after the `session-router` entry:

```markdown
- `onboarding` — First-time user setup and deep domain intake with knowledge distillation.
```

- [ ] **Step 2: Add onboarding to the Key Rules section**

Add to the Key Rules list:

```markdown
- First-time users are routed to `onboarding` automatically by `session-router`.
- `onboarding` is the only skill besides `learning-profile` that writes to `learner-profile.md` (during initial setup only).
- Domain intake classifies knowledge as solid/partial/misconception — tutor adapts mode accordingly.
```

- [ ] **Step 3: Update the Vault section**

Add under the vault file descriptions:

```markdown
- `vault/templates/learner-profile-template.md` — Schema template for new learner profiles
```

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add onboarding skill to project architecture documentation"
```

---

## Execution Order

Tasks 1-2 can run in parallel (template + skill have no dependencies).
Task 3 depends on Task 2 (session-router references onboarding skill).
Tasks 4 and 5 can run in parallel (learning-profile and tutor are independent).
Task 6 depends on Task 4 (profile schema must match what learning-profile expects).
Task 7 can run anytime after Task 2.

```
[Task 1] ──────────────────────────────┐
                                        ├──→ [Task 3] ──→ [Task 6] ──→ Done
[Task 2] ──────────────────────────────┘        │
                                                ├──→ [Task 7]
[Task 4] ──────────────────────────────────────┘
[Task 5] ──────────────────────────────────────┘
```
