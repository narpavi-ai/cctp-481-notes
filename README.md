# CCTP 481 Notes — Building Your First AI Agent

Hands-on lab notebooks for **CCTP 481**, a NAIT Continuing Education course.
This repo is referenced directly from the course slide deck — if a slide points
you here, you're in the right place.

**Who this is for:** business innovators and technical professionals.
**Python familiarity is recommended but not required** — every notebook can be
completed by reading the explanations and pressing ▶ in order. Nothing needs to
be installed; everything runs in your browser.

**Prerequisite:** [CCTP 480](https://github.com/narpavi-ai/cctp-480-notes). These
labs assume you already know *what* an agent is, the ReAct loop, and why
human-in-the-loop matters. Here you build all of it.

## What's in this repo

```
notebooks/     the four Colab labs - run these in order
n8n/           the same four labs as importable n8n workflows (no-code track)
images/        artwork the notebooks display
```

Each lab exists **twice**: once as a notebook you run in Colab, once as a
workflow you import into n8n. They build the same agent. Pick the track you're
comfortable in, or follow both — [the mapping is below](#no-code-track--the-same-four-labs-on-a-canvas).

## The four labs

Run them in order — each one starts where the last finished.

| Lab | Notebook | What you build | Module |
|---|---|---|---|
| 1 | [`01-hello-model.ipynb`](notebooks/01-hello-model.ipynb) | Your first model call from code — messages, roles, no memory, and the two gaps the rest of the course closes | 1 |
| 2 | [`02-first-agent.ipynb`](notebooks/02-first-agent.ipynb) | A real agent: live Edmonton weather and your stock, the ReAct loop traced step by step, and a runaway safety belt | 2 |
| 3 | [`03-tools-data-memory.ipynb`](notebooks/03-tools-data-memory.ipynb) | Memory that survives the conversation, and an agent that quotes *your* handbook instead of guessing | 3 |
| 4 | [`04-oversight-evaluation.ipynb`](notebooks/04-oversight-evaluation.ipynb) | Approval gates, guardrails the model can't argue past, and evidence about whether your agent is any good | 4 |

**Opening a notebook in Colab:** click the notebook above, then click the
**Open in Colab** badge — or go to [colab.research.google.com](https://colab.research.google.com),
choose **GitHub**, and paste this repo's URL.

## Before day one — 3 minutes

Please do this **the day before class**, not weeks early.

1. **Get a free API key.** Go to [Google AI Studio](https://aistudio.google.com/apikey),
   sign in with any Google account, click **Create API key**. No credit card.
   The labs use **`gemini-3.5-flash-lite`** — if you hit a `404 NOT_FOUND` saying a
   model is no longer available, that's Google retiring it, not your mistake:
   check AI Studio for a current model and change the one `MODEL` string.
2. **Store it in Colab.** Open any notebook above, click the **🔑 key icon** in
   the left sidebar → **Add new secret** → name it exactly `GOOGLE_API_KEY`,
   paste the value, and turn **Notebook access** on.

   **You do this once per notebook, not once per account.** *Notebook access*
   is granted to the specific notebook you are looking at, so when you open
   Lab 2 you will be asked to grant it again — and if you skip it, the setup
   cell falls through to a `getpass` prompt asking you to paste the key by
   hand. That prompt is safe (it hides what you type and never writes the key
   into the file), but the key icon is the habit worth keeping.

   You will also see **"Warning: This notebook was not authored by Google"**
   the first time you run each lab. That is Colab telling you the notebook came
   from GitHub, which it did. Click **Run anyway**.
3. **Create an [n8n](https://n8n.io) account** for the no-code half of the
   course. The trial is **14 days** and needs no credit card — but **start it
   the day before class**, not earlier, so it doesn't expire mid-course.
   Full walkthrough: **[`n8n/SETUP.md`](n8n/SETUP.md)**.

> ⚠️ **Use made-up data in these labs.** The free tier of the Gemini API uses
> your prompts to improve Google's products (the paid tier does not), and n8n's
> trial is a third-party cloud service. **Personal projects and public or
> invented data only** — nothing confidential, nothing about a real customer,
> nothing under NDA. That's why the whole course runs on a food truck that
> doesn't exist. We come back to why this matters in Module 4.

## The running example — let's say you own a food truck

You park it in Edmonton's river valley — **Hawrelak Park** on weekends,
**Louise McKinney** when there's something on downtown, the **Old Strathcona
Farmers' Market** on Saturdays. You sell cinnamon buns, saskatoon berry pie,
bison chili and cold brew.

Every morning you answer the same three questions:

> **What's the weather doing? What have I got left? Do I open today?**

Every lab ends by asking the agent the same one — *"should I open at Hawrelak
today?"* — and getting a better answer than the lab before:

| Lab | You add | It says |
|---|---|---|
| 1 | just a model | *"I don't have access to real-time weather data."* |
| 2 | live weather + your stock | *"Feels like −24 °C. You have 4 cinnamon buns."* — real facts, but it still **guesses** the decision |
| 3 | your handbook + memory | *"Don't open — your policy says no service below −20 °C."* |
| 4 | approval gates + guardrails | *"Don't open. Want me to order flour instead?"* — and it **waits for you** before spending |

One business for the whole course, so you're never learning a new domain and a
new concept at the same time.

## No-code track — the same four labs, on a canvas

Every lab here exists twice. The [`n8n/`](n8n/) directory holds an importable
workflow for each notebook, building the same agent on the same bakery:

| Lab | Notebook | n8n workflow |
|---|---|---|
| 1 | [`01-hello-model.ipynb`](notebooks/01-hello-model.ipynb) | [`n8n/01-hello-model.json`](n8n/01-hello-model.json) |
| 2 | [`02-first-agent.ipynb`](notebooks/02-first-agent.ipynb) | [`n8n/02-first-agent.json`](n8n/02-first-agent.json) |
| 3 | [`03-tools-data-memory.ipynb`](notebooks/03-tools-data-memory.ipynb) | [`n8n/03-tools-data-memory.json`](n8n/03-tools-data-memory.json) |
| 4 | [`04-oversight-evaluation.ipynb`](notebooks/04-oversight-evaluation.ipynb) | [`n8n/04-oversight-evaluation.json`](n8n/04-oversight-evaluation.json) |

[**n8n/README.md**](n8n/README.md) has the import steps and a line-by-line
mapping between the Python and the canvas — `@tool` ↔ Code Tool,
`checkpointer` ↔ Simple Memory, `recursion_limit` ↔ Max Iterations.

n8n's AI nodes are named `@n8n/n8n-nodes-langchain.*` because they **are**
LangChain. One caveat, worth knowing before you notice it yourself: n8n
implements LangChain's **JavaScript** framework, so the concepts map exactly
but the code does not.

**Export your workflow JSON before the trial ends.** It imports cleanly into a
free [self-hosted n8n](https://docs.n8n.io/hosting/), so what you build in class
keeps working afterwards at no cost.

## Rate limits — the one number that matters

The free tier is generous about *money* and strict about *requests*. Check
**[your own limits](https://aistudio.google.com/rate-limit)** — they vary by
account — but as of **23 August 2026** the free tier looked like this:

| Model | Requests/min | Tokens/min | **Requests/day** |
|---|---|---|---|
| Gemini 3.7 / 3.6 / 3.5 **Flash** | 5 | 250K | **20** |
| Gemini 3.5 / 3.1 **Flash Lite** | 15 | 250K | **500** |

**These four labs need roughly 70 requests**, because every step an agent takes
is another request — a single question that calls two tools costs three.

That is why the labs pin **`gemini-3.5-flash-lite`** rather than the more
capable Flash. Twenty requests a day would strand you partway through Lab 2,
and the daily count resets at midnight Pacific, so there is no way back in.

**Choosing a model on quota rather than on capability is a real engineering
decision** — the same one you'd make sizing a production agent. If your key has
higher limits, or you add billing, change the one `MODEL` string and carry on.

## Costs

Nothing in this course costs money.

| | |
|---|---|
| Google Colab | Free tier |
| Gemini API | Free tier, no credit card |
| n8n | Free trial in class; free self-hosting afterwards |

If Google is unavailable to you, [Groq](https://console.groq.com) and
[Cerebras](https://cloud.cerebras.ai) also issue free keys without a card —
change one string in the notebook and continue.

## Versions these labs were tested against

Last verified **2026-08-23** against `langchain` 1.3.16, `langgraph` 1.2.11 and
`langchain-google-genai` 4.3.5, on model **`gemini-3.5-flash-lite`**. The install
cells pin below the next major (`langchain>=1.3,<2`) so a v2 release cannot
break a class mid-session.

If an import fails, that pin is the first thing to check. If a *model call*
fails with a 404, the model name is the first thing to check — Google retires
them on their own schedule, and `gemini-2.5-flash` stopped accepting new users
partway through this course's preparation.

The weather tool uses [Open-Meteo](https://open-meteo.com), which needs **no API
key** for non-commercial use — so no student is ever blocked on a second signup.

**The n8n workflows were imported and run on a live n8n Cloud instance on
2026-08-23** — all four, from this repo's `main`, against a real key. See
[`n8n/README.md`](n8n/README.md) for what each one was asked and what it said.
The Colab notebooks are API-verified and their tools have been executed, but no
notebook has yet been run end to end against a live key.

## References used across this repo

**LangChain / LangGraph — the framework taught in this course**

- [LangChain Python docs](https://docs.langchain.com/oss/python/langchain/overview)
- [LangGraph Python docs](https://docs.langchain.com/oss/python/langgraph/overview)
- [Quickstart](https://docs.langchain.com/oss/python/langchain/quickstart) ·
  [Agents](https://docs.langchain.com/oss/python/langchain/agents) ·
  [Tools](https://docs.langchain.com/oss/python/langchain/tools)
- [Short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory) ·
  [Long-term memory](https://docs.langchain.com/oss/python/langchain/long-term-memory) ·
  [Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval)
- [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) ·
  [Guardrails](https://docs.langchain.com/oss/python/langchain/guardrails) ·
  [Agent Evals](https://docs.langchain.com/oss/python/langchain/test/evals)
- [LangChain Academy](https://docs.langchain.com/oss/python/langchain/academy) — free, for after the course

**Wider reading the course draws on**

- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI — A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [Sierra — τ-bench](https://sierra.ai/blog/benchmarking-ai-agents) · [paper](https://arxiv.org/pdf/2406.12045)
- [Simon Willison — The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)

**Tools**

- [Google AI Studio](https://aistudio.google.com) · [Gemini models](https://ai.google.dev/gemini-api/docs/models) · [pricing](https://ai.google.dev/gemini-api/docs/pricing) · [rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Open-Meteo](https://open-meteo.com/en/docs) — the free, keyless weather API the labs call
- [n8n docs — AI components](https://docs.n8n.io/build/integrate-ai/understand-ai-components/) · [self-hosting](https://docs.n8n.io/hosting/)

---

*Generated with AI assistance as part of course prep; may contain errors —
verify against the linked official docs before relying on anything technical.*
