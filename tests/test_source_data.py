import unittest

import pandas as pd

from source_data import (
    detect_columns,
    extract_source_specs,
    filter_offer_rows,
    get_offer_ids,
)


class DetectColumnsTests(unittest.TestCase):
    def test_detects_required_columns(self):
        dataframe = pd.DataFrame(
            columns=[
                "Country",
                "Offer ID",
                "Checkpoint",
                "Expected Format / Rule",
            ]
        )

        self.assertEqual(
            detect_columns(dataframe),
            {
                "offer_id": "Offer ID",
                "country": "Country",
                "checkpoint": "Checkpoint",
                "expected": "Expected Format / Rule",
            },
        )

    def test_detects_columns_ignoring_case_and_spaces(self):
        dataframe = pd.DataFrame(
            columns=[
                "COUNTRY",
                "offer_id",
                "check point",
                "expected-format-rule",
            ]
        )

        self.assertEqual(
            detect_columns(dataframe),
            {
                "offer_id": "offer_id",
                "country": "COUNTRY",
                "checkpoint": "check point",
                "expected": "expected-format-rule",
            },
        )

    def test_returns_none_for_missing_columns(self):
        dataframe = pd.DataFrame(columns=["Offer ID"])

        columns = detect_columns(dataframe)

        self.assertEqual(columns["offer_id"], "Offer ID")
        self.assertIsNone(columns["country"])
        self.assertIsNone(columns["checkpoint"])
        self.assertIsNone(columns["expected"])


class GetOfferIdsTests(unittest.TestCase):
    def test_returns_sorted_unique_offer_ids(self):
        dataframe = pd.DataFrame(
            {
                "Offer ID": [
                    "offer_2",
                    " offer_1 ",
                    "offer_2",
                    None,
                    "",
                ]
            }
        )

        self.assertEqual(
            get_offer_ids(dataframe, "Offer ID"),
            ["offer_1", "offer_2"],
        )


class FilterOfferRowsTests(unittest.TestCase):
    def setUp(self):
        self.dataframe = pd.DataFrame(
            {
                "Offer ID": [
                    "offer_1",
                    "offer_1",
                    "offer_2",
                ],
                "Country": [
                    "hkg_market_EN",
                    "hkg_market_ZH",
                    "hkg_market_EN",
                ],
                "Checkpoint": [
                    "Processor",
                    "Memory",
                    "Storage",
                ],
            }
        )

    def test_filters_by_offer_id(self):
        result = filter_offer_rows(
            self.dataframe,
            "Offer ID",
            "offer_1",
        )

        self.assertEqual(len(result), 2)
        self.assertTrue(
            (result["Offer ID"] == "offer_1").all()
        )

    def test_filters_by_offer_id_and_country(self):
        result = filter_offer_rows(
            self.dataframe,
            "Offer ID",
            "offer_1",
            "Country",
            "hkg_market_ZH",
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result.iloc[0]["Checkpoint"],
            "Memory",
        )

    def test_unknown_offer_returns_empty_dataframe(self):
        result = filter_offer_rows(
            self.dataframe,
            "Offer ID",
            "unknown",
        )

        self.assertTrue(result.empty)


class ExtractSourceSpecsTests(unittest.TestCase):
    def test_extracts_complete_specs(self):
        dataframe = pd.DataFrame(
            {
                "Checkpoint": [
                    "Processor",
                    "Memory",
                ],
                "Expected Format / Rule": [
                    "Intel Core Ultra 7",
                    "16GB DDR5",
                ],
            }
        )

        self.assertEqual(
            extract_source_specs(
                dataframe,
                "Checkpoint",
                "Expected Format / Rule",
            ),
            {
                "Processor": "Intel Core Ultra 7",
                "Memory": "16GB DDR5",
            },
        )

    def test_ignores_missing_and_empty_values(self):
        dataframe = pd.DataFrame(
            {
                "Checkpoint": [
                    "Processor",
                    None,
                    " ",
                    "Storage",
                ],
                "Expected Format / Rule": [
                    "Intel Core Ultra 7",
                    "16GB DDR5",
                    "512GB SSD",
                    None,
                ],
            }
        )

        self.assertEqual(
            extract_source_specs(
                dataframe,
                "Checkpoint",
                "Expected Format / Rule",
            ),
            {
                "Processor": "Intel Core Ultra 7",
            },
        )


if __name__ == "__main__":
    unittest.main()