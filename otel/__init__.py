from .otel_setup import setup_otel
from .metrics import (
    search_counter,
    search_duration,
    search_comparisons,
    search_text_size,
    search_occurrences,
)

__all__ = [
    "setup_otel",
    "search_counter",
    "search_duration",
    "search_comparisons",
    "search_text_size",
    "search_occurrences",
]
