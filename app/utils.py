import os
import ast
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Tuple, Dict, Any

from .config import OUTPUT_BASE

def safe_parse_python(code: str) -> Tuple[bool, str]:
    """
    Attempt to parse Python code to check for syntax errors.
    Returns (is_valid, error_message_if_any)
    """
    try:
        ast.parse(code)
        return True, ""
    except Exception as e:
        return False, str(e)

def write_project_files(base_dir: Path, files: Dict[str, str]) -> None:
    """
    files: {'app/main.py': 'code...', 'app/models.py': 'code...'}
    """
    for rel_path, content in files.items():
        dest = base_dir / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(content)

def make_zip(folder: Path, output_zip: Path) -> Path:
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = Path(root) / file
                arcname = full_path.relative_to(folder)
                z.write(full_path, arcname)
    return output_zip

def new_project_folder(prefix="generated_backend") -> Path:
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    folder = OUTPUT_BASE / f"{prefix}_{timestamp}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder
