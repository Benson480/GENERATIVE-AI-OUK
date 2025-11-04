import os
import tempfile
import shutil
from urllib.parse import urlparse
import subprocess

def clone_repository(repo_url: str) -> dict:
    """
    Clone the repo_url into a temporary directory.
    Returns {'ok': True, 'path': path_to_clone, 'name': repo_name} or {'ok': False, 'error': msg}
    """
    try:
        parsed = urlparse(repo_url)
        name = os.path.splitext(os.path.basename(parsed.path))[0] or "repo"
        tmpdir = os.path.join(tempfile.gettempdir(), f"codegen_{name}")
        # remove old copy if any
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        cmd = ["git", "clone", "--depth", "1", repo_url, tmpdir]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode != 0:
            return {"ok": False, "error": res.stderr.strip() or res.stdout}
        return {"ok": True, "path": tmpdir, "name": name}
    except Exception as e:
        return {"ok": False, "error": str(e)}
