#!/usr/bin/env python3
"""Inject factual CV metadata into a text-based PDF."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


DEFAULT_PROFILE_PATHS = (Path("_site/profile.json"), Path("_data/data.yml"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inject factual CV metadata into a text-based PDF."
    )
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_pdf", type=Path)
    parser.add_argument(
        "--profile-json",
        type=Path,
        default=None,
        help=(
            "Path to generated JSON profile. If omitted, the script uses "
            "_site/profile.json when present, otherwise _data/data.yml."
        ),
    )
    return parser.parse_args()


def load_profile(path: Path | None) -> dict:
    if path is None:
        path = next((candidate for candidate in DEFAULT_PROFILE_PATHS if candidate.exists()), None)
        if path is None:
            candidates = ", ".join(str(candidate) for candidate in DEFAULT_PROFILE_PATHS)
            raise FileNotFoundError(f"No profile data found. Expected one of: {candidates}")

    if not path.exists():
        raise FileNotFoundError(f"Profile data file not found: {path}")

    if path.suffix.lower() in {".yml", ".yaml"}:
        try:
            import yaml
        except ModuleNotFoundError as exc:
            try:
                result = subprocess.run(
                    [
                        "ruby",
                        "-ryaml",
                        "-rjson",
                        "-e",
                        "puts YAML.load_file(ARGV[0]).to_json",
                        str(path),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except (FileNotFoundError, subprocess.CalledProcessError) as ruby_exc:
                raise RuntimeError(
                    "Reading YAML profile data requires PyYAML or Ruby. "
                    "Install PyYAML with: pip3 install pyyaml"
                ) from ruby_exc
            return json.loads(result.stdout)
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    text = path.read_text(encoding="utf-8").strip()
    if text.startswith("---") or "{{" in text:
        raise ValueError(
            f"{path} is a Jekyll template, not generated JSON. Run `jekyll build` "
            "and use `_site/profile.json`, or omit `--profile-json` to read "
            "`_data/data.yml` directly."
        )
    return json.loads(text)


def main() -> None:
    args = parse_args()
    try:
        data = load_profile(args.profile_json)
    except (FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

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
