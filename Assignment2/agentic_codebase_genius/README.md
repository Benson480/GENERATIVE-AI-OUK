Codebase Genius — Agentic Code-Documentation System

Author: Benson Mwangi
Course: Generative AI (Open University of Kenya)
Project: Codebase Genius — multi-agent pipeline (Jac + Python)
Repo layout: agentic_codebase_genius/
(BE = backend Jac walkers, py_helpers = Python helpers, FE = Streamlit frontend, outputs = generated docs)

Assignment source: Requirements and evaluation criteria from the course assignment (see uploaded brief). 

Assignment2 Code genius

Table of contents

Project summary

Architecture & components

Features implemented

Prerequisites

Install & setup (quick)

Run the backend (Jac) and frontend (Streamlit)

API: how to call the system (examples)

Outputs & sample artifacts

Design notes, error handling & limitations

Testing & recommended sample repos

Extending & ideas for future work

Credits & references

Project summary

Codebase Genius is an autonomous, multi-agent system that accepts a public GitHub repository URL and produces a human-readable, well-structured Markdown documentation package for that repository. The system is optimized for Python and Jac codebases but is designed to be extensible.

Main technologies:

Jac (JacLang) — agent language for walker-based orchestration (BE).

Python — helper utilities for cloning repos, parsing (tree-sitter), building a Code Context Graph (CCG), and rendering markdown/diagrams (py_helpers).

Streamlit — simple UI to submit repos and view results (FE).

This project follows the multi-agent workflow described in the assignment and the byLLM Task Manager example as guidance. 

Assignment2 Code genius

Architecture & components

High-level architecture (pipeline):

Client (Streamlit) -> Jac Supervisor walker (BE/main.jac)
    -> RepoMapper walker (clone, file-tree, README summary)  (py_helpers.clone_repo)
    -> CodeAnalyzer walker (parse files, build CCG)         (py_helpers.parser_ccg)
    -> DocGenie walker (assemble markdown + generate diagrams) (py_helpers.render_md)
    -> outputs/<repo_name>/docs.md + diagrams


Key agents (Jac walkers):

Supervisor (Code Genius) — orchestrates the pipeline, decides analysis order based on README and file map, collects partial results, triggers documentation generation.

RepoMapper — clones repository, builds file-tree, extracts README summary and candidate entry points.

CodeAnalyzer — parses prioritized files (tree-sitter), extracts function/class definitions and call relationships, builds a Code Context Graph (CCG).

DocGenie — synthesizes the final docs.md, includes summary, file tree, API reference, and embeds diagrams (SVG/PNG).

Python helper modules (exposed via Jac py_module):

clone_repo.py — clones repository to a temp dir and produces structured file list and README summary.

parser_ccg.py — uses Tree-sitter to parse source and produce a simple CCG (nodes/edges).

render_md.py — consolidates results into Markdown and generates diagram images (Graphviz/pydot).

Features implemented

Repository validation and cloning (public GitHub URL).

File-tree generation with pruning (.git, node_modules, venv, pycache).

README summarization (simple extractive summary; can call an LLM for abstractive summaries if API key provided).

Prioritization of entry points (heuristic: main.py, app.py, top-level .py files).

Tree-sitter based parsing for Python files to detect functions, classes and simple call relationships.

Construction of a Code Context Graph (CCG) stored as structured JSON (and rendered as SVG).

Document generation into outputs/<repo>/docs.md including Overview, File tree, Entry points, CCG diagram, and API listings.

Streamlit frontend to submit a repo URL and poll for results.

Robust error handling for unreachable repos, clone failures, parse exceptions and missing README.

Prerequisites

Git CLI installed and in PATH.

Python 3.10+ (3.12 recommended).

jaclang installed and jac CLI available (see Jac docs).

Optional for diagrams: Graphviz installed (dot), pydot.

Internet access (to clone GitHub repos and call external LLMs if used).

Install & setup (quick)

Clone this project (or place files into agentic_codebase_genius/):

git clone <your-repo-url> agentic_codebase_genius
cd agentic_codebase_genius


Create & activate a Python venv:

python -m venv env
# Windows
.\env\Scripts\activate
# mac / linux
source env/bin/activate


Install Python helper deps:

pip install -r py_helpers/requirements.txt


py_helpers/requirements.txt includes:

gitpython
tree_sitter
networkx
pydot
python-dotenv
requests


Install Jac (if not installed)
Follow Jac docs: https://jac-lang.org/learn/getting_started
 (ensure jac binary is in PATH).

(Optional) Install FE dependencies:

pip install -r FE/requirements.txt
# FE/requirements.txt includes: streamlit, requests


Create a .env in repository root and add any LLM key if you want abstractive README summarization:

# For OpenAI
OPENAI_API_KEY=sk-...
# or for Gemini (if you add support)
GEMINI_API_KEY=...


