# AI Text Summarizer 
*Day 4-5, Week 1 — Summer Training, KAU HPC Center*

A small, containerized Python app that summarizes text using an LLM via [OpenRouter](https://openrouter.ai), and saves the result as either a `.txt` or `.pdf` — the format is decided by Python itself (based on whether you mention "pdf" in your input), not the model.

## Features
- Interactive CLI — keep summarizing until you type `exit`
- Auto-detects PDF vs TXT request and generates the right file (A4-sized PDFs via `reportlab`)
- Fully portable via Docker — no local Python setup needed

## Quick Start

```bash
docker run -it --rm -v "$(pwd)/output:/app" aalghamdi4477/summarizer:latest
```

Or with Docker Compose:

```bash
docker compose run --rm summarizer
```

Generated files will appear in the `output/` folder.

## Setup

You'll need your own [OpenRouter API key](https://openrouter.ai/settings/keys) — add it inside `Main.py` before building the image, or configure it as an environment variable if you've wired that up.

## Tech Stack
- Python 3.12
- OpenAI SDK (pointed at OpenRouter)
- ReportLab (PDF generation)
- Docker
