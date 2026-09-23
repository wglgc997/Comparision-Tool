"""
Checkpoint Rules Engine.

Contains the validation-rule inventory used by the Offer Readiness QA Tool.
The source PDF contains rules 1-66, with rule 51 absent.
"""

_RULE_INDEX = [
    (1, "Site Search / Product Stack", "Product stack displayed"),
    (2, "Site Search / Product Stack", "Product stack text"),
    (3, "Site Search / Product Stack", "Spec sequence"),
    (4, "Site Search / Product Stack", "Processor"),
    (5, "Site Search / Product Stack", "Operating System"),
    (6, "Site Search / Product Stack", "Graphics"),
    (7, "Site Search / Product Stack", "Memory"),
    (8, "Site Search / Product Stack", "Storage"),
    (9, "Site Search / Product Stack", "Display"),
    (10, "Site Search / Product Stack", "Display option count"),
    (11, "Product Stack Visual / Content", "Product images"),
    (12, "Product Stack Visual / Content", "Copilot+ PC badge"),
    (13, "Product Stack Visual / Content", "Product title"),
    (14, "Product Stack Visual / Content", "Price"),
    (15, "Product Stack Visual / Content", "Delivery date"),
    (16, "Product Stack Visual / Content", "Delivery date threshold"),
    (
        17,
        "Search to Customize & Buy Cross-check",
        "Specs carry over correctly",
    ),
    (
        18,
        "Search to Customize & Buy Cross-check",
        "Processor cross-check",
    ),
    (
        19,
        "Search to Customize & Buy Cross-check",
        "Full spec cross-check",
    ),
    (20, "Configuration / Option", "Option-class sequence"),
    (21, "Configuration / Option", "Processor/CPU sequence"),
    (22, "Configuration / Option", "OS sequence"),
    (23, "Configuration / Option", "Graphics sequence"),
    (24, "Configuration / Option", "Downsell/default logic"),
    (25, "Configuration / Option", "OS default"),
    (26, "Operating System / Language", "OS-dependent language"),
    (27, "Operating System / Language", "Windows Home vs Pro"),
    (28, "Display", "Display/camera dependency"),
    (29, "Display", "No display downsell"),
    (30, "Display", "Resolution format"),
    (31, "Display", "Resolution consistency"),
    (32, "Display", "Display label vs resolution"),
    (33, "Localization", "Country labels"),
    (34, "Localization", "Keyboard localization"),
    (35, "Localization", "Power cord localization"),
    (36, "Localization", "Packaging regional label"),
    (37, "Localization", "Regulatory label"),
    (38, "Power Supply / Packaging", "Power supply dependency"),
    (39, "Power Supply / Packaging", "Dummy price"),
    (40, "Power Supply / Packaging", "Packaging type"),
    (41, "Power Supply / Packaging", "Packaging label"),
    (42, "Power Supply / Packaging", "Adapter/battery dependency"),
    (43, "Warranty / Services", "Base warranty"),
    (44, "Warranty / Services", "Hardware support upgrade"),
    (45, "Warranty / Services", "No warranty downsell"),
    (
        46,
        "Warranty / Services",
        "Dummy pricing - warranty duration/options",
    ),
    (47, "Warranty / Services", "Pricing availability"),
    (
        48,
        "Services Compatibility",
        "ProSupport Plus + Accidental Damage",
    ),
    (49, "Services Compatibility", "Option hiding"),
    (50, "Software", "McAfee dependency"),
    (52, "Software", "Autopilot visibility"),
    (53, "Software", "Autopilot tag ID"),
    (54, "Software", "Enterprise software compatibility"),
    (55, "Bundle & Save / Candy Aisle", "Coupon blurb"),
    (56, "Bundle & Save / Candy Aisle", "Pricing"),
    (57, "Bundle & Save / Candy Aisle", "Flyout image"),
    (58, "Bundle & Save / Candy Aisle", "Key tech specs"),
    (59, "Bundle & Save / Candy Aisle", "Offer identifier"),
    (60, "PLP", "Display size"),
    (61, "PLP", "Ratings/reviews"),
    (62, "PLP", "Starting price"),
    (63, "PLP", "Lowest-price rule"),
    (64, "PLP to Config", "Price carry-over"),
    (
        65,
        "Fixed Offer",
        "Same spec sequence as Search",
    ),
    (
        66,
        "Fixed Offer",
        "Spec value consistency",
    ),
]