By default the system will run without an LLM; LLM is optional for better README summaries and doc polishing.

Run the backend (Jac) and frontend (Streamlit)
1) Start Jac server (backend)

Open a terminal, activate venv, then:

cd BE
jac serve main.jac


This launches a local Jac server exposing walkers (e.g., Supervisor) that can be triggered via an HTTP wrapper or Jac API.

If you prefer, you can run jac in debug mode or run specific walkers from CLI during development.

2) Start the Streamlit frontend (optional)

Open another terminal (venv active):

cd FE
streamlit run app.py


The simple UI lets you input a GitHub repo URL and submits it to the Jac backend (the FE app issues an HTTP POST to the Jac wrapper endpoint — adjust the endpoint URL if different).

API: how to call the system (examples)

The Jac server can be called directly with the included HTTP wrapper. The FE uses the wrapper, but you can call it with curl/postman.

HTTP wrapper (example) — this wrapper should be implemented to call Supervisor.enter(repo_url); a minimal curl example (if wrapper at http://localhost:8000/run):

curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"walker":"Supervisor","repo_url":"https://github.com/<owner>/<repo>"}'


Expected immediate response:

{
  "status":"accepted",
  "job_id":"job-12345",
  "message":"Repo accepted. Processing started."
}


Poll for result (example):

curl http://localhost:8000/result/job-12345


Successful result:

{
  "status":"completed",
  "output_path":"./outputs/<repo_name>/docs.md",
  "ccg_svg":"./outputs/<repo_name>/ccg.svg"
}

Outputs & sample artifacts

Upon successful run you will find:

outputs/
  <repo_name>/
    docs.md        # generated documentation (Markdown)
    ccg.svg        # code context graph (diagram)
    file_tree.json # structured file-tree produced by RepoMapper
    raw_summary.txt # README extractive summary


docs.md includes:

Project title and summary (from README summary and optional LLM refinement).

File tree listing with code file links.

Entry points identified.

API reference-style sections for important classes/functions.

Embedded CCG diagram to visualize function/class relationships.

Design notes, error handling & limitations

Design choices

The Supervisor chooses a prioritized analysis order using README summary and heuristic entry point detection. This ensures high-impact files are documented first.

Heavy tasks such as parsing and diagram generation are implemented in Python helper modules and invoked from Jac for performance and library compatibility.

Error handling

Invalid/Private repo: clone fails → RepoMapper returns error → Supervisor passes structured error back to client.

Parsing failures: CodeAnalyzer catches tree-sitter parse exceptions and annotates the docs with “CCG generation failed for file X: <error>”.

Partial outputs: Supervisor writes partial docs.md as it goes and updates outputs/<repo>/progress.json so users can retrieve intermediate results.

Limitations

Current tree-sitter extraction is a practical/simple implementation (sufficient for assignment); advanced cross-file resolution and name binding will require more robust AST traversal.

LLM integration is optional; large repos may need increased timeouts or batching.

Testing & recommended sample repos

Start testing with small-to-medium public Python repos (single module) before scaling to large monorepos.

Suggested test repos:

Simple web app: https://github.com/pallets/flask (large; use a fork or subset)

Small sample: a simple example repo you control (1–3 Python files)

Jac examples: any Jac-focused repo to test Jac parsing

When testing:

Observe logs in the Jac terminal for walker events.

Inspect outputs/<repo> for generated docs.

Check progress.json (if enabled) for real-time status.

Extending & ideas for future work

More language support: add tree-sitter grammars for JS/TS, C/C++, Java and wire them to parser_ccg.

Advanced analyses: compute cyclomatic complexity (radon), function docstring coverage, test coverage hints.

Searchable docs: generate static site (MkDocs) from docs.md with cross-links.

Fine-tune LLM prompts for better API prose, code examples, and README rewriting.

Authentication & rate limiting for the HTTP wrapper in production.

Troubleshooting

jac not found — ensure jac is installed and on PATH; follow Jac docs.

Tree-sitter errors — verify the language library (my-langs.so) is built and parser.set_language points to the correct Language object.

Graphviz/SVG errors — install graphviz system package and ensure dot is in PATH.

LLM errors — confirm .env contains a valid key and network access is allowed.

Credits & references

Assignment brief: Codebase Genius — Generative AI project, Open University of Kenya. 

Assignment2 Code genius

byLLM Task Manager example (Jaseci Labs) — used as reference for multi-agent patterns.

Jac language docs & beginner guide — https://jac-lang.org/learn/

Tree-sitter — https://tree-sitter.github.io/tree-sitter/

Graphviz / pydot — for diagrams

Final notes

This README documents the delivered architecture, setup, and run instructions for Codebase Genius. The code structure, Jac walker templates and Python helper modules implement the assignment goals: clone, map, analyze, build CCG and generate polished documentation with diagrams.