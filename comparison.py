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


def parse_specs(text):
    """
    Parse lines in 'Checkpoint: Value' format into a dictionary.

    Blank lines, lines without a colon, and lines without a checkpoint name
    are ignored. Only the first colon separates the checkpoint from its value.
    """
    if not text:
        return {}

    specs = {}

    for line in text.splitlines():
        stripped_line = line.strip()

        if not stripped_line or ":" not in stripped_line:
            continue

        checkpoint, value = stripped_line.split(":", 1)
        checkpoint = checkpoint.strip()

        if not checkpoint:
            continue

        specs[checkpoint] = value.strip()

    return specs


def compare_specs(source_specs, live_specs):
    """
    Compare source specifications against live PDP specifications.

    Returns one result dictionary for every source checkpoint. Field names
    and values are normalized for comparison, while the original values are
    retained in the returned results for display.
    """
    normalized_live_specs = {
        normalize(field): value
        for field, value in live_specs.items()
    }

    results = []

    for checkpoint, expected in source_specs.items():
        normalized_checkpoint = normalize(checkpoint)
        actual = normalized_live_specs.get(normalized_checkpoint, "")

        matches = normalize(expected) == normalize(actual)

        results.append(
            {
                "checkpoint": checkpoint,
                "expected": expected,
                "actual": actual,
                "status": "PASS" if matches else "FAIL",
            }
        )

    return results


def compare_audit_results(source_rules, live_observations):
    """Evaluate audit rules using explicit PASS/FAIL observations."""
    normalized_observations = {
        normalize(field): value
        for field, value in live_observations.items()
    }

    results = []

    for checkpoint, expected in source_rules.items():
        actual = normalized_observations.get(normalize(checkpoint), "")
        normalized_actual = normalize(actual)

        if _starts_with_outcome(normalized_actual, "pass"):
            status = "PASS"
        elif _starts_with_outcome(normalized_actual, "fail"):
            status = "FAIL"
        else:
            status = (
                "PASS"
                if normalize(expected) == normalized_actual
                else "FAIL"
            )

        results.append(
            {
                "checkpoint": checkpoint,
                "expected": expected,
                "actual": actual,
                "status": status,
            }
        )

    return results


def _starts_with_outcome(value, outcome):
    """Return whether a normalized observation starts with an outcome."""
    if value == outcome:
        return True

    return any(
        value.startswith(f"{outcome}{separator}")
        for separator in (":", " -", " —", " |")
    )


def get_summary(results):
    """
    Summarize comparison results.

    The score is the percentage of checkpoints that passed. Empty results
    receive a NO DATA status because no comparison was performed.
    """
    total = len(results)
    passed = sum(
        result["status"] == "PASS"
        for result in results
    )
    failed = total - passed

    score = round(
        (passed / total) * 100,
        2,
    ) if total else 0.0

    if total == 0:
        overall_status = "NO DATA"
    elif failed == 0:
        overall_status = "PASS"
    else:
        overall_status = "FAIL"

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "score": score,
        "overall_status": overall_status,
    }
