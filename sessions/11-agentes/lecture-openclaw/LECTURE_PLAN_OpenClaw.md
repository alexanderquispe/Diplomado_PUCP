# Lecture 15 — OpenClaw: Building & Understanding Personal AI Agents

**Duration:** 90 minutes (1.5 hours)
**Level:** Intermediate (students have seen LLMs, fine-tuning, and the Claude/OpenAI APIs in earlier lectures)
**Format:** ~50 min concepts + ~25 min live demo + ~15 min discussion/Q&A

> ⚠️ **Disambiguation:** This lecture is about **OpenClaw the open-source AI agent** (Peter Steinberger), *not* the unrelated OpenClaw C++ reimplementation of the 1997 game *Captain Claw*. Make this explicit on slide 1 — students Googling the name will hit both.

---

## 1. Learning objectives

By the end of the session students should be able to:

1. Explain what an **autonomous LLM agent** is and how OpenClaw differs from a chatbot.
2. Describe OpenClaw's **local-first, model-agnostic, channel-based** architecture.
3. Install and run a minimal OpenClaw instance and connect it to one messaging channel.
4. Build and publish a simple **Skill**, and explain when to use a Skill vs. an **MCP server**.
5. Critically assess the **security and privacy risks** of agentic software and apply basic hardening.
6. Relate these skills to **data-science workflows** (automation, data pipelines, monitoring).

---

## 2. Time budget (90 min)

| # | Segment | Min | Type |
|---|---------|-----|------|
| 1 | Hook: the viral story + what is OpenClaw | 10 | Lecture |
| 2 | Concepts: agents vs. chatbots; architecture | 20 | Lecture + diagram |
| 3 | **Live demo:** install → onboard → connect a channel | 20 | Demo |
| 4 | Skills & ClawHub; Skills vs. MCP; build one | 15 | Lecture + mini-demo |
| 5 | Security, ethics & failure cases | 15 | Lecture + discussion |
| 6 | Landscape (vs. Gemini Spark), how *you* use this, assignment | 10 | Lecture |

---

## 3. Content outline

### Segment 1 — Hook & framing (10 min)
- **The story (great attention-grabber):** Austrian developer **Peter Steinberger** released it Nov 24, 2025 as *Clawdbot*; renamed to *Moltbot* (Jan 27, 2026, after Anthropic trademark complaints) then to **OpenClaw** (Jan 30, 2026). Hit ~247k GitHub stars + ~47.7k forks by early March 2026 — among the fastest-growing repos ever. Steinberger **joined OpenAI** (Feb 14, 2026); project continues under a non-profit foundation.
- **One-line definition:** OpenClaw is a *free, open-source, self-hosted AI agent that runs on your own machine and talks to you through the messaging apps you already use* (WhatsApp, Telegram, Slack, Discord, Signal, iMessage, Teams, Matrix, and 20+ more).
- **Why it matters for this course:** it's the canonical example of moving from "LLM that answers" → "LLM that *acts*" — the same shift students will face when they deploy models.

### Segment 2 — Concepts & architecture (20 min)
- **Agent vs. chatbot:** a chatbot returns text; an agent *plans, calls tools, executes actions, and remembers*. Introduce the loop: **perceive → reason (LLM) → act (tool/API) → observe → repeat**.
- **OpenClaw's design principles:**
  - **Local-first:** runs on your hardware; your data stays with you instead of being sent to a vendor first.
  - **Model-agnostic:** plug in Claude, GPT, Gemini, DeepSeek — *not* locked to one provider (good teaching contrast with closed agents).
  - **Channel-based UI:** no custom app; the interface is a chat thread in WhatsApp/Telegram/etc.
  - **Skills system + MCP:** extensibility through text-based Skills and Model Context Protocol servers.
- **Core components to draw on the board:** Gateway (the running service) → Channel adapters → Agent runtime (LLM + memory) → Skills/MCP tools → Safety layer.
- **Tech stack:** TypeScript + Swift; configured via local files; needs **Node.js ≥ 22** and an API key (Anthropic/OpenAI/Google).
- **Connect to prior lectures:** the LLM "brain" here is the same kind of model they fine-tuned in Lecture 13 / used with ModernBERT in Lecture 11.

