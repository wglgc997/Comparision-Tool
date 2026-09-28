"""
Comparison Engine
Compares source specs (Excel) against live specs (PDP page).
"""

def normalize(value):
    """
    Convert a specification value into a consistent comparison string.

    None, NaN, and pandas NA values become an empty string. Other values
    are converted to text, stripped, case-normalized, and reduced to single
    spaces between words.
    """
    if value is None:
        return ""

    try:
        if value != value:
            return ""
    except (TypeError, ValueError):
        pass

    normalized = " ".join(str(value).strip().casefold().split())

    if normalized in {"nan", "<na>"}:
        return ""

    return normalized