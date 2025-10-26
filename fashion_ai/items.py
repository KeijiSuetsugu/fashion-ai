"""Fashion item definitions and curated sample catalog."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Sequence, Set


@dataclass(frozen=True)
class FashionItem:
    """Represents a single fashion item that can appear in an outfit."""

    name: str
    category: str
    style_tags: Set[str] = field(default_factory=set)
    colors: Set[str] = field(default_factory=set)
    season: Set[str] = field(default_factory=set)
    weather: Set[str] = field(default_factory=set)

    def matches_style(self, desired_styles: Iterable[str]) -> bool:
        if not desired_styles:
            return True
        desired = {style.lower() for style in desired_styles}
        return "all" in self.style_tags or bool(self.style_tags & desired)

    def matches_color(self, desired_colors: Iterable[str]) -> bool:
        if not desired_colors:
            return True
        desired = {color.lower() for color in desired_colors}
        return "all" in self.colors or bool(self.colors & desired)

    def matches_season(self, desired_seasons: Iterable[str]) -> bool:
        if not desired_seasons:
            return True
        desired = {season.lower() for season in desired_seasons}
        return "all" in self.season or bool(self.season & desired)

    def matches_weather(self, desired_weather: Iterable[str]) -> bool:
        if not desired_weather:
            return True
        desired = {w.lower() for w in desired_weather}
        return "all" in self.weather or bool(self.weather & desired)


# A curated catalog of diverse fashion items. In a production system this would be
# backed by a database or API. Here we supply a small but expressive sample.
CATALOG: List[FashionItem] = [
    FashionItem(
        name="Oversized White Shirt",
        category="top",
        style_tags={"minimal", "casual"},
        colors={"white"},
        season={"spring", "summer", "fall"},
        weather={"mild", "warm"},
    ),
    FashionItem(
        name="Tailored Black Blazer",
        category="outerwear",
        style_tags={"formal", "modern"},
        colors={"black"},
        season={"spring", "fall", "winter"},
        weather={"cool", "cold"},
    ),
    FashionItem(
        name="Denim High-Waist Jeans",
        category="bottom",
        style_tags={"casual", "street"},
        colors={"blue"},
        season={"spring", "summer", "fall"},
        weather={"mild", "warm"},
    ),
    FashionItem(
        name="Pleated Midi Skirt",
        category="bottom",
        style_tags={"romantic", "formal"},
        colors={"beige", "pink"},
        season={"spring", "summer"},
        weather={"mild", "warm"},
    ),
    FashionItem(
        name="Wide-Leg Trousers",
        category="bottom",
        style_tags={"formal", "minimal"},
        colors={"black", "cream"},
        season={"spring", "fall", "winter"},
        weather={"cool", "cold"},
    ),
    FashionItem(
        name="Chunky Knit Sweater",
        category="top",
        style_tags={"cozy", "minimal"},
        colors={"cream", "beige"},
        season={"fall", "winter"},
        weather={"cool", "cold"},
    ),
    FashionItem(
        name="Silk Camisole",
        category="top",
        style_tags={"romantic", "formal"},
        colors={"champagne", "black"},
        season={"summer"},
        weather={"warm"},
    ),
    FashionItem(
        name="Statement Leather Belt",
        category="accessory",
        style_tags={"modern", "street"},
        colors={"black", "brown"},
        season={"all"},
        weather={"all"},
    ),
    FashionItem(
        name="Minimalist Tote Bag",
        category="bag",
        style_tags={"minimal", "modern"},
        colors={"black", "tan"},
        season={"all"},
        weather={"all"},
    ),
    FashionItem(
        name="White Leather Sneakers",
        category="footwear",
        style_tags={"casual", "minimal"},
        colors={"white"},
        season={"spring", "summer", "fall"},
        weather={"mild", "warm"},
    ),
    FashionItem(
        name="Pointed Toe Heels",
        category="footwear",
        style_tags={"formal", "romantic"},
        colors={"black", "nude"},
        season={"spring", "summer", "fall"},
        weather={"mild", "warm"},
    ),
    FashionItem(
        name="Wool Overcoat",
        category="outerwear",
        style_tags={"formal", "minimal"},
        colors={"camel", "gray"},
        season={"fall", "winter"},
        weather={"cool", "cold"},
    ),
    FashionItem(
        name="Patterned Silk Scarf",
        category="accessory",
        style_tags={"romantic", "modern"},
        colors={"red", "navy"},
        season={"all"},
        weather={"all"},
    ),
    FashionItem(
        name="Crew Socks",
        category="socks",
        style_tags={"casual", "minimal"},
        colors={"white", "black", "gray"},
        season={"all"},
        weather={"all"},
    ),
    FashionItem(
        name="Sheer Tights",
        category="socks",
        style_tags={"formal", "romantic"},
        colors={"black"},
        season={"fall", "winter"},
        weather={"cool", "cold"},
    ),
]


def items_by_category(category: str, catalog: Sequence[FashionItem] | None = None) -> List[FashionItem]:
    """Return all items in the catalog that belong to ``category``."""

    catalog = catalog or CATALOG
    category = category.lower()
    return [item for item in catalog if item.category == category]
