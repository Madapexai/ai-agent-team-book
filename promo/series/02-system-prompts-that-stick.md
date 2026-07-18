<!--
dev.to — Part 2/5
Title: System Prompts That Actually Stick (Most Fail for One Reason)
Tags:  ai, agents, llm, tutorial
-->

# System Prompts That Actually Stick (Most Fail for One Reason)

Most System Prompts fail for the same reason: they're written as **instructions** when they should be written as an **attention-allocation strategy**.

You can tell an agent "be careful and thorough" a hundred times. It won't stick, because "careful" isn't an operable behavior — it's a vibe. A System Prompt that works tells the agent *where to spend its attention, in what order, and what to never do* even when you're not looking.

This is Part 2 of a 5-part series adapted from a free, 21-chapter handbook on building agent teams that actually work.

## 1. Separate "who you are" from "how you work"

A common mistake is cramming identity, rules, examples, and edge cases into one wall of text. Structure it instead:

- **Role** — one sentence on what the agent *is* and who it serves.
- **Operating principles** — the 3–5 rules it falls back on when ambiguous.
- **Hard constraints** — the things it must never do (e.g., "never load more than 6000 tokens of context at once").
- **Escalation** — what to do when stuck ("after 3 consecutive failures, stop and report").

The constraint line above isn't trivia: in the book's cost-control chapter, infinite-loop retries were measured at ~60% of *non-productive* spend. A single "stop after 3 failures" rule is the cheapest insurance you'll ever write.

## 2. Make the prompt survivable across sessions

Agents don't remember yesterday unless you give them memory. So the System Prompt should point at external memory, not try to contain everything:

- Reference a `knowledge/` and `skills/` directory the agent searches *before* calling the model.
- Keep the prompt short enough to re-read every session without drift.

The book's numbers: ~45% of questions an agent faces already have an answer in existing skill files. A prompt that says "search memory first" turns that into free, fast wins.

## 3. Allocate attention, don't dictate steps

Instead of scripting every step, allocate attention:

> "Spend most of your effort on the risky 20% of the task. Delegate translation/formatting to the cheap model. Load context in batches by relevance — never all at once."

This is the difference between an agent that *follows* and an agent that *thinks like a subordinate who gets the intent.*

## 4. Version it like code

Your System Prompt is a piece of infrastructure. Treat it that way: keep it in a file, diff changes, and roll back when behavior regresses. The book walks through a real role-declaration example and a refactor accident that proved why isolation between agents' prompts matters.

---

Next: memory systems and communication protocols — how to stop four agents from holding three different "truths" (Part 3).

👉 **Full playbook, free (中文/English):** https://github.com/Madapexai/ai-agent-team-book
⭐ Star it if you're building an agent team.

*Adapted from "Being the Boss of AI: Agent Combat Team" by Yason (MindApex · VokoForge), MIT Licensed.*
