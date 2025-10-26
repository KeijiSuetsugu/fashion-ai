"""Command line interface for generating AI-inspired fashion outfits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, Mapping

from fashion_ai import OutfitPlanner


def load_preferences(source: str | None) -> Mapping[str, Iterable[str]]:
    if not source:
        return {}
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Preference file not found: {source}")
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return {k: value if isinstance(value, list) else [value] for k, value in data.items()}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preferences",
        type=str,
        help="Path to a JSON file describing style preferences (style, color, season, weather, favorites).",
    )
    parser.add_argument(
        "--face",
        type=str,
        help="Path or identifier for the user's face reference to simulate swapping.",
    )
    parser.add_argument(
        "--categories",
        type=str,
        nargs="*",
        help="Explicit list of categories to include (defaults to tops, bottoms, footwear, etc.).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    preferences = load_preferences(args.preferences)
    planner = OutfitPlanner()
    suggestion = planner.suggest_outfit(
        preferences=preferences,
        required_categories=args.categories,
        face_reference=args.face,
    )
    print(suggestion.to_prompt())


if __name__ == "__main__":
    main()