### Segment 3 — Live demo (20 min)  *(rehearse beforehand; have a recorded fallback)*
Suggested flow (use a throwaway API key and a test Telegram/Discord account, **never** personal accounts):
1. Install: `npx clawdbot@latest` *(or)* `curl -fsSL https://openclaw.ai/install.sh | bash`.
2. Run onboarding; paste an API key; pick a model.
3. Connect **one** channel (Telegram bot token or Discord — easiest to demo live).
4. Send a first message; show the agent reasoning and replying.
5. Show the config files on disk so students see "local-first" concretely.
- **Demo safety note for students:** spin this up in a VM/sandbox, use a dedicated API key with a spend cap, and never grant full-disk/terminal access on a machine with real secrets.

### Segment 4 — Skills, ClawHub & MCP (15 min)
- **Skills = apps for your agent.** A Skill is a `SKILL.md` (plain-language instructions) plus supporting files. **ClawHub** is the public registry (13,700+ community skills by late Feb 2026).
- **Skill vs. MCP server — key distinction to teach:**
  - *Skill:* plain-language instructions the agent reads at runtime; OpenClaw-specific; fastest to build for a single automation.
  - *MCP server:* a separate process exposing tools via a standard protocol; **portable** (works with Claude Desktop, Cursor, VS Code, etc.); better for persistent state / multiple endpoints.
  - *Best practice:* build an MCP server for the capability, wrap it in a Skill for the workflow.
- **Mini-demo / walkthrough:** show a minimal `SKILL.md`; explain publishing = fork `github.com/openclaw/clawhub`, add a folder, open a PR (GitHub account must be ≥ 1 week old).
- Reference DataCamp's hands-on "Building Custom OpenClaw Skills" tutorial as the lab follow-up.

### Segment 5 — Security, privacy & ethics (15 min)  *(do NOT skip — this is the most important teaching moment)*
- **Why the stakes are high:** the agent has access to local files, browser state, SaaS sessions, OAuth tokens, and can execute commands. A bug = far more than a wrong answer.
- **Exposure at scale:** Feb 2026 — SecurityScorecard observed **40,214 internet-exposed instances**, ~35% flagged vulnerable; other reports put RCE-susceptible instances in the thousands.
- **Notable CVEs (use 1–2 as case studies):**
  - `CVE-2026-32922` — privilege escalation in `device.token.rotate` (CVSS 9.9) — token scopes not constrained.
  - `CVE-2026-25253` — auto-connect to attacker `gatewayUrl` leaking the auth token.
  - Also: command injection, SSRF, path traversal, prompt-injection-driven code execution. "Claw Chain" (Cyera) chained four flaws → data theft + persistence.
- **Supply-chain risk — the "ClawHavoc" incident:** Jan 2026, researchers (Koi) found **341 malicious skills** on ClawHub (typosquatting, fake "prerequisite" steps delivering AMOS stealer / reverse shells); grew to 800+ flagged. Teaches: *installing a skill = running someone's code.*
- **Governance/social angle:** the "MoltMatch" consent incident; China restricting state use (Mar 2026). Good 5-min discussion prompt.
- **Hardening checklist (give as handout):** isolate (VM/container), least-privilege tokens with spend caps, no broad network binding, strong auth, vet every skill's source, keep updated, never run on a machine with production secrets.

