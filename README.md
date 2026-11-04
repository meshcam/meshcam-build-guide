# MeshCam build guide

The public guide for turning a MeshCam leaf board into a working solar trail
camera node. Published at https://docs.getmeshcam.com/build/.

Corrections and clearer wording are welcome as issues or pull requests.

## What is here

| File | What it is |
| --- | --- |
| `docs/*.md` | The chapters, one Markdown file each. |
| `docs/img/` | Photos. |
| `build.py` | The whole site generator, about 200 lines. Chapter order lives in its `CHAPTERS` list. |
| `template.html` | The one page layout every chapter is poured into. |
| `style.css` | The one stylesheet. No JavaScript anywhere. |
| `requirements.txt` | The one dependency, Python-Markdown, pinned with hashes. |

## Editing

Edit the Markdown under `docs/`. To add a chapter, create `docs/<name>.md`
starting with a `# Title` line, and add `("<name>", "Nav label")` to
`CHAPTERS` in `build.py` where it belongs in the reading order. It is
published at `/build/<name>/`.

Link to another chapter by its file name (`[First boot](first-boot.md)` or
`first-boot.md#the-microsd-card`). Put photos in `docs/img/` and reference
them with a relative path (`![caption](img/board-front.jpg)`). Keep each photo
at or under 1200 px on its long edge and around 200 KB; the site is read on
phones in garages.

Supported Markdown beyond the basics: tables, fenced code, and warning boxes:

```markdown
!!! warning "Title of the box"
    Indented body text.
```

Build and look at it locally:

```bash
python3 -m venv .venv && .venv/bin/pip install --require-hashes -r requirements.txt
.venv/bin/python build.py --out /tmp/preview/build
python3 -m http.server -d /tmp/preview 8000   # open http://127.0.0.1:8000/build/
```

Every link the pages carry starts with `/build/`, which is why the preview
builds into a directory named `build`. A plain `build.py` writes `site/`.

The build is strict. A link to a chapter that does not exist, an anchor that
is not a heading in that chapter, or a missing image stops it with an error
naming the file, rather than shipping a 404.

## What may appear here

Photographs of a built board, off-board parts, pinouts, wiring and assembly
steps. Not the PCB design files, the on-board bill of materials, component
designators, or close-ups annotated with them.

## Publishing

Every change merged to the default branch is built and published to
https://docs.getmeshcam.com/build/.

## License

Text and photos are licensed under Creative Commons Attribution-ShareAlike 4.0
International (CC BY-SA 4.0). See `LICENSE` and
https://creativecommons.org/licenses/by-sa/4.0/.
