# Setting up n8n — 10 minutes, the day before class

This is the no-code half of CCTP 481. You'll do the same four labs as the
Colab notebooks, on a canvas instead of in Python.

> ⏰ **Do this the day before class, not weeks early.** The n8n trial is
> **14 days**. Start it too soon and it expires halfway through the course.

---

## 1. Create the account

1. Go to **[n8n.io](https://n8n.io)** and click **Get Started** (top right).
2. Enter your email and set a password.
3. You'll land on a page offering a **Start free 14-day trial** button. Click it.

> ⚠️ **This is a trial account for learning. Treat it that way.**
>
> Exactly the same rule as the Gemini free tier: **no company data, no real
> customer records, nothing confidential, nothing under NDA.** Everything in
> these labs uses a made-up food truck on purpose. You are putting data into a
> third-party cloud service on a free trial — that is fine for cinnamon buns
> and not fine for anything real.

4. When you see **"Your workspace is ready!"**, click **Start automating**.

You'll see a banner in the top-left corner showing days remaining and
executions used — something like `14 days left · 0/1000 executions`. That's
your budget for the whole course. It's plenty; the labs use a handful.

---

## 2. Add your Gemini API key as a credential

You need the **same** Google AI Studio key you put into Colab. If you don't
have one yet, get it first: <https://aistudio.google.com/apikey> → **Create
API key**. Free, no credit card.

An n8n **credential** is a saved secret that any workflow can use. You create
it once and every lab reuses it.

1. In the left sidebar, click **Overview**.
2. Click the **Credentials** tab.
3. Click **Create credential** (orange button, top right).
4. In the search box type **`Google Gem`**.
5. Choose **`Google Gemini(PaLM) Api`** — that exact one. *(The "PaLM" in the
   name is historical. It is the Gemini credential.)*
6. Fill in:
   - **Host** — leave it as `https://generativelanguage.googleapis.com`
   - **API Key** — paste your AI Studio key
7. Click **Save**.

> **Why the workflow files don't already contain this.** A credential is a
> secret tied to *your* n8n instance, with an ID that means nothing in anyone
> else's. Shipping one in a public repo would publish the key. The workflows
> carry an empty credential slot instead — you point it at the one you just
> made, once, and it sticks.

---

## 3. Import a lab

Each lab is one `.json` file in this directory. Download it first
(**Raw** → save), then:

1. Click **Personal** in the left sidebar.
2. Click **Create workflow**.
3. Click the **⋯** menu at the top of the canvas.
4. Choose **Import** → **From file…**
5. Pick the `.json` for the lab you're on.

The canvas fills in with the nodes and a **sticky note** explaining what to try.
**Read the sticky before you run anything** — it has the exact questions to ask
and what to compare against the notebook.

---

## 4. Connect the credential and chat

1. Open the **Google Gemini Chat Model** node (double-click it).
2. In **Credential to connect with**, pick the credential you made in step 2.
3. Close the node.
4. Click **Chat** at the bottom of the canvas.
5. Ask it the questions from the sticky note.

To see what actually happened — which tool the agent chose, what came back —
open the **Logs** panel at the bottom. That's n8n's version of the notebook's
`show_trace()`, and it's where the real learning is.

---

## The four labs

| Lab | Workflow | Notebook twin |
|---|---|---|
| 1 | [`01-hello-model.json`](01-hello-model.json) | [`01-hello-model.ipynb`](../notebooks/01-hello-model.ipynb) |
| 2 | [`02-first-agent.json`](02-first-agent.json) | [`02-first-agent.ipynb`](../notebooks/02-first-agent.ipynb) |
| 3 | [`03-tools-data-memory.json`](03-tools-data-memory.json) | [`03-tools-data-memory.ipynb`](../notebooks/03-tools-data-memory.ipynb) |
| 4 | [`04-oversight-evaluation.json`](04-oversight-evaluation.json) | [`04-oversight-evaluation.ipynb`](../notebooks/04-oversight-evaluation.ipynb) |

[**README.md**](README.md) has the line-by-line mapping between the Python and
the canvas.

---

## Before your trial ends

**Export every workflow you care about.** Open it, **⋯** → **Export JSON**, and
save the file.

Those files import cleanly into a free
[self-hosted n8n](https://docs.n8n.io/hosting/), so what you build in class
keeps working afterwards at no cost.

---

## If something breaks

| What you see | Fix |
|---|---|
| The Gemini node has a red triangle | No credential selected. Open it and pick the one from step 2 |
| `401` / `API key not valid` | The key in the credential is wrong, or has a stray space. Re-paste it |
| `404` / *model not found* | Google retired the model. Open the Gemini node, and pick a current model from the dropdown |
| **Import** is greyed out | You're on the workflow *list*, not inside a workflow. Create one first, then use its ⋯ menu |
| The agent answers without using a tool | Open the tool node and strengthen its **Description** — that field is the prompt the model reads |
| Lab 4 never asks for approval | The Chat Trigger's **Response Mode** must be **Using Response Nodes** |
| **Get Weather** errors | It calls Open-Meteo with no key. Check the URL in the node, and that your network allows it |
| `Executions` count stuck at the limit | You've used the trial's 1,000. Export your workflows and self-host |

---

*Generated with AI assistance as part of course prep; may contain errors —
verify against the linked official docs before relying on anything technical.*
