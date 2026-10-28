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

Instruments: `voz`, `bandurria`, `laud`, `guitarra`, `guitarron`, `contrabajo`, `cuatro`, `pandereta`, `percusion`. Preferred digital format is MusicXML (`.musicxml`); scans (`.jpg`, `.pdf`), LilyPond (`.ly`), Guitar Pro (`.gp5`) and MIDI (`.mid`) are all welcome as originals.
