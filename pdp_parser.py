"""Interpret text copied from a Dell product detail page."""

import re
from datetime import date, datetime

from comparison import normalize


_MONTH_DATE_PATTERN = re.compile(
    r"\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|"
    r"jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|"
    r"nov(?:ember)?|dec(?:ember)?)\s+\d{1,2}(?:,\s*\d{4})?\b",
    re.IGNORECASE,
)
_ISO_DATE_PATTERN = re.compile(r"\b\d{4}-\d{1,2}-\d{1,2}\b")
_SLASH_DATE_PATTERN = re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b")
_DISPLAY_PATTERN = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:\"|inch(?:es)?\b).*"
    r"(?:\d{3,4}\s*[x×]\s*\d{3,4}|fhd|qhd|uhd|wuxga)",
    re.IGNORECASE,
)


def analyze_pdp_content(source_rules, pdp_text, today=None):
    """Evaluate supported checkpoints against text copied from a PDP."""
    reference_date = today or date.today()
    lines = _clean_lines(pdp_text)
    normalized_text = normalize(pdp_text)
    delivery_date = _extract_delivery_date(lines, reference_date)

    results = []

    for checkpoint, expected in source_rules.items():
        status, evidence = _evaluate_checkpoint(
            checkpoint,
            expected,
            lines,
            normalized_text,
            delivery_date,
            reference_date,
        )
        results.append(
            {
                "checkpoint": checkpoint,
                "expected": expected,
                "actual": evidence,
                "status": status,
            }
        )

    return results


def get_audit_summary(results):
    """Summarize PASS, FAIL, and REVIEW audit outcomes."""
    total = len(results)
    passed = sum(result["status"] == "PASS" for result in results)
    failed = sum(result["status"] == "FAIL" for result in results)
    review = sum(result["status"] == "REVIEW" for result in results)
    evaluated = passed + failed
    score = round((passed / evaluated) * 100, 2) if evaluated else 0.0

    if total == 0:
        overall_status = "NO DATA"
    elif failed:
        overall_status = "FAIL"
    elif review:
        overall_status = "REVIEW"
    else:
        overall_status = "PASS"

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "review": review,
        "score": score,
        "overall_status": overall_status,
    }


def _clean_lines(text):
    return [line.strip() for line in str(text or "").splitlines() if line.strip()]


def _evaluate_checkpoint(
    checkpoint,
    expected,
    lines,
    normalized_text,
    delivery_date,
    reference_date,
):
    normalized_checkpoint = normalize(checkpoint)

    if normalized_checkpoint == "graphics":
        graphics_lines = _matching_lines(
            lines,
            ("graphics", "radeon", "geforce", "nvidia", "intel arc"),
        )
        return _presence_result(graphics_lines, "Graphics line item not found")

    if normalized_checkpoint == "display option count":
        display_lines = [line for line in lines if _DISPLAY_PATTERN.search(line)]
        if len(display_lines) == 1:
            return "PASS", display_lines[0]
        return (
            "FAIL",
            f"Found {len(display_lines)} display lines: "
            + (" | ".join(display_lines) if display_lines else "none"),
        )

    if normalized_checkpoint == "delivery date":
        if delivery_date is None:
            return "FAIL", "Delivery date not found"
        if delivery_date < reference_date:
            return "FAIL", f"Delivery date {delivery_date.isoformat()} is in the past"
        return "PASS", f"Delivery date: {delivery_date.isoformat()}"

    if normalized_checkpoint == "delivery date threshold":
        if delivery_date is None:
            return "FAIL", "Delivery date not found"
        days = (delivery_date - reference_date).days
        status = "PASS" if 0 <= days <= 30 else "FAIL"
        return status, f"Delivery is {days} day(s) from today"

    presence_patterns = {
        "processor": ("processor", "intel core", "amd ryzen", "snapdragon"),
        "operating system": ("windows", "ubuntu", "linux", "chrome os"),
        "memory": ("memory", " ddr", "gb ddr"),
        "storage": ("storage", " ssd", " hdd"),
        "display": ("display", "fhd", "qhd", "uhd", "wuxga"),
    }

    patterns = presence_patterns.get(normalized_checkpoint)
    if patterns:
        matches = _matching_lines(lines, patterns)
        if not matches:
            return "FAIL", f"{checkpoint} not found"
        if _is_generic_rule(expected):
            return "PASS", " | ".join(matches)

        compact_expected = _compact(expected)
        if any(compact_expected in _compact(match) for match in matches):
            return "PASS", " | ".join(matches)
        return (
            "FAIL",
            f"Expected {expected}; found " + " | ".join(matches),
        )

    return "REVIEW", "Automatic validation is not available for this checkpoint"


def _presence_result(matches, missing_message):
    if matches:
        return "PASS", " | ".join(matches)
    return "FAIL", missing_message


def _matching_lines(lines, patterns):
    return [
        line
        for line in lines
        if any(pattern in normalize(line) for pattern in patterns)
    ]


def _is_generic_rule(expected):
    normalized_expected = normalize(expected)
    return any(
        marker in normalized_expected
        for marker in (
            "should",
            "must",
            "line item",
            "present",
            "shown",
            "displayed",
            "available",
        )
    )


def _compact(value):
    return "".join(character for character in normalize(value) if character.isalnum())


def _extract_delivery_date(lines, reference_date):
    delivery_lines = [
        line
        for line in lines
        if any(
            marker in normalize(line)
            for marker in ("delivery", "delivers", "arrives", "get it by")
        )
    ]

    for line in delivery_lines:
        for pattern in (
            _ISO_DATE_PATTERN,
            _SLASH_DATE_PATTERN,
            _MONTH_DATE_PATTERN,
        ):
            match = pattern.search(line)
            if match:
                parsed = _parse_date(match.group(0), reference_date)
                if parsed:
                    return parsed

    return None


def _parse_date(value, reference_date):
    formats = (
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%B %d",
        "%b %d",
    )

    for date_format in formats:
        try:
            parsed = datetime.strptime(value, date_format).date()
        except ValueError:
            continue

        if "%Y" not in date_format:
            parsed = parsed.replace(year=reference_date.year)
            if parsed < reference_date:
                parsed = parsed.replace(year=reference_date.year + 1)

        return parsed

    return None
