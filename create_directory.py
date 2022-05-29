import pathlib
from pathlib import Path
import hashlib


def create_directory(filename: str) -> pathlib:
    filename_hash = hashlib.md5(filename.encode('utf-8'))
    parent_dir = Path.cwd().parent
    main_dir = filename_hash.hexdigest()[:2]
    Path.mkdir(parent_dir / main_dir, exist_ok=True)
    sub_dir = filename_hash.hexdigest()[2:5]
    Path.mkdir(pathlib.Path(parent_dir) / main_dir / sub_dir, exist_ok=True)

    return parent_dir / main_dir / sub_dir

