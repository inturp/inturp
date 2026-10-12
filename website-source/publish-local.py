from pathlib import Path
import shutil
source = Path(__file__).resolve().parent
site = source.parent
for item in (source / "dist/client").iterdir():
    if item.is_dir():
        shutil.copytree(item, site / item.name, dirs_exist_ok=True)
    else:
        shutil.copy2(item, site / item.name)
print("Updated static site; /vet-charted/ preserved.")
