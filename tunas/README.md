# tunas/

One folder per tuna. The website loads every folder listed in `index.json`.

```
tunas/<id>/
  tuna.json      name, city, beca colour, links, songs, photos, recordings, albums (Spotify etc.)
  historia.md    short history of the tuna (plain text paragraphs; first line "# Historia")
  songs/         one ChordPro file (.cho) per song
  parts/         melodies, tabs and sheet music, one subfolder per song (see below)
  photos/        photos of the tuna (JPG/PNG/WebP, under ~500 KB each)
```

Start from `_plantilla/`: copy it to `tunas/<your-tuna>/`, fill in `tuna.json`, add `<your-tuna>` to `index.json`, open a pull request.

Folders whose `tuna.json` has `"status": "pendiente"` are shown on the site as reserved but not yet filled in. Remove that line once the tuna has songs.

## songs/

ChordPro, one song per file, file name in lowercase with underscores (`tuna_compostelana.cho`). List every file under `songs` in `tuna.json`; files that aren't listed are not shown (Ciudad de Luz keeps unfinished songs in `songs/borradores/`).

Songs from different tunas are grouped on the site by `{title}`, so use the common title of the song.

## parts/

Everything beyond chords: melody, bandurria/laúd tabs, guitarrón lines, percussion, scans of old paper sheets. Keep originals as they are, in whatever format they exist:

```
parts/<song-file>/<instrument>-<what>.<ext>

parts/fonseca/bandurria-melodia.musicxml
parts/fonseca/bandurria-melodia-scan-1998.jpg
parts/fonseca/laud-tab.pdf
parts/clavelitos/voz-melodia.ly
```

Instruments: `voz`, `bandurria` (or `bandurria1`, `bandurria2`, `bandurria3` for a single voice), `laud`, `guitarra`, `guitarron`, `bajo`, `contrabajo`, `cuatro`, `acordeon`, `trompeta`, `pandereta`, `percusion`, and `todos` for a full score. What: `partitura`, `melodia`, `letra`, `tab`, `midi`, `musescore`, `scan`; add `-2`, `-3` when there is more than one (`laud-partitura-2.pdf`). Preferred digital format is MusicXML (`.musicxml`); scans (`.jpg`, `.pdf`), LilyPond (`.ly`), MuseScore (`.mscz`), Guitar Pro (`.gp5`) and MIDI (`.mid`) are all welcome as originals.

The site can't list folders, so it reads `parts/index.json` (folder → song title and files). After adding or removing files, run `python3 tools/parts_index.py`; `tools/check.py` fails while the index is out of date. A folder with the same name as a file in `songs/` is shown on that song's page; any other folder shows up as a song with sheet music but no chords yet, under the title in the index.

Audio and video don't go in the repository (too big for git). Link them as `recordings` in `tuna.json` instead.