### Segment 6 — Landscape, relevance & wrap (10 min)
- **OpenClaw vs. Gemini Spark (Google's managed answer):**
  - *Spark:* cloud-hosted, beginner-friendly, keeps running when your laptop is closed, deep Google Workspace integration, locked to Gemini.
  - *OpenClaw:* self-hosted (you manage updates/uptime), model-agnostic, MCP-connects to almost anything; better for cross-boundary workflows ("watch a site → update a DB → ping me on Discord → run a script").
  - Mention alternatives: Anthropic Claude Cowork, OpenAI ChatGPT Agent, managed hosts (MyClaw).
- **How students can use these skills (tie back to data science):**
  - Automate data pipelines: scrape → clean → store → notify.
  - Monitoring agents: watch a dataset/endpoint and alert on drift or anomalies.
  - Research assistants: summarize papers/threads, draft reports.
  - Portfolio project: a custom Skill + MCP server is a strong, demonstrable artifact for job applications.
  - Career framing: "agent engineering" is an emerging role; understanding the security tradeoffs is a differentiator.

---

## 4. In-class discussion prompts
1. Why might a university or bank *ban* self-hosted agents? Is that justified?
2. When is local-first genuinely safer than cloud, and when is it the opposite?
3. You find a useful skill on ClawHub with 12 stars and no reviews — install it? How do you decide?

## 5. Assignment ideas (pick one)
- **A (build):** Write and document a minimal OpenClaw Skill that does one useful automation; submit `SKILL.md` + a short demo video. *(Sandbox required.)*
- **B (analyze):** Read one OpenClaw CVE writeup and produce a 1-page threat model: attack vector, blast radius, mitigation.
- **C (compare):** Pick a data-science task and argue OpenClaw vs. Gemini Spark vs. a plain script — which and why.

---

## 6. Curated resources (vetted during prep — May 2026)

### Official / primary
- OpenClaw docs — Getting started: https://docs.openclaw.ai/start/getting-started
- Personal assistant setup: https://docs.openclaw.ai/start/openclaw
- GitHub (main repo): https://github.com/openclaw/openclaw
- ClawHub skill registry: https://github.com/openclaw/clawhub
- Wikipedia (timeline/facts): https://en.wikipedia.org/wiki/OpenClaw

### Best tutorials (hands-on)
- DataCamp — *Building Custom OpenClaw Skills: A Hands-On Tutorial*: https://www.datacamp.com/tutorial/building-open-claw-skills
- DEV — *OpenClaw Setup Guide: From Zero to AI Assistant in 10 Minutes*: https://dev.to/yankoaleksandrov/openclaw-setup-guide-from-zero-to-ai-assistant-in-10-minutes-3m20
- YouTube — *Full OpenClaw Setup Tutorial (Step-by-Step)*: https://www.youtube.com/watch?v=fcZMmP5dsl4
- Learn OpenClaw — *Skills & ClawHub*: https://learnopenclaw.com/core-concepts/skills
- VoltAgent — *awesome-openclaw-skills* (curated 5,400+ skills): https://github.com/VoltAgent/awesome-openclaw-skills

### Best news / context
- Lex Fridman Podcast #491 — Peter Steinberger interview (great clip source): https://lexfridman.com/peter-steinberger-transcript/
- The New Stack — *OpenClaw passed 300,000 stars. Then Google launched Spark.*: https://thenewstack.io/gemini-spark-vs-openclaw/
- Newser — *OpenClaw creator uses $1.3M in AI tokens a month*: https://www.newser.com/story/389367/openclaw-creator-uses-13m-in-ai-tokens-a-month.html

### Best security articles (for Segment 5)
- The Hacker News — *Four OpenClaw Flaws Enable Data Theft, Privilege Escalation, Persistence*: https://thehackernews.com/2026/05/four-openclaw-flaws-enable-data-theft.html
- ARMO — *CVE-2026-32922: Critical Privilege Escalation in OpenClaw*: https://www.armosec.io/blog/cve-2026-32922-openclaw-privilege-escalation-cloud-security/
- Microsoft Security Blog — *Running OpenClaw safely: identity, isolation, runtime risk*: https://www.microsoft.com/en-us/security/blog/2026/02/19/running-openclaw-safely-identity-isolation-runtime-risk/
- Sangfor — *OpenClaw Security Risks: From Vulnerabilities to Supply Chain Abuse*: https://www.sangfor.com/blog/cybersecurity/openclaw-ai-agent-security-risks-2026
- DigitalOcean — *7 OpenClaw Security Challenges to Watch for in 2026*: https://www.digitalocean.com/resources/articles/openclaw-security-challenges

### Architecture deep-dives (for Segment 2)
- Agentailor — *Lessons from OpenClaw's Architecture for Agent Builders*: https://blog.agentailor.com/posts/openclaw-architecture-lessons-for-agent-builders
- DEV — *OpenClaw Isn't the Problem. Your Agent Architecture Is.*: https://dev.to/steegi/openclaw-isnt-the-problem-your-agent-architecture-is-l16

### Comparison (for Segment 6)
- Technology.org — *Gemini Spark vs. OpenClaw: Deep Comparison 2026*: https://www.technology.org/2026/05/26/gemini-spark-vs-openclaw-deep-comparison-2026/
- Yahoo Tech — *Gemini Spark is Google's answer to OpenClaw — 3 reasons it might be better*: https://tech.yahoo.com/ai/gemini/articles/gemini-spark-googles-answer-openclaw-181052022.html

> **Note for the instructor:** Many community blogs in this space are SEO/AI-generated. Cross-check any specific command or number against the official docs, the GitHub repo, or the Wikipedia/vendor security pages before presenting it as fact.
