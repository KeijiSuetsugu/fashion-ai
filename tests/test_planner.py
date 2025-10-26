from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fashion_ai import OutfitPlanner


def test_planner_returns_all_default_categories():
    planner = OutfitPlanner()
    suggestion = planner.suggest_outfit()
    # Should cover face + default categories
    expected_categories = {"face", "top", "outerwear", "bottom", "footwear", "socks", "accessory", "bag"}
    assert expected_categories.issubset(set(suggestion.items.keys()))


def test_preferences_filtering_prefers_matching_style():
    planner = OutfitPlanner()
    suggestion = planner.suggest_outfit(preferences={"style": ["formal"]})
    top = suggestion.items.get("top")
    assert top is not None
    assert getattr(top, "style_tags", set())
    assert "formal" in getattr(top, "style_tags", set()) or "minimal" in getattr(top, "style_tags", set())
