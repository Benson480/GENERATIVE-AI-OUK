# Codebase Genius — Assignment 2 (Jac + Python + Streamlit)

## Overview
Codebase Genius is a multi-agent Jac + Python system that generates markdown documentation and diagrams for a GitHub repo.

This repository includes:
- Jac backend (BE) with simple walkers (supervisor, http_api).
- Python helpers to clone, parse, build a simple CCG and generate docs + a diagram.
- Streamlit front-end to submit repository URLs.

## Requirements
- Python 3.10+.
- git.
- graphviz system package (for dot): e.g. `sudo apt install graphviz` (Linux) or `brew install graphviz` (macOS).
- Jaseci / Jac runtime. See below.

## Install Python deps
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r FE/requirements.txt
