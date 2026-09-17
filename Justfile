set shell := ["bash", "-cu"]

raw_pdf := "raw.pdf"
final_pdf := "assets/Ivan_Shamrai_CV.pdf"
profile_json := "_site/profile.json"
site_url := "http://127.0.0.1:4000/cv/"
print_url := "http://127.0.0.1:4000/cv/print/"
chrome := env_var_or_default("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

# Show available commands.
default:
    @just --list

# Install Python dependencies used by PDF metadata injection.
deps:
    python3 -m pip install pypdf

# Start local Jekyll preview at http://127.0.0.1:4000/cv/.
serve:
    docker compose up

# Start local Jekyll preview in the background and wait until it is ready.
up:
    docker compose up -d
    for i in {1..60}; do \
      if curl -fsS "{{print_url}}" >/dev/null; then exit 0; fi; \
      sleep 1; \
    done; \
    echo "Timed out waiting for {{print_url}}" >&2; \
    exit 1

# Stop the background Jekyll preview.
down:
    docker compose down

# Build static site under _site/.
build:
    docker compose run --rm jekyll jekyll build

# Generate the machine-readable profile at _site/profile.json.
profile: build
    test -s "{{profile_json}}"
    @echo "Generated {{profile_json}}"

# Generate raw text-based PDF from the /print/ page.
raw-pdf: up
    test -x "{{chrome}}" || { echo "Chrome not found. Set CHROME=/path/to/chrome and retry." >&2; exit 1; }
    "{{chrome}}" \
      --headless \
      --disable-gpu \
      --no-pdf-header-footer \
      --print-to-pdf="{{raw_pdf}}" \
      "{{print_url}}"
    test -s "{{raw_pdf}}"
    @echo "Generated {{raw_pdf}}"

# Inject CV metadata into the final PDF.
pdf-metadata:
    python3 scripts/inject_pdf_metadata.py "{{raw_pdf}}" "{{final_pdf}}"
    test -s "{{final_pdf}}"
    @echo "Generated {{final_pdf}}"

# Generate the final PDF from current site data.
pdf: raw-pdf pdf-metadata

# Generate static site, profile JSON, raw PDF, and final metadata-enriched PDF.
all: profile pdf

# Remove generated outputs.
clean:
    rm -rf _site .sass-cache .jekyll-cache
    rm -f "{{raw_pdf}}" "{{final_pdf}}"
