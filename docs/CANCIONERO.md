# Cancionero Común — system overview and roadmap

Background documentation for the Cancionero Común: a shared songbook website for tunas, in the repository `mcpechka/cancionera`. Read this before changing the site, the converter or the song files.

Status: October 2026. The site works and shows the 52 songs of Tuna Ciudad de Luz's current bundel; folders for four more tunas are reserved. Chords, melodies and tuna information still need work (see [Roadmap](#roadmap)).

---

## 1. What this is

Tuna Ciudad de Luz has kept its songbook (*bundel*) in LaTeX since 2015 (`bundel/`, custom package `tunaChords.sty`, see `documentation/HOWTO.MD` and `Feature list.txt`). The PDF is good to print, but the songs could only be read in the PDF and only edited by someone with a LaTeX setup.

The Cancionero Común adds three things on top of the bundel, without replacing it:

1. **ChordPro copies** of every song (`tunas/ciudad-de-luz/songs/*.cho`), generated from the bundel's `.tex` files. ChordPro is the plain-text standard most songbook apps and tools read.
2. **A website** (`index.html`, GitHub Pages) that shows the songs with transposing, DO-RE-MI / C-D-E notation and side-by-side comparison of versions.
3. **A folder per tuna** (`tunas/<id>/`) with room for songs, melodies and tabs, photos and history, so other tunas can add their own versions of the same songs. Tunas play the same repertoire with small differences in chords and structure; the site groups songs by title and highlights those differences.

## 2. System overview

```mermaid
flowchart LR
  subgraph bundel["repo mcpechka/tunabundel"]
    tex["bundel/songs/*.tex<br/>(source for Ciudad de Luz)"]
    pdf["Tunabundel PDF<br/>(pdflatex)"]
  end
  subgraph cc["repo mcpechka/cancionera"]
    conv["tools/tex2cho.py"]
    cdl["tunas/ciudad-de-luz/songs/*.cho"]
    other["tunas/&lt;other tuna&gt;/songs/*.cho<br/>(written directly in ChordPro)"]
    idx["tunas/index.json + tuna.json"]
    site["index.html"]
    chk["tools/check.py<br/>(GitHub Action)"]
  end
  tex --> pdf
  tex --> conv --> cdl --> idx
  other --> idx --> site --> pages["GitHub Pages<br/>mcpechka.github.io/cancionera"]
  idx -.-> chk
```

