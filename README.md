# Multi-LLM Orchestration API

## Overview
This project demonstrates a FastAPI backend that orchestrates two LLMs (OpenAI ChatGPT + Google Gemini/Vertex AI) to generate backend application code from a natural-language prompt. The system:
- asks ChatGPT to generate code,
- asks Gemini to review and improve the generated code,
- merges both outputs,
- validates Python files for syntax,
- writes files to disk and zips them.

## Setup

1. Clone the repo
2. Create a Python 3.10+ virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
