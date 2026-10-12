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

# Pre-paint script: applies the shared theme (inturp-theme) and language (inturp-lang) before first paint,
# so moving between inturp.com, /vet-charted/ and /alameer/ never flashes the wrong theme or language.
PREPAINT = ("<script data-inturp-prepaint>(function(){try{var d=document.documentElement,L=localStorage,"
            "t=L.getItem('inturp-theme'),dk=t==='dark'||(t!=='light'&&matchMedia('(prefers-color-scheme: dark)').matches);"
            "d.classList.toggle('dark',dk);d.style.colorScheme=dk?'dark':'light';var p=location.pathname;"
            "if(p.indexOf('/ar')===0&&(p.length===3||p.charAt(3)==='/')){L.setItem('inturp-lang','ar')}"
            "else if(L.getItem('inturp-lang')==='ar'){location.replace('/ar'+(p==='/'?'/':p)+location.search+location.hash)}"
            "}catch(e){}})()</script>")
for page in build.rglob("*.html"):
    if page.name == "404.html":
        continue
    target = site / page.relative_to(build)
    html = target.read_text(encoding="utf-8")
    if "data-inturp-prepaint" not in html and "<head>" in html:
        target.write_text(html.replace("<head>", "<head>" + PREPAINT, 1), encoding="utf-8")
product = source / "vet-promo"
if product.exists():
    import subprocess
    subprocess.run(["python3", str(product / "build.py")], check=True)
    pages = ["index.html", "en.html", "privacy.html", "delete-account.html"]
    pages += [str(f.relative_to(product)) for sub in ("en", "privacy", "delete-account") for f in (product / sub).rglob("index.html")]
    for name in pages:
        (site / "vet-charted" / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(product / name, site / "vet-charted" / name)
    for folder in ["js", "css"]:
        shutil.copytree(product / folder, site / "vet-charted" / folder, dirs_exist_ok=True)
print("Updated static site; /vet-charted/ preserved.")