- **Two repositories.** `tunabundel` keeps the LaTeX bundel (and stays the source for Tuna Ciudad de Luz's songs while the tuna prints from LaTeX). `cancionera` holds the website and every tuna's material. Ciudad de Luz's `.cho` files are generated from the `.tex` (section 5); other tunas write ChordPro directly. If Ciudad de Luz drops LaTeX later, its `.cho` files become the source and `tools/tex2cho.py` can be retired.
- **The website is static.** It has no server and no database. On page load it reads `tunas/index.json`, then each tuna's `tuna.json`, then every song file listed there, and builds the songbook in the browser. Changing the repo changes the site on the next GitHub Pages build (about a minute).
- **Contributions go through pull requests.** Nobody edits on the website itself.

### 2.1 Second copy on claude.ai (not synced)

There is also an editable version of the songbook published as a Claude artifact. It stores songs in its own database, lets invited people add versions and recordings in the browser, and can import `.tex` and PDF songbooks. It does **not** sync with this repo. Treat the GitHub site as the main one; the artifact is useful for quick experiments and has an "Exportar copia" button that downloads everything as JSON.

## 3. Repository layout

**cancionera**

| Path | What it is |
|---|---|
| `index.html` | The website (single file, no build step) |
| `tunas/index.json` | List of tuna folders the site loads |
| `tunas/<id>/tuna.json` | One tuna: name, city, beca colour, links, songs, photos, recordings |
| `tunas/<id>/songs/` | ChordPro songs (`borradores/` for unfinished, unlisted songs) |
| `tunas/<id>/parts/` | Melodies, tabs, sheet music and scans, one subfolder per song (see `tunas/README.md`) |
| `tunas/<id>/photos/` | Photos of the tuna |
| `tunas/<id>/historia.md` | Short history |
| `tunas/_plantilla/` | Template folder to copy for a new tuna |
| `tools/tex2cho.py` | LaTeX → ChordPro converter for the Tunabundel format |
| `tools/check.py` | Checks `tunas/` (JSON, files exist, ChordPro sections balanced); runs on every push and pull request |
| `docs/CANCIONERO.md` | This document |

Reserved folders (`"status": "pendiente"`) exist for the tunas whose songbooks are in `tunabundel/documentation/Extra Bundels voor research/`: `maastricht`, `medicina-navarra` (Pamplona), `empresariales-huelva`, `uaa`. Names marked "por confirmar" in their `tuna.json` were guessed from those PDFs and need checking.

**tunabundel** (relevant parts)

| Path | What it is |
|---|---|
| `bundel/songs/*.tex` | One LaTeX file per song (74, 5 of them empty templates) |
| `bundel/Tunabundel2.tex` | Main bundel; its `\input{songs/...}` lines decide which songs are in the current edition (52) |
| `bundel/tunaChords.sty` | The LaTeX package (`song`, `verse`, `instrumental`, `\chord`, `\measure`, …), see `documentation/HOWTO.MD` |
| `bundel/theory/` | Chord charts, rhythms (*slagjes*), pronunciation guides, singing workshop |
| `bundel/setlist.tex`, `festivalbundel.tex` | Setlist and festival songbooks |
| `Songs to do/`, `Banduriabundel/` | Unfinished songs, bandurria melodies (zipped) |
| `Cancionero de Tuna Ciudad de Luz 2004.pdf` | The 2004 edition |
| `documentation/Extra Bundels voor research/` | Songbooks of other tunas |

## 4. Formats

### 4.1 `tunas/<id>/tuna.json`

```json
{
  "name": "Tuna Ciudad de Luz",
  "city": "Eindhoven",
  "country": "Países Bajos",
  "founded": 2001,
  "beca": "burdeos",
  "web": "https://…",
  "notes": "Short description shown on the tuna card",
  "label": "",
  "status": "pendiente",
  "songs": ["songs/adelita.cho", "songs/fonseca.cho"],
  "photos": [{ "file": "photos/ronda-2025.jpg", "caption": "Ronda, 2025" }],
  "recordings": [
    { "song": "Fonseca", "title": "Certamen 2025", "date": "2025-05-10",
      "event": "Certamen de tunas", "url": "https://www.youtube.com/watch?v=…" }
  ]
}
```

- `songs`: paths relative to the tuna's folder (a leading `/` means the repo root). `.cho`, `.chopro`, `.txt` (ChordPro) and `.tex` (Tunabundel format) are read.
- `status`: `"pendiente"` shows the tuna as reserved; remove it once there are songs.
- `photos`: JPG/PNG/WebP files in `photos/`; the first one is shown on the tuna card.
- `historia.md` is shown on the tuna card as "Historia" (plain paragraphs).
- `artist`: the tuna's profile on music platforms, `{ "spotify": "https://open.spotify.com/artist/…", "youtube": "…" }`. Shown as buttons on the tuna card.
- `albums`: `[{ "title", "year", "cover", "links": { "spotify": "…", "apple_music": "…", … }, "tracks": ["Fonseca", …] }]`. Shown on the *Discos* page. `cover` is a file in the tuna folder or an https URL. `tracks` are matched to songs by title, so each song page lists the albums it's on and each track links to its song.

### 4.1.1 Music platforms

The site has a small registry, `PLATFORMS` in `index.html`. Each entry has a name, a colour, a pattern that recognises its links and, optionally, a function that turns a link into an embeddable player. Current entries:

| Key | Platform | Player on the site |
|---|---|---|
| `spotify` | Spotify | yes (album, track, playlist, artist) |
| `apple_music` | Apple Music | yes |
| `youtube` | YouTube / YouTube Music | yes (video or playlist, via youtube-nocookie) |
| `deezer` | Deezer | yes |
| `soundcloud` | SoundCloud | yes |
| `bandcamp`, `amazon_music`, `tidal` | | link only |

Players are loaded only when someone presses *Escuchar aquí*, because embedding them sets the platform's cookies. Unknown keys still work as plain links. Adding a platform is one new entry in `PLATFORMS`; nothing else changes.

There is no Spotify API call: the site only needs the public links, so no keys or accounts are involved. Covers and track lists come from `tuna.json`, not from Spotify.
- `beca`: one of `burdeos granate rojo naranja amarillo verde turquesa celeste azul morado rosa negro plata blanco`, or a hex colour like `#1f4e9c`.
- `label`: optional text shown after the tuna name on every version (e.g. `"2004"` for an old edition).
- `recordings[].song` is matched to a song by title, the same way versions are.
- **Missing for Ciudad de Luz:** `city`, `country`, `founded`, `beca` and `web` are still empty.

### 4.2 ChordPro conventions used here

| In the `.cho` file | Meaning | From LaTeX |
|---|---|---|
| `{title}`, `{key}`, `{time}` | Title, key, time signature | `\begin{song}`, `\rhythmandkey` |
| `{meta: rhythm Vals}` | Rhythm/style; the site maps it to a genre filter | `\rhythmandkey{Vals}` or the song option `[vals]` |
| `{start_of_verse: Couplet 1}` … `{end_of_verse}` | A verse | `verse` environment |
| `{start_of_chorus: Refrein}` … `{end_of_chorus}` | A chorus (any section whose name starts with Refrein/Refrain/Estribillo/Coro) | `verse` environment |
| `{chorus: Refrein}` | Repeat the chorus | `\repetition{Refrein}` |
| `{comment: …}` | Performance notes, repeats of other sections | `\repetition{…}`, `sidenote`, loose `\textbf{…}` notes |
| `[Am]` before a syllable | Chord on that syllable | `\chord{Am}` |
| `[*50 52 53]` | Annotation, shown grey, never transposed: bandurria tab numbers, remarks | `\chord{\underline{…}}`, `\tiny{\underline{…}}` |
| `{define: Edim base-fret 1 frets x 1 2 0 2 0}` | Chord diagram | `\chord{Edim: x-1-2-0-2-0}` |
| `\| [G] \| . \| [D] [A7] \| [D] : \|` | Bar grid: one cell per measure, `.` = empty beat or bar, `:` at the start/end of a cell = repeat sign, `(2x)` = repeat count | `instrumental` + `\measure{…;…}[:]` |

Grid rows follow the bars-per-row option of `\begin{instrumental}{…}[N]` (default 8, as in `tunaChords.sty`). Beats inside a measure (`\measure{Am;E}`) become `[Am] [E]`.

Not carried over: the Dutch translations (`translation` environment), strum arrows (↓ ↑) and the `°` symbols in measures, `\hspace`/layout commands, `tabular` blocks, `\notition` pages.

All files parse with the ChordPro parser used by most JavaScript songbook tools (chordsheetjs).

### 4.3 Bandurria tab numbers

The bundel writes bandurria/laúd notes as two-digit numbers (`50 52 53`, `60 64 62`). **The meaning of these numbers is not written down anywhere in the repo.** Add it to `HOWTO.MD` (string and fret? which string is 1?) before anyone builds a tab renderer on top of it.

## 5. How-tos

**Edit a Ciudad de Luz song**
1. Edit `bundel/songs/<song>.tex` in `tunabundel` (see its `documentation/HOWTO.MD`).
2. In a checkout of `cancionera` next to it, regenerate:
   `python3 tools/tex2cho.py ../tunabundel/bundel/songs tunas/ciudad-de-luz/songs`
   This writes all songs into `songs/`; move songs that aren't in `Tunabundel2.tex` back into `songs/borradores/` (or only commit the files you changed).
3. Run `python3 tools/check.py`, commit, push.

**Edit another tuna's song:** edit its `.cho` directly.

**Add a song to the site:** put the `.cho` in `tunas/<id>/songs/` and add it to `songs` in `tuna.json`.

**Add a tuna:** fork, copy `tunas/_plantilla/` to `tunas/<id>/` (or fill in the reserved folder), fill in `tuna.json`, add `<id>` to `tunas/index.json` if new, run `python3 tools/check.py`, open a pull request. The site's *Añade tu tuna* tab shows the same steps.

**Add melody, tabs or scans:** `tunas/<id>/parts/<song-file>/<instrument>-<what>.<ext>`, see `tunas/README.md`. The site doesn't show these yet (roadmap B).

**Publish:** GitHub → Settings → Pages → Deploy from branch `main`, folder `/ (root)`. The site is then at `https://mcpechka.github.io/cancionera/`.

**Test locally:** `python3 -m http.server` in the repo root, open `http://localhost:8000`. Opening `index.html` as a file does not work, because the browser blocks reading the song files.

## 6. Known issues

### 6.1 Fixed in the converter (October 2026)

- *Cantar de Emigração*: every chord carried a bass tab (`Dm\tiny{\underline{40}}`) and was dropped. Now `[Dm][*40]`.
- Dutch accidentals (`Bes`, `Fis`) are converted to `Bb`, `F#`.
- Chords with a fingering star (`A7*`, `Bbm*`), chords with a tab in brackets (`Em(67/60)`), repeat colons in measures, beats inside measures, bars per row.
- Loose bold performance notes between sections (`\textbf{versnelling trom…}`) are kept as comments.

### 6.2 Needs a person (fix in the `.tex`, then regenerate)

Chord bodies the converter can't read are kept as grey annotations, so nothing is lost, but they don't transpose or compare. Likely typos or shorthand:

| Song file | Written as | Probably means |
|---|---|---|
| `granada.tex` | `EEE`, `G4-9`, several chords in brackets | check the original |
| `cintas_de_mi_capa.tex` | `AmEAm` | `Am E Am` as separate chords |
| `puntas.tex` | `FEm` | `F Em` |
| `caja_de_musica.tex` | `Em-D` | two chords |
| `amalia_rosa.tex` | `A7-D` | two chords |
| `venezuela.tex`, `siete_amores.tex`, `recuerdos.tex` | `A(C)`, `D(G)`, `Bm(Bm)` | alternative chord in brackets; decide on a convention (e.g. second guitar) |

Sections with no chords at all (could be spoken/a capella, could be missing): `la_banda`, `chan_chan`, `estudiantina_portuguesa`, `aqui_esta`, `caja_de_musica`, `don_quijote`, `elsa`.

Skipped because they have no content: `espana_cani`, `horas_de_rondas`, `luna_de_espana`, `quizas`, `tequila` (empty templates) and `cantinero_de_cuba`, `pajaro_choqui` (nothing but a translation).

Everyone who plays from the site should report songs that look wrong. A per-song checklist ("chords checked against how we play it, by whom, when") would make the review measurable; see roadmap item A.

### 6.3 Website limitations

- Read-only; changes go through GitHub.
- Songs are grouped by title. Two tunas spelling a title very differently ("Tuna Compostelana" vs "Pasa la tuna") end up as two songs; fix by aligning the `{title}`.
- Chord positions inside a word are as exact as the source. Long chord names can push text sideways on narrow phones.

## Roadmap

Ordered by how much it helps playing together. Each item says what "done" looks like.

### A. Fix chords and songs (now)

1. Go through the table in 6.2 and the chordless sections. Done when the converter reports no chord-like annotations.
2. Review every song against how the tuna actually plays it. Proposal: add `{meta: reviewed 2026-11 Egor}` to the `.tex`-generated file via a `% reviewed:` comment line that the converter copies, and show a "reviewed" badge on the site. Done when all 52 songs carry it.
3. Bring in the 17 commented-out songs and the *Songs to do* folder once they are complete.
4. `tools/check.py` already runs on every push. Extend it to warn when a Ciudad de Luz `.cho` is older than its `.tex` in `tunabundel`, so the two can't drift apart.

### B. Melody and other instruments

The material exists in many forms: printouts of old PDFs, photos of sheets that no longer exist, bandurria tabs, proper notation, LilyPond (`.ly`), Guitar Pro (`.gp5`), MIDI, and the zips in `Banduriabundel/`. There is no single format, so the plan is **collect first, digitise second**.

1. **Inventory.** One table (a CSV in `documentation/`) with a row per song × instrument (melody/voice, bandurria, laúd, guitar, guitarrón, cuatro, percussion) and columns: what exists, format, where it is, quality. This shows what's missing and what to digitise first.
2. **Store originals as-is** in `tunas/<id>/parts/<song-file>/` (folders already exist) (scans as JPG/PDF, `.ly`, `.gp5`, `.mid`, `.musicxml`), named `<instrument>-<what>.<ext>`, e.g. `parts/fonseca/bandurria-melodia.pdf`. The site lists them per song; images and PDFs are viewable immediately. Even an unreadable old photo is better than nothing.
3. **Digitise to one target format: MusicXML.** It is the exchange format every notation program reads (MuseScore, Sibelius, Dorico, LilyPond via `musicxml2ly`) and it can be rendered in the browser. Routes:
   - LilyPond files → export MusicXML (or keep `.ly` as source and export PDF + MIDI with `lilypond_export.sh`).
   - Scans and old PDFs → optical music recognition with Audiveris (free) or MuseScore's import, then correct by hand in MuseScore.
   - Guitar Pro → open in MuseScore or TuxGuitar, export MusicXML.
   - Bandurria number tabs → typed into MuseScore with a bandurria/laúd tab staff once the number system (4.3) is written down.
4. **Show it on the site:** render MusicXML with OpenSheetMusicDisplay (sheet music and tab, can transpose), play MIDI so people can learn a melody by ear, and later a "practice" mode that loops the intro at a chosen tempo.

Done when every song on the site has at least the melody in MusicXML or a readable scan.

### C. Tuna pages

- **Photos:** supported. Put files in `tunas/<id>/photos/` and list them in `tuna.json`; the first is shown on the tuna card. Next: a gallery per tuna. Keep files under ~500 KB so the repo stays fast.
- **Website and socials:** `web` exists; music platforms via `artist` and `albums` (section 4.1). Still to add: `instagram`, `contact`.
- **Discography:** fill in Ciudad de Luz's albums with their Spotify links.
- **History:** supported via `tunas/<id>/historia.md` (template text in every folder), a short overview (founding, notable trips and certámenes, traditions), rendered on the tuna card. For Ciudad de Luz the 2004 bundel, the 2015 LaTeX start and the festival bundels (Murcia, Torremolinos) are a starting timeline.
- **Beca colour and *estandarte*/logo** (`bundel/logo.eps` exists).

### D. Other ideas

- **Setlists:** `bundel/setlist.tex` and the festival bundels already exist. A `setlists/*.json` (name, date, ordered songs) shown as a page you can play through on a phone during a *ronda*, one song per swipe.
- **Print/PDF from the site:** generate a clean PDF per song or per setlist from ChordPro (the `chordpro` command-line tool can do this in a GitHub Action), for tunas that don't use LaTeX.
- **Theory pages:** move `bundel/theory/` (chord charts, *slagjes*/rhythms, pronunciation guides, singing workshop) onto the site. The pronunciation guide is especially useful for Dutch members.
- **Chord diagrams for the tuna's instruments:** guitar shapes exist via `{define}`; add bandurria/laúd shapes.
- **Search inside lyrics**, not only titles.
- **Offline use:** make the site installable on phones (a small service worker), so it works in a cellar or a square without signal.
- **Other tunas:** the songbooks in `documentation/Extra Bundels voor research/` show which tunas share the repertoire. They are a natural first list of tunas to invite, each adding their own versions (with their permission, not by copying their PDFs in).
- **Comments per song** ("we play the second couplet twice") through GitHub issues linked from each song page.
- **Invite the reserved tunas:** confirm the names in their `tuna.json` and send them the *Añade tu tuna* link.

## Credits

Bundel and `tunaChords.sty`: M. Heidweiller, Y. Haenen, R. Peters, S. van Himste (2015–2016). 2004 edition: Michiel, Peter and Robert. ChordPro conversion and website: 2026.
