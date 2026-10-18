# INTENT.md — J1-PIPELINE Phase -1 (ORACLE)

**Repository:** `OneByJorah/benchova`
**Analysis Date:** 2026-07-05
**Analyst:** J1-PIPELINE ORACLE (read-only)
**Status:** Intent Reconstructed (updated from prior ORACLE run)

> **Update 2026-08-22:** Since this analysis, the repo gained `index.html` (standalone dashboard UI, sample data), `Dockerfile`, `docker-compose.yml`, `.env.example`, `docs/`, `j1.yaml`, `.dockerignore`, and `CODEOWNERS` — several "missing" items listed below now exist. The core finding stands: the benchmark backend (`app.py`, runner, scoring, persistence, scheduler, notifications) is still unimplemented. See README status banner.

---

## What This System Does

### Technical Role

**Ollama Benchmark Dashboard (benchova)** is a planned comprehensive, automated benchmarking platform for local LLMs running on [Ollama](https://ollama.ai). The README describes an end-to-end pipeline that would:

1. **Auto-discover** all Ollama models available on the host machine
2. **Run multi-dimensional tests** across 13+ categories (knowledge, programming, math, reasoning, creativity, conversation, vision, image/audio/video generation, game development, error resilience, consistency, and context-window stress)
3. **Support three agent modes** — direct Ollama API calls (baseline), Hermes Agent (with tool access), and Claude Code (via Ollama proxy) — enabling comparative evaluation of the same model under different orchestration layers
4. **Collect system telemetry** — CPU/RAM/GPU/VRAM/CUDA/driver/OS metrics alongside every benchmark run
5. **Score and rank** results using a discrete-tier scoring system (0.1–1.0) with per-category and overall leaderboards, plus bonus awards for top performers
6. **Persist results** in SQLite (`benchmark.db`) and per-model JSON files under `results/`
7. **Serve a real-time dashboard** — a self-contained HTTP server with Chart.js visualizations (score by model/mode, success rates, category radar, tokens/sec, model summary tables, filter controls, auto-refresh)
8. **Export** to CSV, JSON, and Markdown report formats
9. **Support scheduling** (cron-style daily/weekly/monthly) and **Telegram notifications** for run completions

**Current implementation status:** Only 1 of the ~20 described modules exists — `collector/system_info.py` (101 lines). The rest of the architecture is documented but not yet implemented. This repo is currently a **design document with one working module**.

### Operational Role

As designed, the system would operate as a **local-first observability and evaluation tool** for AI/LLM workloads, running on the same machine as Ollama (or pointing to a remote Ollama host) with no external infrastructure beyond Python 3.10+ and a running Ollama instance. The dashboard would bind to `0.0.0.0:8081` by default.

In its current state, the system can only collect system telemetry via `collector/system_info.py` and save it to `system_info.json`. It cannot run benchmarks, serve a dashboard, or produce reports.

---

## Why This Was Built

### Real Problem

Evaluating local LLMs is ad-hoc and inconsistent. Practitioners typically:

- Run a few manual prompts and eyeball quality
- Have no standardized, repeatable test suite
- Cannot compare models across multiple dimensions (knowledge vs. speed vs. creativity vs. context retention)
- Have no way to compare the same model under different agent orchestration layers (raw API vs. agent framework)
- Lack historical tracking — results are lost after a terminal session

This makes it impossible to make data-driven decisions about which model to use for which task, or to track regressions when models are updated.

### Why Existing Tools Were Insufficient

| Tool | Limitation |
| ------ | ----------- |
| **Ollama itself** | No built-in benchmarking or evaluation |
| **lm-eval-harness** | Complex setup, specific model formats, no multi-agent comparison, no real-time dashboard |
| **OpenAI Evals** | Cloud-focused, not designed for local Ollama models |
| **Manual testing** | Not repeatable, not standardized, no historical persistence |
| **LLM latency benchmarks** | Measure speed only, ignore quality, reasoning, creativity, and robustness |

No existing tool combines: (a) multi-dimensional quality testing, (b) multi-agent orchestration comparison, (c) system telemetry collection, (d) real-time visualization, (e) historical persistence, and (f) scheduling — all in a single zero-dependency Python codebase.

### What Triggered Development

The rapid proliferation of local LLMs via Ollama (Gemma 2, Llama 3, Mistral, Qwen, Phi, etc.) created an urgent need for systematic evaluation. The author (Jhonattan L. Jimenez / OneByJorah) needed a tool to:

- Objectively compare models for production deployment decisions
- Evaluate how different agent frameworks (Hermes Agent, Claude Code) affect model output quality vs. raw API calls
- Track performance regressions across Ollama version updates
- Generate shareable benchmark reports for the open-source AI community

The initial release (v1.0.0) was published on 2026-07-04. The first commit (`bc0ced5`, by "Villon") added the README and `collector/system_info.py` — a documentation-first approach that describes the full vision before implementation. The second commit (`0f88ea9`, by "JorahOne Admin") added all community/governance files (LICENSE, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT, CHANGELOG, ROADMAP, .gitignore, .github/*). The third commit (`22403c5`, by "OneByJorah") sanitized email references — a security audit pass.

### Ecosystem Fit

This repository is part of the **OneByJorah** organization's portfolio of AI infrastructure tools. It integrates with:

- **Hermes Agent** — one of the three benchmark agent modes, testing models through Hermes' tool-calling layer
- **Claude Code** — another agent mode, testing models through Claude Code's orchestration
- **Codebuff** — referenced in the README footer as a related tool
- **Ollama** — the core runtime being benchmarked

The system fills the **observability and evaluation gap** in the JorahOne stack: given that the organization builds AI agent tooling (Hermes Agent), there is a natural need to systematically measure and compare the underlying models those agents orchestrate.

---

## Operational Classification

## Classification: PROTOTYPE / DESIGN DOCUMENT

Evidence:

- **v1.0.0 tagged** in CHANGELOG — but no actual benchmark code exists beyond one collector module
- **3 commits** from 3 different author names (Villon, JorahOne Admin, OneByJorah) — likely the same person with different git configurations
- **Only 1 Python module** exists (`collector/system_info.py`, 101 lines) out of ~20 described modules
- **No `orchestrator.py`**, **no `run_benchmark.py`**, **no `dashboard_server.py`** — the core pipeline is entirely unimplemented
- **No `static/` directory** — the dashboard frontend does not exist
- **No `tests/` directory** — no test modules exist
- **No `db/`, `ranking/`, `exports/`, `scheduler/`, `notifications/` directories** — the data layer, scoring, export, scheduling, and notification subsystems are all unimplemented
- **No `results/` or `outputs/` directories** — no runtime artifacts exist
- **No `requirements.txt`, `pyproject.toml`, or `Dockerfile`** — no dependency or container definitions
- **No `j1.yaml`** — J1 pipeline metadata file is missing
- **No `docs/` directory** — no supplementary documentation
- **CodeQL CI configured** for Python, JavaScript, and TypeScript — but only Python files exist (JS/TS are template vestiges)
- **Dependabot configured** for pip, npm, docker, and GitHub Actions — but no `requirements.txt`, `package.json`, or `Dockerfile` exist (template vestiges)
- **Security policy exists** (SECURITY.md) with vulnerability reporting process
- **Community files exist** (CODE_OF_CONDUCT.md, CONTRIBUTING.md, issue/PR templates)
- **Audit branch exists** (`origin/audit/benchova`) from a prior J1 pipeline run — indicating the pipeline has touched this repo before
- **MIT License** with copyright assigned to Jhonattan L. Jimenez

---

## Key Architectural Decisions

1. **Zero pip dependencies** — Uses only Python stdlib + Ollama HTTP API + Chart.js CDN. This is a deliberate design choice to minimize setup friction, but it also means no dependency pinning or lockfile.

2. **SQLite + JSON dual persistence** — Structured queries via SQLite + portable per-run JSON files. Provides both queryability and portability.

3. **Discrete scoring tiers** (0.1/0.4/0.7/1.0) — Avoids false precision in subjective LLM evaluation. A deliberate rejection of continuous scoring.

4. **Multi-agent comparison** — Same model tested through different orchestration layers (raw API, Hermes Agent, Claude Code). This is the unique differentiator vs. existing tools.

5. **Self-contained dashboard** — No web framework dependency; single-file HTTP server using Python's `http.server`. Chart.js loaded via CDN.

6. **Documentation-first development** — The README describes the full architecture before implementation. The repo was started with a comprehensive design document, not incremental code.

---

## Repository Structure

```text
|benchova/
├── collector/
│   └── system_info.py          # ✓ EXISTS — System telemetry collector (101 lines)
├── .github/
│   ├── dependabot.yml          # ✓ EXISTS — pip, npm, docker, GH Actions (template vestiges)
│   ├── workflows/
│   │   └── codeql.yml          # ✓ EXISTS — Python, JS, TS analysis (JS/TS are vestiges)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md       # ✓ EXISTS
│   │   └── feature_request.md  # ✓ EXISTS
│   └── PULL_REQUEST_TEMPLATE.md # ✓ EXISTS
├── CHANGELOG.md                # ✓ EXISTS — v1.0.0 entry
├── CODE_OF_CONDUCT.md          # ✓ EXISTS
├── CONTRIBUTING.md             # ✓ EXISTS
├── INTENT.md                   # ✓ EXISTS — This file
├── LICENSE                     # ✓ EXISTS — MIT
├── README.md                   # ✓ EXISTS — Full architecture design document
├── ROADMAP.md                  # ✓ EXISTS — Generic placeholder
├── SECURITY.md                 # ✓ EXISTS — Vulnerability reporting process
└── .gitignore                  # ✓ EXISTS — Python, venv, node_modules, IDE, OS, build artifacts
```

**Missing directories (described in README but not present):**

- `tests/` — 13 test category modules
- `ranking/` — scorer and bonus modules
- `db/` — SQLite schema and CRUD
- `exports/` — CSV, JSON, Markdown export
- `scheduler/` — cron-style scheduling
- `notifications/` — Telegram integration
- `static/` — Dashboard frontend (index.html)
- `results/` — Per-run JSON files
- `outputs/` — Generated artifacts
- `docs/` — Supplementary documentation

**Missing files (described in README but not present):**

- `orchestrator.py` — Main pipeline runner
- `run_benchmark.py` — Single-model runner
- `run_one_model.py` — Simplified runner
- `dashboard_server.py` — HTTP dashboard server
- `benchmark_meta.json` — Task definitions
- `models.json` — Discovered models
- `system_info.json` — Hardware report (generated at runtime)
- `benchmark.db` — SQLite database
- `leaderboard.json`, `benchmark.csv`, `benchmark.json`, `report.md` — Output artifacts
- `j1.yaml` — J1 pipeline metadata

---

## Notes

### Config-Drift Patterns

1. **Dependabot ecosystem mismatch**: Dependabot is configured for `pip`, `npm`, and `docker` ecosystems, but no `requirements.txt`, `pyproject.toml`, `package.json`, or `Dockerfile` exist in the repo. This is a template vestige from the JorahOne portfolio standardization (second commit).

2. **CodeQL language mismatch**: CodeQL is configured to analyze Python, JavaScript, and TypeScript, but only Python files exist. The JS/TS entries are template vestiges.

### Git History

- **3 commits, 3 author names**: `Villon` (initial commit), `JorahOne Admin` (portfolio standardization), `OneByJorah` (security audit). These are almost certainly the same person (Jhonattan L. Jimenez) using different git configurations.
- **Initial commit** (`bc0ced5`): Added `README.md` and `collector/system_info.py` — the README was the first artifact, confirming a documentation-first development approach.
- **Second commit** (`0f88ea9`): Added all community/governance files — this is the JorahOne portfolio standardization pass.
- **Third commit** (`22403c5`): Sanitized email references — a security audit pass, which is a positive maturity signal.
- **Audit branch** (`origin/audit/benchova`): A prior J1 pipeline run created this branch, indicating the pipeline has already touched this repo.

### Implementation Gap

The most significant finding is the **gap between documented architecture and implemented code**. The README describes a complete benchmarking platform with ~20 modules, but only 1 module (`collector/system_info.py`) actually exists. This is not necessarily a problem — it may be intentional (design-first development) — but it means the repo is currently a **prototype/design document** rather than a working system.

### Author Attribution

The three different author names in git history (Villon, JorahOne Admin, OneByJorah) all map to the same person. This is a common pattern in JorahOne repos where the author uses different git configurations across different machines or contexts.
