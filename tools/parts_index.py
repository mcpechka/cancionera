"""Rebuild tunas/<id>/parts/index.json from the files in parts/<song>/.
The site can't list folders, so it reads this index. Titles already in the index are kept;
new folders get the {title} of songs/<song>.cho, or the folder name.
Usage: python3 tools/parts_index.py          (rewrite every index)
       python3 tools/parts_index.py --check  (exit code 1 if an index is out of date)"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
T = os.path.join(ROOT, "tunas")
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.[a-z0-9]+$")

def cho_title(base, folder):
    for p in (f"songs/{folder}.cho", f"songs/borradores/{folder}.cho"):
        try: m = re.search(r"^\{\s*(?:title|t)\s*:\s*(.*?)\s*\}", open(os.path.join(base, p), encoding="utf-8").read(), re.M | re.I)
        except OSError: continue
        if m: return m.group(1)
    return folder.replace("_", " ").capitalize()

def build(base):
    pd = os.path.join(base, "parts")
    try: old = json.load(open(os.path.join(pd, "index.json"), encoding="utf-8"))
    except (OSError, ValueError): old = {}
    out, bad = {}, []
    for folder in sorted(os.listdir(pd)) if os.path.isdir(pd) else []:
        d = os.path.join(pd, folder)
        if not os.path.isdir(d): continue
        files = sorted(f for f in os.listdir(d) if not f.startswith("."))
        bad += [f"{folder}/{f}" for f in files if not NAME.match(f)]
        if files: out[folder] = {"title": (old.get(folder) or {}).get("title") or cho_title(base, folder), "files": files}
    return out, bad

def main():
    check, stale, bad_all = "--check" in sys.argv, [], []
    for i in json.load(open(os.path.join(T, "index.json"))):
        base = os.path.join(T, i)
        idx, bad = build(base)
        bad_all += [f"tunas/{i}/parts/{b}: name it <instrument>-<what>.<ext> (lowercase, no spaces)" for b in bad]
        path = os.path.join(base, "parts", "index.json")
        text = json.dumps(idx, ensure_ascii=False, indent=1) + "\n" if idx else None
        cur = open(path, encoding="utf-8").read() if os.path.isfile(path) else None
        if text != cur:
            if check: stale.append(f"tunas/{i}/parts/index.json is out of date: run python3 tools/parts_index.py")
            elif text: open(path, "w", encoding="utf-8").write(text)
            elif cur is not None: os.remove(path)
    return stale, bad_all

if __name__ == "__main__":
    stale, bad = main()
    for m in stale + bad: print("error:" if m in stale else "warning:", m)
    sys.exit(1 if stale else 0)