_RULE_DETAILS = {
    2: {
        "expected": "Product stack text should follow the standard format.",
        "logic": (
            "If the product stack text uses the correct format, pass. "
            "Otherwise, fail."
        ),
        "why_it_matters": (
            "Correct formatting improves readability and consistency."
        ),
    },
    3: {
        "expected": (
            "Specifications should begin with Processor, followed by "
            "Operating System. MDF-compliant specifications and the "
            "remaining specifications may follow."
        ),
        "logic": (
            "If the specification sequence matches the standard, pass. "
            "Otherwise, fail."
        ),
        "why_it_matters": (
            "A consistent sequence makes products easier to read and compare."
        ),
    },
    4: {
        "expected": (
            "Processor information should be present as the first line item "
            "in the product stack."
        ),
        "logic": (
            "If Processor is present, pass. "
            "If Processor is missing, fail."
        ),
        "why_it_matters": (
            "Processor is a key specification users rely on to evaluate "
            "performance and compare products."
        ),
    },
    5: {
        "expected": (
            "Operating System should be present as a key line item "
            "in the product stack."
        ),
        "logic": (
            "If Operating System is present, pass. "
            "If Operating System is missing, fail."
        ),
        "why_it_matters": (
            "Operating System affects compatibility, usability, and "
            "the purchase decision."
        ),
    },
    6: {
        "expected": (
            "Graphics information should be present as a key line item "
            "in the product stack."
        ),
        "logic": (
            "If Graphics is present, pass. "
            "If Graphics is missing or replaced, fail."
        ),
        "why_it_matters": (
            "Graphics information helps customers evaluate performance "
            "for gaming, design, and video workloads."
        ),
    },
    8: {
        "expected": (
            "Storage information, such as SSD or HDD capacity, should be "
            "present as a key line item in the product stack."
        ),
        "logic": (
            "If Storage is present, pass. "
            "If Storage is missing or replaced, fail."
        ),
        "why_it_matters": (
            "Storage capacity affects how much data users can store and "
            "influences their purchase decision."
        ),
    },
    9: {
        "expected": (
            "Display information, including size, resolution, and type, "
            "should be present as a key line item in the product stack."
        ),
        "logic": (
            "If Display is present, pass. "
            "If Display is missing or replaced, fail."
        ),
        "why_it_matters": (
            "Display size, resolution, and clarity are key buying factors."
        ),
    },
    10: {
        "expected": (
            "Only one display option should appear in the product stack."
        ),
        "logic": (
            "If exactly one display option is shown, pass. "
            "If multiple display options are shown, fail."
        ),
        "why_it_matters": (
            "Multiple display values can confuse customers and misrepresent "
            "the displayed configuration."
        ),
    },
    13: {
        "expected": (
            "The product title should match the approved naming standard "
            "and the product-detail page source of truth."
        ),
        "logic": (
            "If the product title matches the source of truth, pass. "
            "If it is missing, inconsistent, or incorrect, fail."
        ),
        "why_it_matters": (
            "The product title supports correct product identification and "
            "comparison. An incorrect title can mislead customers."
        ),
    },
    15: {
        "expected": (
            "The delivery date should be today or a future date."
        ),
        "logic": (
            "If the delivery date is today or later, pass. "
            "If the delivery date is in the past, fail."
        ),
        "why_it_matters": (
            "Incorrect delivery dates can mislead customers and affect "
            "purchase decisions."
        ),
    },
    16: {
        "expected": (
            "The delivery date should be no more than 30 days from "
            "the current date."
        ),
        "logic": (
            "If the delivery date is within 30 days, pass. "
            "If it is more than 30 days away, fail."
        ),
        "why_it_matters": (
            "Unrealistic delivery timelines create a poor customer "
            "experience and may cause customers to abandon a purchase."
        ),
    },
}

def _build_rule(rule_id, category, checkpoint):
    """Build one rule dictionary from its inventory and available details."""
    details = _RULE_DETAILS.get(rule_id, {})

    expected = details.get("expected")
    logic = details.get("logic")
    why_it_matters = details.get("why_it_matters")

    has_complete_details = all(
        value is not None
        for value in (expected, logic, why_it_matters)
    )

    return {
        "id": rule_id,
        "category": category,
        "checkpoint": checkpoint,
        "expected": expected,
        "logic": logic,
        "why_it_matters": why_it_matters,
        "severity": None,
        "status": (
            "documented"
            if has_complete_details
            else "needs_rule_details"
        ),
    }


CHECKPOINT_RULES = [
    _build_rule(rule_id, category, checkpoint)
    for rule_id, category, checkpoint in _RULE_INDEX
]

