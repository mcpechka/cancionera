# Cancionero Común

Shared songbook for tunas: every song once, with each tuna's version of it side by side. Transpose, switch between DO-RE-MI and C-D-E, and compare two versions with the chord differences highlighted.

**Site:** https://mcpechka.github.io/cancionera/

## How it works

The site (`index.html`) is a single static page. It reads `tunas/index.json`, each tuna's `tuna.json` and the ChordPro song files they list, and builds the songbook in the browser. There is no server or database: the repository is the database, and changes arrive through pull requests.

```
tunas/
  index.json            which tuna folders the site loads
  _plantilla/           template to copy for a new tuna
  ciudad-de-luz/        Tuna Ciudad de Luz, 52 songs
    tuna.json  historia.md  songs/  parts/  photos/
  maastricht/  medicina-navarra/  empresariales-huelva/  uaa/   reserved, still empty
tools/
  tex2cho.py            converts the Tunabundel LaTeX songs to ChordPro
  check.py              checks the tunas/ folder (runs on every push and pull request)
docs/CANCIONERO.md      system overview, formats, known issues, roadmap
```

## Add your tuna

1. Fork this repository.
2. Copy `tunas/_plantilla/` to `tunas/<your-tuna>/` (or use the reserved folder for your tuna) and fill in `tuna.json`.
3. Add your songs to `songs/` as ChordPro (`.cho`) and list them in `tuna.json`. Melodies, tabs and scans go in `parts/`, photos in `photos/`, a short history in `historia.md`. Details in [`tunas/README.md`](tunas/README.md).
4. Add the folder name to `tunas/index.json` if it's new, run `python3 tools/check.py`, and open a pull request.

## Run locally

```
python3 -m http.server
```

then open http://localhost:8000. (Opening `index.html` directly as a file doesn't work, because the browser blocks reading the song files.)

## Tuna Ciudad de Luz songs

Generated from the LaTeX bundel in [mcpechka/tunabundel](https://github.com/mcpechka/tunabundel):

```
python3 tools/tex2cho.py ../tunabundel/bundel/songs tunas/ciudad-de-luz/songs
```

See [`docs/CANCIONERO.md`](docs/CANCIONERO.md) for the full background and roadmap.
