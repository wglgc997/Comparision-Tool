import unittest

from comparison import (
    compare_audit_results,
    compare_specs,
    get_summary,
    normalize,
    parse_specs,
)


class NormalizeTests(unittest.TestCase):
    def test_normalizes_case_and_whitespace(self):
        value = "  Intel   Core ULTRA 7  "

        self.assertEqual(
            normalize(value),
            "intel core ultra 7",
        )

    def test_normalizes_missing_values(self):
        self.assertEqual(normalize(None), "")
        self.assertEqual(normalize(float("nan")), "")

    def test_normalizes_non_string_value(self):
        self.assertEqual(normalize(16), "16")


class CompareSpecsTests(unittest.TestCase):
    def test_compares_offer_specs(self):
        source_specs = {
            "Processor": "Intel Core Ultra 7",
            "Memory": "16GB DDR5",
            "Graphics": "Intel Integrated Graphics",
        }
        live_specs = {
            " processor ": "intel  core ultra 7",
            "Memory": "32GB DDR5",
        }

        results = compare_specs(source_specs, live_specs)

        self.assertEqual(
            [result["status"] for result in results],
            ["PASS", "FAIL", "FAIL"],
        )
        self.assertEqual(results[2]["actual"], "")

    def test_preserves_original_values(self):
        source_specs = {
            "Display": "14-inch FHD",
        }
        live_specs = {
            "display": "  14-INCH FHD  ",
        }

        result = compare_specs(source_specs, live_specs)[0]

        self.assertEqual(result["expected"], "14-inch FHD")
        self.assertEqual(result["actual"], "  14-INCH FHD  ")
        self.assertEqual(result["status"], "PASS")

    def test_empty_source_returns_no_results(self):
        self.assertEqual(compare_specs({}, {}), [])


class CompareAuditResultsTests(unittest.TestCase):
    def test_uses_explicit_outcomes_with_evidence(self):
        source_rules = {
            "Graphics": "Graphics line item present",
            "Display option count": "Only one display size should be shown",
        }
        observations = {
            "Graphics": "FAIL - Missing from specs",
            "Display option count": "PASS - One display line shown",
        }

        results = compare_audit_results(source_rules, observations)

        self.assertEqual(
            [result["status"] for result in results],
            ["FAIL", "PASS"],
        )
        self.assertEqual(
            results[0]["actual"],
            "FAIL - Missing from specs",
        )

    def test_missing_observation_fails(self):
        results = compare_audit_results(
            {"Delivery date": "Delivery date should not be in the past"},
            {},
        )

        self.assertEqual(results[0]["status"], "FAIL")

    def test_exact_match_remains_supported(self):
        results = compare_audit_results(
            {"Graphics": "Graphics line item present"},
            {"Graphics": "graphics line item present"},
        )

        self.assertEqual(results[0]["status"], "PASS")


class ParseSpecsTests(unittest.TestCase):
    def test_parses_checkpoint_value_lines(self):
        text = (
            "Processor: Intel Core Ultra 7\n"
            "Memory: 16GB DDR5\n"
            "Storage: 512GB SSD"
        )

        self.assertEqual(
            parse_specs(text),
            {
                "Processor": "Intel Core Ultra 7",
                "Memory": "16GB DDR5",
                "Storage": "512GB SSD",
            },
        )

    def test_preserves_colons_inside_values(self):
        self.assertEqual(
            parse_specs("Delivery: Estimated date: October 15"),
            {
                "Delivery": "Estimated date: October 15",
            },
        )

    def test_ignores_blank_and_malformed_lines(self):
        text = (
            "\n"
            "Invalid line\n"
            ": Missing checkpoint\n"
            "Display: 14-inch FHD\n"
        )

        self.assertEqual(
            parse_specs(text),
            {
                "Display": "14-inch FHD",
            },
        )

    def test_empty_input_returns_empty_dictionary(self):
        self.assertEqual(parse_specs(""), {})
        self.assertEqual(parse_specs(None), {})

class SummaryTests(unittest.TestCase):
    def test_summarizes_mixed_results(self):
        results = [
            {"status": "PASS"},
            {"status": "FAIL"},
            {"status": "PASS"},
        ]

        self.assertEqual(
            get_summary(results),
            {
                "total": 3,
                "passed": 2,
                "failed": 1,
                "score": 66.67,
                "overall_status": "FAIL",
            },
        )

    def test_summarizes_all_passed_results(self):
        summary = get_summary(
            [
                {"status": "PASS"},
                {"status": "PASS"},
            ]
        )

        self.assertEqual(summary["score"], 100.0)
        self.assertEqual(summary["overall_status"], "PASS")

    def test_summarizes_empty_results(self):
        self.assertEqual(
            get_summary([]),
            {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "score": 0.0,
                "overall_status": "NO DATA",
            },
        )


if __name__ == "__main__":
    unittest.main()
