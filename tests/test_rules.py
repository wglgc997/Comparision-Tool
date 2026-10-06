import unittest

from rules import (
    get_all_rules,
    get_by_category,
    get_by_severity,
)


class GetAllRulesTests(unittest.TestCase):
    def test_returns_complete_rule_inventory(self):
        rules = get_all_rules()
        rule_ids = [rule["id"] for rule in rules]

        self.assertEqual(len(rules), 65)
        self.assertEqual(rule_ids, list(range(1, 51)) + list(range(52, 67)))

    def test_every_rule_has_required_fields(self):
        required_fields = {
            "id",
            "category",
            "checkpoint",
            "expected",
            "logic",
            "why_it_matters",
            "severity",
            "status",
            "notes",
        }

        for rule in get_all_rules():
            with self.subTest(rule_id=rule["id"]):
                self.assertEqual(set(rule), required_fields)

    def test_rule_ids_are_unique(self):
        rule_ids = [rule["id"] for rule in get_all_rules()]

        self.assertEqual(len(rule_ids), len(set(rule_ids)))

    def test_returns_a_new_list(self):
        first_result = get_all_rules()
        second_result = get_all_rules()

        self.assertIsNot(first_result, second_result)


class CategoryFilterTests(unittest.TestCase):
    def test_filters_rules_by_category(self):
        rules = get_by_category("Site Search / Product Stack")

        self.assertEqual(
            [rule["id"] for rule in rules],
            list(range(1, 11)),
        )

    def test_category_filter_ignores_case(self):
        rules = get_by_category("site search / product stack")

        self.assertEqual(
            [rule["id"] for rule in rules],
            list(range(1, 11)),
        )

    def test_category_filter_ignores_outer_spaces(self):
        rules = get_by_category(
            "  Site Search / Product Stack  "
        )

        self.assertEqual(
            [rule["id"] for rule in rules],
            list(range(1, 11)),
        )

    def test_unknown_category_returns_empty_list(self):
        self.assertEqual(
            get_by_category("Unknown category"),
            [],
        )


class SeverityFilterTests(unittest.TestCase):
    def test_filters_rules_by_severity(self):
        rules = get_by_severity("critical")

        self.assertTrue(rules)
        self.assertTrue(
            all(rule["severity"] == "critical" for rule in rules)
        )

    def test_severity_filter_ignores_case(self):
        lowercase_result = get_by_severity("critical")
        uppercase_result = get_by_severity("CRITICAL")

        self.assertEqual(uppercase_result, lowercase_result)

    def test_severity_filter_ignores_outer_spaces(self):
        regular_result = get_by_severity("critical")
        spaced_result = get_by_severity("  critical  ")

        self.assertEqual(spaced_result, regular_result)

    def test_unknown_severity_returns_empty_list(self):
        self.assertEqual(
            get_by_severity("unknown"),
            [],
        )


class RuleStatusTests(unittest.TestCase):
    def test_documented_rules_have_complete_logic(self):
        documented_rules = [
            rule
            for rule in get_all_rules()
            if rule["status"] == "documented"
        ]

        self.assertTrue(documented_rules)

        for rule in documented_rules:
            with self.subTest(rule_id=rule["id"]):
                self.assertIsNotNone(rule["expected"])
                self.assertIsNotNone(rule["logic"])
                self.assertIsNotNone(rule["why_it_matters"])

    def test_undefined_rules_are_not_marked_as_documented(self):
        undefined_rule_ids = {25, 37, 38, 39, 40, 41, 42, 59}

        rules_by_id = {
            rule["id"]: rule
            for rule in get_all_rules()
        }

        for rule_id in undefined_rule_ids:
            with self.subTest(rule_id=rule_id):
                self.assertNotEqual(
                    rules_by_id[rule_id]["status"],
                    "documented",
                )


if __name__ == "__main__":
    unittest.main()