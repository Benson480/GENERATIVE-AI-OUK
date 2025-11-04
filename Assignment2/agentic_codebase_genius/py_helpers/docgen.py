import os
from pathlib import Path
import json
from .diagram import build_simple_diagram

def generate_markdown(root_path: str, repo_name: str) -> dict:
    """
    Generate docs.md from file tree, readme summary, ccg results.
    """
    outdir = Path("outputs") / repo_name
    outdir.mkdir(parents=True, exist_ok=True)
    docs_path = outdir / "docs.md"
    # load ccg if exists
    ccg_file = outdir / "ccg.json"
    ccg = {}
    if ccg_file.exists():
        try:
            ccg = json.loads(ccg_file.read_text(encoding="utf-8"))
        except Exception:
            ccg = {}
    # simple assembly
    content = []
    content.append(f"# {repo_name} — Auto generated documentation\n")
    readme_path = Path(root_path) / "README.md"
    if readme_path.exists():
        content.append("## Project overview (from README)\n")
        content.append(readme_path.read_text(encoding="utf-8")[:2000] + "\n")
    else:
        content.append("## Project overview\nNo README provided.\n")
    content.append("## Code Context Graph (CCG) summary\n")
    if ccg.get("nodes"):
        content.append(f"- Functions/classes found: {len(ccg['nodes'])}\n")
        content.append("### Sample nodes\n")
        for n in ccg["nodes"][:10]:
            content.append(f"- {n.get('id')} ({n.get('type')})\n")
    else:
        content.append("CCG not available or empty.\n")
    # generate diagram image (svg)
    diagram_path = outdir / "ccg_diagram.svg"
    build_simple_diagram(ccg, diagram_path)
    content.append("\n## Diagram\n")
    content.append(f"![CCG Diagram](./{diagram_path.name})\n")
    docs_path.write_text("\n".join(content), encoding="utf-8")
    return {"ok": True, "docs_path": str(docs_path), "diagram_path": str(diagram_path)}
