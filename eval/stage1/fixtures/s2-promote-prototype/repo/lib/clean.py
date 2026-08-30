"""Example of this repo's lib/ conventions (the pattern to follow)."""
from typing import Tuple


def normalize_tag(tag: str) -> str:
    """Lowercase and trim a tag. Raise ValueError on empty input."""
    tag = tag.strip().lower()
    if not tag:
        raise ValueError("tag must be non-empty")
    return tag


def split_pair(text: str, sep: str = ":") -> Tuple[str, str]:
    """Split exactly once on sep; raise ValueError if sep is missing."""
    if sep not in text:
        raise ValueError(f"separator {sep!r} missing")
    left, right = text.split(sep, 1)
    return left.strip(), right.strip()
