# BenchDash

Automated benchmarking platform for local LLMs running on Ollama — auto-discover, test, rank, and visualize.

![status](https://img.shields.io/badge/status-design%20document-FFB300?style=flat-square)
![language](https://img.shields.io/badge/python-3.10+-0d0d0c?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-FFB300?style=flat-square)

> **Status: Design Document** — This repository describes a planned benchmarking platform. Currently only `collector/system_info.py` is implemented. The architecture and test design are documented below.

## Overview

BenchDash is a planned self-hosted benchmarking platform for local LLMs running on Ollama. It will auto-discover models, run multi-dimensional tests (13+ categories), rank and score results, and visualize everything in a Chart.js dashboard. Supports direct Ollama API calls, Hermes agent, and multi-agent benchmarking modes.

## Features (Planned)

- Automated model discovery — detects all Ollama models, benchmarks smallest to largest
- 13+ test categories — knowledge, reasoning, coding, creativity, conversation, stress, and more
- Multi-agent support — Direct Ollama API, Hermes CLI agent, multi-agent orchestration
- Scoring engine — weighted multi-dimensional ranking with configurable criteria
- Chart.js dashboard — visual comparison of model performance
- SQLite storage — local result persistence
- Docker Compose deployment
- Export results to JSON/CSV

## Architecture / Tech Stack

- **Backend**: Python 3.10+, FastAPI (planned)
- **LLM**: Ollama API
- **Database**: SQLite
- **Dashboard**: Chart.js (planned)
- **Deployment**: Docker Compose

## Current State

Only `collector/system_info.py` is implemented. See [ROADMAP.md](ROADMAP.md) for build progress.

## License

MIT — see [LICENSE](LICENSE).

---
Part of the JorahOne / J1 ecosystem — benchmarking tools for self-hosted LLM infrastructure.
