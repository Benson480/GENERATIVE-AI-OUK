import os

def summarise_readme(root_path: str) -> dict:
    """
    Very simple README summariser: returns first 4 lines or the whole short README.md
    (In a full implementation replace with LLM call)
    """
    candidates = ["README.md", "readme.md", "docs/README.md"]
    summary = ""
    for c in candidates:
        p = os.path.join(root_path, c)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as fh:
                lines = fh.readlines()
            summary = "".join(lines[:8]).strip()
            break
    if not summary:
        summary = "No README found or it's empty."
    return {"ok": True, "summary": summary}
