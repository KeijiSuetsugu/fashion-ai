"""Outfit planning logic that simulates AI-driven styling suggestions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional

from .items import CATALOG, FashionItem

DEFAULT_CATEGORIES = [
    "face",
    "top",
    "outerwear",
    "bottom",
    "footwear",
    "socks",
    "accessory",
    "bag",
]


@dataclass
class OutfitSuggestion:
    """Represents a cohesive outfit recommendation."""

    items: Dict[str, FashionItem | str]
    rationale: List[str] = field(default_factory=list)

    def to_prompt(self) -> str:
        """Serialize the outfit in a human-friendly prompt string."""

        lines = ["提案されたAIコーディネート:"]
        for category, item in self.items.items():
            if isinstance(item, FashionItem):
                lines.append(f"- {category.title()}: {item.name}")
            else:
                lines.append(f"- {category.title()}: {item}")
        if self.rationale:
            lines.append("\n選定理由:")
            lines.extend(f"* {reason}" for reason in self.rationale)
        return "\n".join(lines)


class OutfitPlanner:
    """Rule-based planner that mimics AI outfit curation."""

    def __init__(self, catalog: Iterable[FashionItem] | None = None):
        self.catalog = list(catalog or CATALOG)
        self.catalog_by_category: Dict[str, List[FashionItem]] = {}
        for item in self.catalog:
            self.catalog_by_category.setdefault(item.category, []).append(item)

    def suggest_outfit(
        self,
        preferences: Mapping[str, Iterable[str]] | None = None,
        required_categories: Iterable[str] | None = None,
        face_reference: str | None = None,
    ) -> OutfitSuggestion:
        """Generate an outfit based on the provided preferences."""

        preferences = {k: [v.lower() for v in values] for k, values in (preferences or {}).items()}
        categories = list(required_categories or DEFAULT_CATEGORIES)

        selected: MutableMapping[str, FashionItem | str] = {}
        rationale: List[str] = []

        if face_reference:
            selected["face"] = face_reference
            rationale.append("顔画像は提供された参照を活用してAI合成します。")
        elif "face" in categories:
            selected["face"] = "ユーザーの顔写真を活用"

        for category in categories:
            if category == "face":
                continue
            candidates = self.catalog_by_category.get(category, [])
            filtered = self._filter_candidates(candidates, preferences)
            item = self._choose_best_item(category, filtered, preferences)
            if item:
                selected[category] = item
                rationale.extend(self._build_rationale(category, item, preferences))
            else:
                selected[category] = "AIが該当カテゴリのアイテムを見つけられませんでした"
                rationale.append(f"{category}カテゴリで条件に合うアイテムがなかったため追加選定を推奨。")

        return OutfitSuggestion(items=dict(selected), rationale=rationale)

    def _filter_candidates(
        self,
        candidates: Iterable[FashionItem],
        preferences: Mapping[str, Iterable[str]],
    ) -> List[FashionItem]:
        styles = preferences.get("style", [])
        colors = preferences.get("color", [])
        seasons = preferences.get("season", [])
        weather = preferences.get("weather", [])

        filtered: List[FashionItem] = []
        for item in candidates:
            if not item.matches_style(styles):
                continue
            if not item.matches_color(colors):
                continue
            if not item.matches_season(seasons):
                continue
            if not item.matches_weather(weather):
                continue
            filtered.append(item)
        return filtered or list(candidates)

    def _choose_best_item(
        self,
        category: str,
        candidates: List[FashionItem],
        preferences: Mapping[str, Iterable[str]],
    ) -> Optional[FashionItem]:
        if not candidates:
            return None

        preferred_names = {name.lower() for name in preferences.get("favorites", [])}
        for candidate in candidates:
            if candidate.name.lower() in preferred_names:
                return candidate

        # Fallback: choose the candidate with the most overlapping style tags.
        desired_styles = set(preferences.get("style", []))
        ranked = sorted(
            candidates,
            key=lambda item: len(item.style_tags & desired_styles),
            reverse=True,
        )
        return ranked[0]

    def _build_rationale(
        self,
        category: str,
        item: FashionItem,
        preferences: Mapping[str, Iterable[str]],
    ) -> List[str]:
        reasons: List[str] = []
        styles = preferences.get("style", [])
        colors = preferences.get("color", [])
        seasons = preferences.get("season", [])

        if styles and item.matches_style(styles):
            reasons.append(
                f"{category}は{', '.join(styles)}スタイルのキーワードにマッチしています。"
            )
        if colors and item.matches_color(colors):
            reasons.append(
                f"カラーパレット({', '.join(colors)})に調和する色味です。"
            )
        if seasons and item.matches_season(seasons):
            reasons.append(
                f"指定されたシーズン({', '.join(seasons)})で着用しやすいアイテムです。"
            )
        if not reasons:
            reasons.append(f"{item.name}はカテゴリ{category}でバランスの良い選択肢です。")
        return reasons
