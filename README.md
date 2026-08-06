# Ivan Shamrai CV

The CV is a Jekyll site with one content source: `_data/data.yml`.

## Local preview

```bash
docker compose up
```

Open `http://localhost:4000/cv/` for the website and
`http://localhost:4000/cv/print/` for the A4 print view.

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
jekyll build
python3 scripts/inject_pdf_metadata.py raw.pdf assets/Ivan_Shamrai_CV.pdf
```

The script reads `_site/profile.json` and requires `pypdf`. Keep the generated
PDF text-based so ATS and accessibility tools can extract its content.
