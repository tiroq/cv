# Ivan Shamrai CV

The CV is a Jekyll site with one content source: `_data/data.yml`.

## Local preview

```bash
just serve
```

Open `http://localhost:4000/cv/` for the website and
`http://localhost:4000/cv/print/` for the A4 print view.

## Generation commands

The project uses `Justfile` as the main command entrypoint:

```bash
just deps       # install Python dependencies for PDF metadata
just build      # generate the static Jekyll site in _site/
just profile    # generate and verify _site/profile.json
just raw-pdf    # export the print page to raw.pdf
just pdf        # generate assets/Ivan_Shamrai_CV.pdf with metadata
just all        # run the full generation flow
just clean      # remove generated outputs
```

## Machine-readable profile

`machine_profile` in `_data/data.yml` controls factual classification metadata:

- HTML meta fields and JSON-LD;
- the public `/profile.json` machine-readable profile;
- optional visible machine-readable profile;
- PDF title, subject, author, and keywords.

The metadata must contain verifiable professional facts, not prompts or
instructions intended to influence an automated decision.

## PDF metadata

Build the site, export the `/print/` page to a text-based PDF, then inject the
configured metadata:

```bash
just pdf
```

The script reads `_site/profile.json` and requires `pypdf`. Keep the generated
PDF text-based so ATS and accessibility tools can extract its content.

If `_site/profile.json` is not available, the script reads `_data/data.yml`
directly. In that mode it uses `PyYAML` when installed, or Ruby's built-in
YAML support as a fallback:

```bash
pip3 install pypdf
python3 scripts/inject_pdf_metadata.py raw.pdf assets/Ivan_Shamrai_CV.pdf
```
