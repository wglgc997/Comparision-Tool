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
    1: {
        "expected": "The product stack should be available and displayed.",
        "logic": (
            "If the product stack is displayed, pass. "
            "If it is missing, fail."
        ),
        "why_it_matters": (
            "Without the product stack, customers cannot compare products."
        ),
    },
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
    11: {
        "expected": (
            "Product images should load correctly and be visible in the "
            "product tile."
        ),
        "logic": (
            "If product images display correctly, pass. If an image is "
            "missing, broken, or does not load, fail."
        ),
        "why_it_matters": (
            "Images support visual validation and customer engagement. "
            "Missing images can reduce trust and conversion."
        ),
    },
    12: {
        "expected": (
            "The Copilot+ PC badge should appear exactly once for a "
            "qualifying configuration."
        ),
        "logic": (
            "If exactly one badge is shown, pass. "
            "If zero or multiple badges are shown, fail."
        ),
        "why_it_matters": (
            "Missing or duplicate badges reduce interface clarity and can "
            "misrepresent product eligibility."
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
    14: {
        "expected": (
            "The advertised starting price should match the price of an "
            "available configuration."
        ),
        "logic": (
            "If the starting price matches an available configuration, pass. "
            "If no matching configuration exists, fail."
        ),
        "why_it_matters": (
            "A price customers cannot reproduce creates confusion and "
            "damages trust."
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

    17: {
        "expected": (
            "The selected configuration should match the specifications "
            "shown in the Search product stack."
        ),
        "logic": (
            "If the Search specifications match the selected configuration, "
            "pass. If they do not match, fail."
        ),
        "why_it_matters": (
            "A mismatch between Search and Configuration can cause confusion "
            "and lead to an incorrect product selection."
        ),
    },
    18: {
        "expected": (
            "The processor selected in Configuration should match the "
            "processor shown in the Search product stack."
        ),
        "logic": (
            "If the Search processor matches the selected Configuration "
            "processor, pass. Otherwise, fail."
        ),
        "why_it_matters": (
            "Processor consistency maintains customer trust and prevents "
            "incorrect product selection."
        ),
    },
    19: {
        "expected": (
            "Processor, Operating System, Graphics, Memory, Storage, and "
            "Display shown in Search should exactly match the default "
            "configuration on the Customize & Buy page."
        ),
        "logic": (
            "If every Search specification matches the corresponding "
            "default configuration specification, pass. "
            "If any specification differs, fail."
        ),
        "why_it_matters": (
            "Matching specifications ensure data consistency throughout "
            "the Search-to-Configuration journey."
        ),
    },
    20: {
        "expected": (
            "Option classes should follow the platform-defined sequence, "
            "such as Processor, Operating System, Graphics, Memory, Storage, "
            "Display, and Add-ons."
        ),
        "logic": (
            "If the option-class order matches the platform standard, pass. "
            "Otherwise, fail."
        ),
        "why_it_matters": (
            "Standard ordering supports consistent dependency handling and "
            "valid product configurations."
        ),
    },
    21: {
        "expected": (
            "Processor options should follow the platform rule, with Intel "
            "listed first where applicable, followed by AMD or other options."
        ),
        "logic": (
            "If Intel appears first where required, pass. Otherwise, fail."
        ),
        "why_it_matters": (
            "Correct processor ordering supports platform rules and "
            "consistent configuration validation."
        ),
    },
    22: {
        "expected": (
            "Operating System options should appear after Processor options "
            "in the configuration sequence."
        ),
        "logic": (
            "If Operating System appears after Processor, pass. "
            "If it appears before Processor, fail."
        ),
        "why_it_matters": (
            "Correct sequencing supports dependency flow, prevents invalid "
            "configurations, and maintains platform consistency."
        ),
        "severity": "high",
    },
    23: {
        "expected": (
            "Graphics options should appear after Operating System options. "
            "The required order is Processor, Operating System, Graphics."
        ),
        "logic": (
            "If Graphics appears after Operating System, pass. "
            "Otherwise, fail."
        ),
        "why_it_matters": (
            "Correct ordering supports dependency logic and helps prevent "
            "invalid or incompatible configuration selections."
        ),
    },
    24: {
        "expected": (
            "The default configuration should select the lowest-priced "
            "valid option."
        ),
        "logic": (
            "If the default is the lowest-priced valid option, pass. "
            "If a higher-priced option is selected while a cheaper valid "
            "option exists, fail."
        ),
        "why_it_matters": (
            "An incorrect default can mislead customers about pricing, "
            "reduce trust, and violate pricing rules."
        ),
    },
    25: {
        "expected": (
            "The default Operating System should follow the product segment: "
            "Dell, Dell Plus, and XPS use Windows Home; Dell Pro and "
            "Dell Pro Precision use Windows Pro."
        ),
        "logic": (
            "If the default Operating System matches the product-line rule, "
            "pass. Otherwise, fail."
        ),
        "why_it_matters": (
            "The correct default supports licensing, pricing, compliance, "
            "and a consistent customer experience."
        ),
        "status": "needs_clarification",
        "notes": (
            "The PDF also lists XPS and Dell Plus defaulting to Windows Pro "
            "as an exception, which conflicts with the stated expectation."
        ),
    },
    26: {
        "expected": (
            "Available language options should update based on the selected "
            "Operating System."
        ),
        "logic": (
            "If the language options update after the Operating System "
            "selection, pass. Otherwise, fail."
        ),
        "why_it_matters": (
            "Correct language dependencies prevent invalid configurations "
            "and ensure the proper Operating System and language pairing."
        ),
    },
    27: {
        "expected": (
            "Only software compatible with the selected Windows edition "
            "should be displayed."
        ),
        "logic": (
            "If only compatible software is shown, pass. "
            "If incompatible software is shown, fail."
        ),
        "why_it_matters": (
            "Compatibility filtering prevents invalid configurations, "
            "setup problems, and licensing errors."
        ),
    },
    28: {
        "expected": (
            "The camera should map automatically to the selected display "
            "and should not be independently selectable."
        ),
        "logic": (
            "If the camera is tied to the display, pass. "
            "If the camera can be selected independently, fail or review."
        ),
        "why_it_matters": (
            "The dependency ensures correct hardware pairing and prevents "
            "invalid configurations."
        ),
    },
    29: {
        "expected": (
            "Only valid display options should be shown, with no prohibited "
            "lower-tier display options available."
        ),
        "logic": (
            "If a prohibited display downsell appears, fail. "
            "If only allowed display options appear, pass."
        ),
        "why_it_matters": (
            "The restriction preserves product positioning and prevents "
            "unsupported display configurations."
        ),
    },
    30: {
        "expected": (
            "Display resolution should use the approved production format, "
            "such as '2560 x 1600, 400 nits'."
        ),
        "logic": (
            "If the resolution format matches the approved standard, pass. "
            "Otherwise, fail."
        ),
        "why_it_matters": (
            "Consistent formatting improves readability, accuracy, and "
            "customer trust."
        ),
    },
    31: {
        "expected": (
            "Resolution values should be consistent across comparable "
            "products."
        ),
        "logic": (
            "If the resolution is consistent across applicable products, "
            "pass. Otherwise, fail."
        ),
        "why_it_matters": (
            "Consistent values support accurate product comparisons and "
            "prevent customer confusion."
        ),
    },
    32: {
        "expected": (
            "The display label should correspond to its resolution, such as "
            "FHD corresponding to 1920 x 1080."
        ),
        "logic": (
            "If the display label matches the resolution, pass. "
            "Otherwise, fail."
        ),
        "why_it_matters": (
            "Matching labels and resolutions prevents misleading product "
            "information and supports accurate comparisons."
        ),
    },

    33: {
        "expected": (
            "The page should display only labels relevant to the selected "
            "country or region."
        ),
        "logic": (
            "If all displayed labels match the selected country or region, "
            "pass. If a label from another region appears, fail."
        ),
        "why_it_matters": (
            "Incorrect localization can confuse customers, reduce trust, "
            "and create compliance or legal concerns."
        ),
    },
    34: {
        "expected": (
            "Keyboard options should match the approved layouts for the "
            "selected country or region."
        ),
        "logic": (
            "If all keyboard options are approved for the selected region, "
            "pass. If a non-approved keyboard appears, flag or fail."
        ),
        "why_it_matters": (
            "Region-appropriate keyboard options prevent incorrect orders, "
            "returns, and customer dissatisfaction."
        ),
    },
    35: {
        "expected": (
            "Only power cords approved for the selected region should be "
            "displayed and selectable."
        ),
        "logic": (
            "If only region-approved power cords are shown, pass. "
            "If a non-approved regional cord appears, fail."
        ),
        "why_it_matters": (
            "Correct regional power cords prevent hardware compatibility "
            "problems and support electrical safety and compliance."
        ),
    },
    43: {
        "expected": (
            "A Base Warranty option should be displayed in the services "
            "section."
        ),
        "logic": (
            "If Base Warranty is present, pass. "
            "If Base Warranty is missing, fail."
        ),
        "why_it_matters": (
            "Warranty information helps customers understand product "
            "coverage and available support."
        ),
    },
    44: {
        "expected": (
            "Hardware support or service-upgrade options should be available "
            "in the services section."
        ),
        "logic": (
            "If hardware support upgrade options are present, pass. "
            "If they are missing, fail."
        ),
        "why_it_matters": (
            "Support upgrades let customers select the coverage and service "
            "level that fits their needs."
        ),
    },
    45: {
        "expected": (
            "Warranty downsell options, including reduced-value options with "
            "negative pricing, should not be displayed."
        ),
        "logic": (
            "If no warranty downsell is present, pass. "
            "If a warranty downsell is present, fail."
        ),
        "why_it_matters": (
            "Warranty downsells can confuse customers, reduce perceived "
            "value, and create an inconsistent pricing experience."
        ),
    },
    46: {
        "expected": (
            "Warranty pricing should remain valid and realistic when the "
            "customer changes the duration or service option."
        ),
        "logic": (
            "If warranty pricing is valid, pass. "
            "If dummy or invalid pricing appears, fail."
        ),
        "why_it_matters": (
            "Invalid warranty pricing reduces customer trust and can indicate "
            "a configuration or pricing defect."
        ),
    },
    47: {
        "expected": (
            "Pricing should be available for every selectable warranty "
            "duration and option."
        ),
        "logic": (
            "If pricing is available, pass. "
            "If pricing is missing or unavailable, fail."
        ),
        "why_it_matters": (
            "Missing pricing prevents informed purchase decisions and may "
            "indicate a backend or configuration problem."
        ),
    },
    48: {
        "expected": (
            "Accidental Damage should not be independently selectable when "
            "it is already included with ProSupport Plus."
        ),
        "logic": (
            "If the invalid combination is blocked, pass. "
            "If the invalid combination is allowed, fail."
        ),
        "why_it_matters": (
            "Blocking duplicate services prevents incorrect pricing and "
            "ensures a valid service configuration."
        ),
    },
    49: {
        "expected": (
            "Incompatible service options should be hidden or disabled."
        ),
        "logic": (
            "If incompatible options are hidden or disabled, pass. "
            "If they remain visible or selectable, fail or review."
        ),
        "why_it_matters": (
            "Preventing invalid selections reduces configuration errors and "
            "guides customers toward valid service combinations."
        ),
    },

    50: {
        "expected": (
            "The McAfee product should map to the selected Operating System: "
            "Windows Home uses McAfee Premium, while Windows Pro uses "
            "McAfee Business."
        ),
        "logic": (
            "If the McAfee product matches the selected Operating System, "
            "pass. Otherwise, fail."
        ),
        "why_it_matters": (
            "Correct dependency mapping prevents licensing and configuration "
            "errors and ensures customers receive the appropriate security "
            "product."
        ),
    },
    52: {
        "expected": (
            "The Autopilot option should appear only when a valid Windows Pro "
            "upsell is available. Otherwise, it should not be shown."
        ),
        "logic": (
            "If Autopilot is hidden when no Windows Pro upsell is available, "
            "pass. If Autopilot remains visible without a Windows Pro upsell, "
            "fail."
        ),
        "why_it_matters": (
            "Correct visibility prevents invalid configurations and customer "
            "confusion by offering Autopilot only when it is supported."
        ),
        "notes": (
            "Dell XPS and Alienware products are excluded from this "
            "checkpoint."
        ),
    },
    53: {
        "expected": (
            "When Autopilot is selected, the customer should be able to "
            "enter or update the tenant ID and domain."
        ),
        "logic": (
            "If Autopilot is selected and the tenant ID or domain input is "
            "missing, fail. Otherwise, pass."
        ),
        "why_it_matters": (
            "The tenant ID and domain are required for correct Autopilot "
            "provisioning, deployment, and registration."
        ),
    },
    54: {
        "expected": (
            "Enterprise or commercial software should appear only with a "
            "compatible Operating System, such as Windows Pro or higher, "
            "and should not appear with Windows Home."
        ),
        "logic": (
            "If software compatible with the selected Operating System is "
            "shown, pass. If enterprise software appears with Windows Home, "
            "fail."
        ),
        "why_it_matters": (
            "Operating System compatibility prevents invalid configurations, "
            "supports correct licensing, and ensures customers see only "
            "relevant software options."
        ),
    },
    55: {
        "expected": (
            "The Bundle & Save section should display a clear coupon message "
            "that communicates additional savings."
        ),
        "logic": (
            "If the coupon message is present and displayed clearly, pass. "
            "If it is missing or unclear, fail."
        ),
        "why_it_matters": (
            "A clear savings message improves conversion and ensures "
            "customers understand the available discount."
        ),
    },
    56: {
        "expected": (
            "Bundle items should display accurate and consistent pricing, "
            "with discounts or savings shown clearly."
        ),
        "logic": (
            "If bundle pricing is accurate and clearly displayed, pass. "
            "If pricing is missing, incorrect, or inconsistent, fail."
        ),
        "why_it_matters": (
            "Accurate bundle pricing provides transparency and helps "
            "customers understand the value of the offer."
        ),
    },
    57: {
        "expected": (
            "The flyout should display the same product image as the "
            "associated product listing."
        ),
        "logic": (
            "If the flyout image matches the product image, pass. "
            "Otherwise, fail."
        ),
        "why_it_matters": (
            "Consistent images prevent customer confusion and reduce the "
            "risk of selecting the wrong product."
        ),
    },
    58: {
        "expected": (
            "All expected key technical specifications should appear in "
            "the Bundle & Save flyout panel."
        ),
        "logic": (
            "If all expected specifications are present in the flyout, pass. "
            "If any expected specification is missing, fail."
        ),
        "why_it_matters": (
            "Visible specifications help customers make informed purchase "
            "decisions without leaving the product listing page."
        ),
        "severity": "medium",
    },
    59: {
        "expected": None,
        "logic": None,
        "why_it_matters": None,
        "status": "needs_clarification",
        "notes": (
            "The PDF states that the expected offer-identifier behavior "
            "must be confirmed with Chaitali."
        ),
    },
    60: {
        "expected": (
            "The product display size should be clearly shown in the "
            "product specifications or title on the product listing page."
        ),
        "logic": (
            "If the display size is visible and correct, pass. "
            "If it is missing or incorrect, fail."
        ),
        "why_it_matters": (
            "Display size is a key buying factor, and incorrect or missing "
            "information can mislead customers."
        ),


    },
    61: {
        "expected": (
            "Ratings and reviews may appear for older products, but should "
            "not appear for newer badge products."
        ),
        "logic": (
            "If ratings behavior matches the product age and badge status, "
            "pass. If ratings appear for a new badge product, fail."
        ),
        "why_it_matters": (
            "Correct ratings behavior provides accurate social proof, "
            "supports informed decisions, and maintains customer trust."
        ),
        "severity": "medium",
    },
    62: {
        "expected": (
            "The starting price on the product listing page should match "
            "the base configuration price on the Configuration page."
        ),
        "logic": (
            "If the listing price matches the base configuration price, "
            "pass. Otherwise, fail."
        ),
        "why_it_matters": (
            "Consistent entry-level pricing prevents confusion and builds "
            "customer trust during navigation."
        ),
        "severity": "critical",
        "notes": (
            "Rule 63 separately verifies that the displayed starting price "
            "is the lowest available valid configuration price."
        ),
    },
    63: {
        "expected": (
            "The product listing page should display the lowest available "
            "starting price from all valid product configurations."
        ),
        "logic": (
            "If the listing price equals the lowest valid configuration "
            "price, pass. If it is higher, fail."
        ),
        "why_it_matters": (
            "Accurate starting prices prevent misleading price comparisons "
            "and protect customer trust."
        ),
    },

    64: {
        "expected": (
            "The price shown on the product listing or Search tile should "
            "match the starting or selected price on the Configuration page."
        ),
        "logic": (
            "If the price remains consistent between the listing and "
            "Configuration page, pass. Otherwise, fail."
        ),
        "why_it_matters": (
            "Price consistency provides transparency and prevents confusion "
            "or abandonment caused by unexpected price changes."
        ),
        "severity": "critical",
    },
    65: {
        "expected": (
            "The specification order in the fixed-offer detail view should "
            "match the order shown in Search."
        ),
        "logic": (
            "If the specification sequence is identical in Search and the "
            "detail view, pass. Otherwise, fail."
        ),
        "why_it_matters": (
            "Consistent ordering improves readability and helps customers "
            "compare product information."
        ),
    },
    66: {
        "expected": (
            "All specification values shown in Search and the fixed-offer "
            "detail view should match exactly."
        ),
        "logic": (
            "If all specification values match between Search and the detail "
            "view, pass. If any value differs, fail."
        ),
        "why_it_matters": (
            "Consistent product data builds customer trust and prevents "
            "incorrect purchase decisions."
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

    default_status = (
        "documented"
        if has_complete_details
        else "needs_rule_details"
    )

    return {
        "id": rule_id,
        "category": category,
        "checkpoint": checkpoint,
        "expected": expected,
        "logic": logic,
        "why_it_matters": why_it_matters,
        "severity": details.get("severity"),
        "status": details.get("status", default_status),
        "notes": details.get("notes"),
    }


CHECKPOINT_RULES = [
    _build_rule(rule_id, category, checkpoint)
    for rule_id, category, checkpoint in _RULE_INDEX
]

