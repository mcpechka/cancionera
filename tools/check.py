"""Check the tunas/ folder: run before opening a pull request.
Usage: python3 tools/check.py   (exit code 1 on errors)"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
T = os.path.join(ROOT, "tunas")
BECAS = "burdeos granate rojo naranja amarillo verde turquesa celeste azul morado rosa negro plata blanco".split()
errors, warnings = [], []

def check_cho(path):
    txt = open(path, encoding="utf-8").read()
    if not re.search(r"^\{\s*(title|t)\s*:", txt, re.M | re.I): errors.append(f"{path}: no {{title: …}}")
    stack = []
    for n, line in enumerate(txt.splitlines(), 1):
        m = re.match(r"^\{\s*(start|end)_of_(\w+)", line)
        if m:
            if m.group(1) == "start": stack.append((m.group(2), n))
            elif not stack or stack.pop()[0] != m.group(2): errors.append(f"{path}:{n}: {{end_of_{m.group(2)}}} without matching start")
        if line.count("[") != line.count("]"): errors.append(f"{path}:{n}: unbalanced [ ]")
    for kind, n in stack: errors.append(f"{path}:{n}: {{start_of_{kind}}} never closed")

ids = json.load(open(os.path.join(T, "index.json")))
for d in sorted(os.listdir(T)):
    if os.path.isdir(os.path.join(T, d)) and not d.startswith("_") and d not in ids:
        warnings.append(f"tunas/{d}/ is not listed in tunas/index.json")
for i in ids:
    base = os.path.join(T, i)
    if not re.fullmatch(r"[a-z0-9-]+", i): errors.append(f"index.json: bad folder name {i!r}")
    if not os.path.isfile(os.path.join(base, "tuna.json")): errors.append(f"tunas/{i}/tuna.json missing"); continue
    try: cfg = json.load(open(os.path.join(base, "tuna.json"), encoding="utf-8"))
    except Exception as e: errors.append(f"tunas/{i}/tuna.json: {e}"); continue
    if not cfg.get("name"): errors.append(f"tunas/{i}/tuna.json: name is empty")
    b = cfg.get("beca", "")
    if b and b not in BECAS and not re.fullmatch(r"#[0-9a-fA-F]{6}", b): errors.append(f"tunas/{i}/tuna.json: unknown beca {b!r}")
    for s in cfg.get("songs", []):
        p = os.path.join(ROOT, s[1:]) if s.startswith("/") else os.path.join(base, s)
        if not os.path.isfile(p): errors.append(f"tunas/{i}: song file {s} not found")
        elif p.endswith((".cho", ".chopro")): check_cho(p)
    for ph in cfg.get("photos", []):
        if not os.path.isfile(os.path.join(base, ph.get("file", ""))): errors.append(f"tunas/{i}: photo {ph.get('file')} not found")
        elif os.path.getsize(os.path.join(base, ph["file"])) > 1_000_000: warnings.append(f"tunas/{i}: {ph['file']} is over 1 MB")
    links = [("artist", k, u) for k, u in (cfg.get("artist") or {}).items()]
    for al in cfg.get("albums", []):
        if not al.get("title"): errors.append(f"tunas/{i}: an album has no title")
        links += [(al.get("title") or "album", k, u) for k, u in (al.get("links") or {}).items()]
        cov = al.get("cover", "")
        if cov and not cov.startswith("https://") and not os.path.isfile(os.path.join(base, cov)): errors.append(f"tunas/{i}: album cover {cov} not found")
        for tr in al.get("tracks", []):
            if not (isinstance(tr, str) or (isinstance(tr, dict) and tr.get("title"))): errors.append(f"tunas/{i}: album {al.get('title')}: bad track {tr!r}")
    for where, k, u in links:
        if not str(u).startswith("https://"): errors.append(f"tunas/{i}: {where}: {k} link needs https://")
    for r in cfg.get("recordings", []):
        if not str(r.get("url", "")).startswith("https://"): errors.append(f"tunas/{i}: recording {r.get('title') or r.get('song')} needs an https:// url")
    listed = {os.path.normpath(os.path.join(base, s)) for s in cfg.get("songs", [])}
    sd = os.path.join(base, "songs")
    for f in sorted(os.listdir(sd)) if os.path.isdir(sd) else []:
        if f.endswith(".cho") and os.path.normpath(os.path.join(sd, f)) not in listed:
            warnings.append(f"tunas/{i}/songs/{f} exists but is not listed in tuna.json")

for w in warnings: print("warning:", w)
for e in errors: print("error:", e)
print(f"{len(ids)} tunas checked, {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
