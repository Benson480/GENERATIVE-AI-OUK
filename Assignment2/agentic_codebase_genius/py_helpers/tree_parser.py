import os
import json
from pathlib import Path

# Simple file tree generator and a very simple "CCG" stub that finds function definitions using ast
import ast

def build_file_tree(root_path: str) -> dict:
    """
    Walk repository, ignore .git, node_modules, __pycache__.
    Return a filetree dict and list of top files (heuristic).
    """
    ignore = {'.git', 'node_modules', '__pycache__'}
    filetree = {}
    top_files = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # filter out ignored dirs
        dirnames[:] = [d for d in dirnames if d not in ignore]
        rel = os.path.relpath(dirpath, root_path)
        files = [f for f in filenames if f.endswith(('.py', '.jac', '.md'))]
        if files:
            filetree[rel] = files
        # heuristic: look for app.py, main.py, README.md at repo root
        if rel == ".":
            for candidate in ("app.py", "main.py", "README.md", "readme.md"):
                if candidate in filenames and candidate not in top_files:
                    top_files.append(candidate)
    # fallback: pick first python file found
    if not top_files:
        for rel, files in filetree.items():
            for f in files:
                if f.endswith(".py") and f not in top_files:
                    top_files.append(f)
                    if len(top_files) >= 3:
                        break
            if len(top_files) >= 3:
                break
    return {"filetree": filetree, "top_files": top_files}

def parse_and_build_ccg(root_path: str, entry_filename: str) -> dict:
    """
    Very simple parser: parse python files and extract functions/classes and call relations in that file.
    Save intermediate CCG json to outputs/<repo>/ccg.json
    """
    outputs = Path("outputs")
    outputs.mkdir(parents=True, exist_ok=True)
    repo_name = Path(root_path).name
    repo_out = outputs / repo_name
    repo_out.mkdir(exist_ok=True)
    ccg = {"nodes": [], "edges": []}
    # naive implementation: find defs in each .py under root_path
    for pyfile in Path(root_path).rglob("*.py"):
        try:
            with open(pyfile, "r", encoding="utf-8") as fh:
                src = fh.read()
            tree = ast.parse(src)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    node_id = f"{pyfile.relative_to(root_path)}:{node.name}"
                    ccg["nodes"].append({"id": node_id, "type": "function", "lineno": node.lineno})
                    # find simple calls inside function body
                    for child in ast.walk(node):
                        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                            target = child.func.id
                            ccg["edges"].append({"from": node_id, "to": target})
                if isinstance(node, ast.ClassDef):
                    node_id = f"{pyfile.relative_to(root_path)}:{node.name}"
                    ccg["nodes"].append({"id": node_id, "type": "class", "lineno": node.lineno})
        except Exception:
            continue
    # write a CCg JSON
    ccg_path = repo_out / "ccg.json"
    with open(ccg_path, "w", encoding="utf-8") as fh:
        json.dump(ccg, fh, indent=2)
    return {"ok": True, "ccg_path": str(ccg_path)}

def export_ccg(root_path: str) -> dict:
    repo_name = Path(root_path).name
    ccg_path = Path("outputs") / repo_name / "ccg.json"
    if ccg_path.exists():
        return {"ok": True, "ccg_summary": str(ccg_path)}
    else:
        return {"ok": False, "error": "ccg not found"}
