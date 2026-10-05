import unittest
from datetime import date

from pdp_parser import analyze_pdp_content, get_audit_summary


class AnalyzePdpContentTests(unittest.TestCase):
    def setUp(self):
        self.rules = {
            "Graphics": "Graphics line item present",
            "Display option count": "Only one display size should be shown",
            "Delivery date": "Delivery date should not be in the past",
            "Delivery date threshold": "Working threshold = within 30 days",
        }

    def test_finds_failures_in_copied_product_tile(self):
        content = """
        Dell Pro 7 Series 14 Laptop
        AMD Ryzen AI 5 PRO 435, 6 Cores
        Windows 11 Pro
        16 GB DDR5
        512 GB SSD
        14" Non Touch FHD (1920x1200)
        0" Non Touch WUXGA (1920x1200)
        """

        results = analyze_pdp_content(
            self.rules,
            content,
            today=date(2026, 10, 5),
        )

        self.assertEqual(
            [result["status"] for result in results],
            ["FAIL", "FAIL", "FAIL", "FAIL"],
        )
        self.assertIn("Found 2 display lines", results[1]["actual"])

    def test_passes_supported_rules_when_content_is_valid(self):
        content = """
        Graphics: AMD Radeon 780M
        14" Non Touch FHD (1920x1200)
        Estimated delivery: October 20, 2026
        """

        results = analyze_pdp_content(
            self.rules,
            content,
            today=date(2026, 10, 5),
        )

        self.assertEqual(
            [result["status"] for result in results],
            ["PASS", "PASS", "PASS", "PASS"],
        )

    def test_marks_unsupported_checkpoint_for_review(self):
        results = analyze_pdp_content(
            {"Product images": "Images should be correct"},
            "Dell Pro laptop",
            today=date(2026, 10, 5),
        )

        self.assertEqual(results[0]["status"], "REVIEW")


class AuditSummaryTests(unittest.TestCase):
    def test_summarizes_pass_fail_and_review(self):
        summary = get_audit_summary(
            [
                {"status": "PASS"},
                {"status": "FAIL"},
                {"status": "REVIEW"},
            ]
        )

        self.assertEqual(
            summary,
            {
                "total": 3,
                "passed": 1,
                "failed": 1,
                "review": 1,
                "score": 50.0,
                "overall_status": "FAIL",
            },
        )


if __name__ == "__main__":
    unittest.main()
