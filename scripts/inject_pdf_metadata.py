#!/usr/bin/env python3
"""Inject factual CV metadata from _data/data.yml into a text-based PDF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_pdf", type=Path)
    parser.add_argument(
        "--profile-json", type=Path, default=Path("_site/profile.json")
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = json.loads(args.profile_json.read_text(encoding="utf-8"))
    machine = data["machine_profile"]
    profile = data["profile"]

    keywords = machine.get("keywords", []) + machine.get("technologies", [])
    reader = PdfReader(args.input_pdf)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.add_metadata(
        {
            "/Title": machine["title"],
            "/Subject": machine["summary"],
            "/Author": profile["name"],
            "/Keywords": ", ".join(keywords),
            "/Creator": "Ivan Shamrai CV",
        }
    )
    args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with args.output_pdf.open("wb") as output:
        writer.write(output)


if __name__ == "__main__":
    main()
