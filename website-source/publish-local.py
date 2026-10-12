from pathlib import Path
import shutil
source = Path(__file__).resolve().parent
site = source.parent
build = source / "dist/client"
if not (build / "index.html").exists():
    raise SystemExit("Run npm run build first.")
for item in (site / "assets").iterdir():
    if item.is_file() and not (build / "assets" / item.name).exists():
        item.unlink()
shutil.copytree(build, site, dirs_exist_ok=True)
product = source / "vet-promo"
if product.exists():
    import subprocess
    subprocess.run(["python3", str(product / "build.py")], check=True)
    for name in ["index.html", "en.html", "privacy.html", "delete-account.html"]:
        shutil.copy2(product / name, site / "vet-charted" / name)
    for folder in ["js", "css"]:
        shutil.copytree(product / folder, site / "vet-charted" / folder, dirs_exist_ok=True)
print("Updated static site; /vet-charted/ preserved.")
