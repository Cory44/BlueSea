"""Utility helpers for determining if content relates to marine topics."""

from __future__ import annotations

from typing import Final, Optional

# A curated list of keywords associated with marine and oceanic topics.
MARINE_KEYWORDS: Final = (
    "algae",
    "aquatic",
    "bay",
    "beach",
    "boat",
    "buoy",
    "coast",
    "coastal",
    "coral",
    "crab",
    "current",
    "dolphin",
    "estuary",
    "fish",
    "fishing",
    "harbor",
    "kelp",
    "lagoon",
    "marine",
    "nautical",
    "ocean",
    "reef",
    "sail",
    "sailing",
    "sea",
    "seabird",
    "seagrass",
    "seashell",
    "seawater",
    "shellfish",
    "shore",
    "tidal",
    "tide",
    "turtle",
    "waterway",
    "wave",
    "whale",
)


def is_marine(text: Optional[str]) -> bool:
    """Return ``True`` when the provided ``text`` references marine topics.

    The check performs a simple case-insensitive keyword lookup against
    :data:`MARINE_KEYWORDS`. Non-string or empty inputs yield ``False``.
    """

    if not text or not isinstance(text, str):
        return False

    normalized = text.casefold()
    return any(keyword in normalized for keyword in MARINE_KEYWORDS)


__all__ = ["is_marine", "MARINE_KEYWORDS"]
