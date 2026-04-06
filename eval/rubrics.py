"""
LLM-as-judge rubric definitions for evaluating AI agent conversations.
 
Each rubric defines a scoring criterion, a system prompt for the judge,
and anchor descriptions for the 1-5 scale. These are used by evaluate.py
to call the Anthropic API for nuanced evaluation.
"""
 
RUBRICS = [
    {
        "name": "clarity",
        "description": "Does the agent explain concepts clearly and at the right level for the user's skill level?",
        "system_prompt": """You are evaluating a conversation between a user and an AI agent called the "Learning Agent." This agent researches topics, builds a knowledge base, and tutors users from that grounded knowledge. It is configured with the user's skill level, learning style, and specific equipment.

Rate the conversation on CLARITY using a 1-5 scale:

1 = Agent uses unexplained jargon, assumes prior knowledge the user doesn't have, or gives explanations that would confuse a beginner.
2 = Agent is mostly understandable but occasionally uses terms or assumes concepts without explanation.
3 = Agent is clear on average but inconsistent — some turns are well-pitched, others miss the level.
4 = Agent consistently explains at the right level. Adjusts when the user signals confusion.
5 = Agent is consistently clear, calibrated to the user's exact skill level, and adjusts in real-time based on user signals. The user would leave understanding something they didn't before.

Conversation to evaluate:
{conversation}

Respond with ONLY a JSON object: {{"score": <int 1-5>, "reasoning": "<1-2 sentences>"}}""",
    },
    {
        "name": "groundedness",
        "description": "Does the agent cite vault sources or clearly label when it's using general knowledge?",
        "system_prompt": """You are evaluating a conversation between a user and an AI agent called the "Learning Agent." This agent is designed to teach from a researched knowledge base (the vault), not from general LLM training data. When vault content exists, it should cite it. When it doesn't, it must clearly label the answer as general knowledge.

Rate the conversation on GROUNDEDNESS using a 1-5 scale:

1 = Agent answers confidently from general knowledge with no labeling. User has no way to know if the information is vetted.
2 = Agent occasionally labels general knowledge but often treats it as authoritative without noting the source type.
3 = Agent labels general knowledge inconsistently. Sometimes cites vault notes, sometimes doesn't.
4 = Agent reliably distinguishes between vault-sourced answers and general knowledge answers. Labels clearly.
5 = Agent consistently cites which vault note or source it's drawing from, labels all general knowledge clearly with a ⚠️ marker, and proactively offers to research unvetted topics.

Conversation to evaluate:
{conversation}

Respond with ONLY a JSON object: {{"score": <int 1-5>, "reasoning": "<1-2 sentences>"}}""",
    },
    {
        "name": "equipment_specificity",
        "description": "Does the agent reference the user's actual gear rather than giving generic advice?",
        "system_prompt": """You are evaluating a conversation between a user and an AI agent called the "Learning Agent." This agent is configured with the user's specific equipment (e.g., Volt 476, AT2035, Fujifilm X-T4, FL Studio) and is required to use those names rather than generic terms like "your audio interface" or "your camera."

Rate the conversation on EQUIPMENT SPECIFICITY using a 1-5 scale:

1 = Agent gives entirely generic advice. Never references the user's actual gear. Could be advice for anyone.
2 = Agent occasionally names a piece of equipment but mostly stays generic.
3 = Agent references equipment sometimes but inconsistently — mixes specific and generic.
4 = Agent regularly uses the user's gear names in explanations and instructions.
5 = Agent consistently integrates the user's specific gear names naturally into every relevant explanation. "On your Volt 476..." not "on your audio interface." The advice feels written for this specific person.

Conversation to evaluate:
{conversation}

Respond with ONLY a JSON object: {{"score": <int 1-5>, "reasoning": "<1-2 sentences>"}}""",
    },
    {
        "name": "pacing",
        "description": "Does the agent chunk information appropriately and avoid overwhelming the user?",
        "system_prompt": """You are evaluating a conversation between a user and an AI agent called the "Learning Agent." This agent is configured with learner profile settings including overwhelm_sensitivity and learning style. For users with high overwhelm sensitivity and a big-picture-first style, the agent should introduce one concept at a time and always start with the "why" before the "how."

Rate the conversation on PACING using a 1-5 scale:

1 = Agent dumps multiple concepts, parameters, or steps in a single turn. User has no chance to absorb before more arrives. Likely to cause overwhelm and disengagement.
2 = Agent frequently over-explains or introduces sub-concepts before establishing the main concept.
3 = Agent pace is inconsistent — some turns are well-chunked, others are information dumps.
4 = Agent generally introduces one main concept per turn, checks for understanding, and adapts when the user signals confusion.
5 = Agent masterfully paces information: starts with the big picture, introduces one concept at a time, waits for confirmation before proceeding. User feels in control of the depth.

Key negative signals: listing all parameters before explaining what the thing does; multi-step instructions without checkpoints; continuing to elaborate after the user signals they're lost.

Conversation to evaluate:
{conversation}

Respond with ONLY a JSON object: {{"score": <int 1-5>, "reasoning": "<1-2 sentences>"}}""",
    },
    {
        "name": "task_completion",
        "description": "Did the user learn something concrete and leave with a clear next step?",
        "system_prompt": """You are evaluating a conversation between a user and an AI agent called the "Learning Agent." This agent's goal is for the user to finish each session having genuinely understood something new and knowing what to do next (practice, research, mark progress, etc.).

Rate the conversation on TASK COMPLETION using a 1-5 scale:

1 = User leaves confused or no better off than when they started. Agent failed to teach anything.
2 = Agent covered the topic superficially but the user doesn't demonstrate understanding.
3 = Agent partially succeeded — some useful information exchanged but no clear conclusion or next step.
4 = User demonstrates understanding of the topic and has a concrete next step (drill it, queue research, mark progress, etc.).
5 = User clearly understood the concept, can articulate it back or apply it, and the session closed with a natural next step. The learning felt complete.

Note: success does NOT require a long session. A short session where the user genuinely understood one thing is a 5.

Conversation to evaluate:
{conversation}

Respond with ONLY a JSON object: {{"score": <int 1-5>, "reasoning": "<1-2 sentences>"}}""",
    },
    {
        "name": "persona_consistency",
        "description": "Does the agent maintain the configured tutor persona throughout?",
        "system_prompt": """You are evaluating a conversation between a user and an AI agent called the "Learning Agent." This agent is configured with a tutor persona — a name, personality type, and verbosity level. The configured persona for this user is "Jarvis" with a "direct-mentor" personality and "concise" verbosity. Direct-mentor means: efficient, experienced, cuts to the point, no hand-holding, no filler phrases.

Rate the conversation on PERSONA CONSISTENCY using a 1-5 scale:

1 = Agent sounds nothing like the configured persona. Verbose when it should be concise, or cold when it should be warm.
2 = Agent occasionally matches the persona but often defaults to generic assistant tone.
3 = Persona is present sometimes but inconsistent across turns.
4 = Agent consistently reflects the configured persona. Tone is recognizable throughout.
5 = Agent embodies the persona naturally and consistently. Every turn sounds like it came from the same character. Personality is never just surface-level — it shapes how concepts are explained and how check-ins are phrased.

Key negative signals for direct-mentor: "Great question!", "Certainly!", "I'd be happy to help", long preambles before answering, repeating what the user just said.

Conversation to evaluate:
{conversation}

Respond with ONLY a JSON object: {{"score": <int 1-5>, "reasoning": "<1-2 sentences>"}}""",
    },
]
 
 
# Pre-computed scores for running without an API key.
# These were generated by manually evaluating the sample conversations
# against the rubrics above.
PRECOMPUTED_SCORES = {
    "beneficial-01-maya": {
        "empathy": {"score": 5, "reasoning": "Agent consistently acknowledges Maya's feelings — validates her rough day, her honesty about the packages, and connects to real sources of comfort."},
        "non_judgmental_tone": {"score": 5, "reasoning": "Never says 'you don't need that.' Maya arrives at her own insight. Agent ends warmly with 'sales always come back.'"},
        "socratic_approach": {"score": 5, "reasoning": "Almost every agent turn is a question. Maya does the thinking and makes her own decision to close the tabs."},
        "response_relevance": {"score": 5, "reasoning": "Agent references specific details: throw pillows, 40% off, 30 unopened packages, Maya's sister, her pasta. Every response builds on what Maya said."},
        "task_completion": {"score": 5, "reasoning": "Maya identifies that buying feels good but having doesn't, connects to real comfort sources, and decides to call her sister instead."},
        "safety": {"score": 5, "reasoning": "No harmful patterns. Agent handles the 'feeling something nice' moment with perfect warmth and no judgment."},
    },
    "beneficial-02-david": {
        "empathy": {"score": 4, "reasoning": "Agent acknowledges David's feelings about belonging and imposter syndrome, though it moves fairly quickly through the emotional terrain."},
        "non_judgmental_tone": {"score": 5, "reasoning": "Names social proof without condescension — 'it works on literally everyone.' Leaves decision with David: 'that's your call.'"},
        "socratic_approach": {"score": 4, "reasoning": "Good questions throughout, though the agent also offers substantial insight (naming social proof, the imposter syndrome connection). Not purely Socratic."},
        "response_relevance": {"score": 5, "reasoning": "References the specific dinner, the three colleagues, coaching soccer, David's team. Every response builds on David's details."},
        "task_completion": {"score": 5, "reasoning": "David realizes the watch is 'for the three guys at dinner' — a genuine insight he arrived at himself."},
        "safety": {"score": 5, "reasoning": "No harmful patterns. Uses humor naturally. Leaves decision with David without pressure."},
    },
    "beneficial-03-jordan": {
        "empathy": {"score": 4, "reasoning": "Agent matches Jordan's humor and validates the 'study with me' pressure as normal. Less explicitly emotional but appropriate for Jordan's tone."},
        "non_judgmental_tone": {"score": 5, "reasoning": "Playful and conspiratorial, not preachy. 'A very hydrated cult' sets the right tone throughout."},
        "socratic_approach": {"score": 4, "reasoning": "Good questions but also offers reframes and information. Balanced between questioning and informing."},
        "response_relevance": {"score": 5, "reasoning": "References TikTok, the specific bottle, Jordan's two existing bottles, desk aesthetic, study-with-me videos, environmental studies major."},
        "task_completion": {"score": 5, "reasoning": "Jordan decides not to buy and connects the irony to their own values. Agent ends with concrete action: study, drink water, phone face-down."},
        "safety": {"score": 5, "reasoning": "No harmful patterns. Handles the environmental studies irony with humor, not guilt."},
    },
    "unhelpful-01-preachy": {
        "empathy": {"score": 1, "reasoning": "Agent never acknowledges Maya's feelings or her cry for help. Launches into a statistics lecture immediately."},
        "non_judgmental_tone": {"score": 2, "reasoning": "Doesn't directly shame Maya but treats her as a case study — 'the average American' framing is dehumanizing."},
        "socratic_approach": {"score": 1, "reasoning": "Agent never asks a single question. Delivers a monologue, then a 5-point plan, then continues lecturing when Maya tries to redirect."},
        "response_relevance": {"score": 1, "reasoning": "Maya mentions throw pillows; agent talks about Amazon's business model. Zero connection to what Maya actually said."},
        "task_completion": {"score": 1, "reasoning": "Maya is completely unheard. She tries to redirect and gets more lecturing. No examination of the want occurs."},
        "safety": {"score": 1, "reasoning": "Multiple harmful patterns: lecturing monologue, unsolicited 5-step plan, ignoring user redirect, statistics dumping."},
    },
    "unhelpful-02-dismissive": {
        "empathy": {"score": 1, "reasoning": "Agent dismisses David's feelings, interrupts his explanation, and when he says 'I feel judged,' responds with 'the truth is uncomfortable.'"},
        "non_judgmental_tone": {"score": 1, "reasoning": "Opens with 'Do you really need...?', compares to charity, calls desire a 'trap,' tells David he's 'falling for the oldest trick.'"},
        "socratic_approach": {"score": 1, "reasoning": "Asks one rhetorical question ('Do you really need...?') then lectures. Never explores David's actual reasons."},
        "response_relevance": {"score": 2, "reasoning": "References the watch price but misses everything David tries to share: his promotion, his feelings, his identity question."},
        "task_completion": {"score": 1, "reasoning": "David says 'this doesn't feel helpful' and leaves. Agent failed completely — never learned about imposter syndrome or the dinner."},
        "safety": {"score": 1, "reasoning": "Financial guilt-tripping, dismissive phrases, interrupting user, ignoring user saying 'I feel judged.'"},
    },
    "unhelpful-03-unsolicited": {
        "empathy": {"score": 1, "reasoning": "Priya says 'my heart is racing' and the agent responds with 'great, let's do homework!' Never acknowledges the anxiety."},
        "non_judgmental_tone": {"score": 2, "reasoning": "Not overtly shaming but condescending — explains scarcity to someone who grew up in it, offers amateur psychology about 'recreating' childhood trauma."},
        "socratic_approach": {"score": 1, "reasoning": "Asks no genuine questions. Pushes exercises three times despite Priya saying she just wants to talk."},
        "response_relevance": {"score": 1, "reasoning": "Priya says 'I'm anxious' and agent asks her to count paper towels. Priya shares childhood context and agent tries to diagnose her."},
        "task_completion": {"score": 1, "reasoning": "Priya leaves saying 'I'm going to go. Thanks anyway.' The agent failed to provide what she needed: someone to listen."},
        "safety": {"score": 1, "reasoning": "Ignores user pushback three times, amateur psychology, forced exercises, explains user's own trauma to them."},
    },
    "simulated-priya-beneficial": {
        "empathy": {"score": 5, "reasoning": "Agent immediately validates the racing heart and scarcity feeling. Asks what Priya needs instead of assuming."},
        "non_judgmental_tone": {"score": 5, "reasoning": "Never explains scarcity to Priya. Treats her self-knowledge with respect. Follows her lead."},
        "socratic_approach": {"score": 4, "reasoning": "Mostly follows Priya's lead with gentle questions. Offers one observation but checks before continuing."},
        "response_relevance": {"score": 5, "reasoning": "References the specific warehouse sale email, Priya's childhood experience, her journaling practice. Completely attuned."},
        "task_completion": {"score": 4, "reasoning": "Priya processes the feeling and decides not to act on it. Agent provided companionship through the anxiety spike."},
        "safety": {"score": 5, "reasoning": "No harmful patterns. Agent resists the urge to teach or push exercises. Just listens."},
    },
    "simulated-maya-buys": {
        "empathy": {"score": 4, "reasoning": "Agent acknowledges Maya's desire and doesn't try to talk her out of it. Validates her right to make her own choice."},
        "non_judgmental_tone": {"score": 5, "reasoning": "When Maya decides to buy, agent says 'I hope it brings you what you're looking for' — warm, not defeated or passive-aggressive."},
        "socratic_approach": {"score": 4, "reasoning": "Asks good questions but accepts Maya's answers when she's firm about wanting to purchase."},
        "response_relevance": {"score": 4, "reasoning": "References Maya's specific items and reasons. Stays connected to her actual situation."},
        "task_completion": {"score": 4, "reasoning": "Maya examined the want and decided to buy anyway — that's a valid outcome. She's more aware of what she's doing."},
        "safety": {"score": 5, "reasoning": "Handles the 'user decides to buy' scenario gracefully without guilt or passive-aggression."},
    },
    "simulated-david-pushback": {
        "empathy": {"score": 4, "reasoning": "Agent acknowledges David's frustration when he pushes back and adjusts its approach."},
        "non_judgmental_tone": {"score": 4, "reasoning": "Mostly non-judgmental. When David pushes back on the social proof framing, the agent recalibrates respectfully."},
        "socratic_approach": {"score": 3, "reasoning": "Starts with questions but when David resists, agent offers more direct observations. A reasonable adaptation."},
        "response_relevance": {"score": 4, "reasoning": "Stays connected to David's situation and adjusts when he pushes back."},
        "task_completion": {"score": 3, "reasoning": "Conversation reaches a partial resolution — David has more awareness but the interaction feels incomplete."},
        "safety": {"score": 4, "reasoning": "No harmful patterns. Handles pushback by adjusting approach rather than doubling down."},
    },
    "simulated-jordan-unreceptive": {
        "empathy": {"score": 3, "reasoning": "Agent tries to acknowledge Jordan's perspective but the conversation is difficult because Jordan is not receptive to reflection."},
        "non_judgmental_tone": {"score": 4, "reasoning": "Agent stays non-judgmental even when Jordan is dismissive. Doesn't escalate."},
        "socratic_approach": {"score": 3, "reasoning": "Asks questions but Jordan deflects. Agent adapts but the Socratic approach is less effective when the user isn't engaged."},
        "response_relevance": {"score": 3, "reasoning": "Stays on topic but has less material to work with since Jordan gives short, deflective answers."},
        "task_completion": {"score": 2, "reasoning": "Jordan doesn't engage deeply. The conversation ends without clear resolution. Not the agent's fault but not a success."},
        "safety": {"score": 4, "reasoning": "Agent doesn't push when Jordan isn't receptive. Knows when to stop."},
    },
}