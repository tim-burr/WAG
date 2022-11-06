# Imports
# Standard
import shutil
from pathlib import Path

def copy_file(src, dest) -> None | bool:
    try:
        shutil.copy(src, dest)
    except shutil.SameFileError:
        print("Error: Source and destination are the same file.")
        return False
    except IsADirectoryError:
        print("Error: The destination is a directory.")
        return False
    print(f"Copy: file {src} into {dest}")

def copy_directory(src, dest) -> None:
    print(f"Copy: {src}\\ into {dest}\\")
    shutil.copytree(src, dest / Path(src).stem, dirs_exist_ok=True)

def copy_recursive(src, dest) -> None:
    print(f"Copy: {src}\\ into {dest}\\")
    shutil.copytree(src, dest, dirs_exist_ok=True)

def walk_dir(dir) -> dict:
    files = {}
    for file in Path(dir).rglob('*.*'):
        files[file.stem] = file.resolve()
    return files  # {filename, absolute path}

def open_file(file, encoding='utf-8') -> str:
    with open(file, 'r', encoding=encoding) as f:
        return f.read()

def create_directory(dir) -> None:
    if not Path(dir).exists():
        print(f"Create: directory {dir}\\")
        Path.mkdir(dir, parents=True)
    
def delete_directory(dir) -> None:
    if Path(dir).exists():
        print(f"Remove: directory {dir}\\")
        shutil.rmtree(dir)