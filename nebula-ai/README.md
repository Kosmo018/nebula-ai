# Nebula AI

**Turn long-form YouTube videos into vertical Shorts — guided by AI, inspired by the cosmos.**

Nebula AI is a Python research-and-engineering project for a U.S. university portfolio. It explores the full path from a public YouTube URL to a set of Shorts-ready clips: download, multimodal analysis, and precise editorial cuts. The goal is not only automation, but *judgment* — selecting moments that feel complete, paced, and watchable on a phone.

Meet **Nebby**, our cosmic astronaut drone mascot. Nebby scouts the “nebula” of a long video the way a small craft maps a star field: hovering over scenes, tagging bright spots of energy, and bringing home compact highlights. The branding is playful; the pipeline is meant to be rigorous, documented, and easy for a faculty reviewer to run.

---

## Why this project

Short-form video sits at the intersection of **media systems**, **machine learning**, and **human attention**. This repository is designed as a clean academic artifact:

- A readable `src/` layout with explicit pipeline stages
- Placeholder interfaces you can replace with real models without rewriting the story of the code
- Tests that lock in configuration contracts before models land
- A stack that is honest about dependencies (download, FFmpeg-class editing, optional LLM/vision)

## Intended pipeline

```
YouTube URL  →  download  →  AI highlight detection  →  9:16 Shorts export
                 (yt-dlp)     (scene / speech / vision)    (MoviePy / FFmpeg)
```

1. **Acquire** — fetch source media and metadata.
2. **Interpret** — detect scenes, speech, and candidate “hooks.”
3. **Compose** — crop to 9:16, trim to Shorts length, write files under `output/`.

Each stage in `src/main.py` is currently a typed placeholder (`NotImplementedError`) so the architecture is reviewable before GPU or API keys are required.

## Project structure

```
nebula-ai/
├── src/
│   ├── __init__.py
│   └── main.py          # pipeline entry + stage stubs
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
pytest
```

FFmpeg should be installed on the system PATH before video cutting is implemented.

## Academic notes

Use only content you have the right to process. YouTube’s terms of service and copyright law still apply; this codebase is a learning scaffold, not a distribution product. When models are added, document training data, prompts, and evaluation criteria in this README so a reviewer can reproduce your claims.

---

*Nebby keeps watch from the dark side of the timeline. Fly safe.*
