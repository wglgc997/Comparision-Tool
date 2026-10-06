import unittest
from io import BytesIO

import pandas as pd

from source_data import (
    detect_columns,
    extract_source_specs,
    filter_offer_rows,
    get_offer_ids,
    read_source_file,
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


class UploadedFile(BytesIO):
    def __init__(self, content, name):
        super().__init__(content)
        self.name = name


class ReadSourceFileTests(unittest.TestCase):
    def test_reads_csv_file(self):
        uploaded_file = UploadedFile(
            (
                b"Country,Offer ID,Checkpoint\n"
                b"hkg_market_EN,offer_1,Processor\n"
            ),
            "offers.csv",
        )

        result = read_source_file(uploaded_file)

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result.iloc[0]["Offer ID"],
            "offer_1",
        )

    def test_reads_cp1252_csv_file(self):
        uploaded_file = UploadedFile(
            (
                "Country,Offer ID,Checkpoint\n"
                "hkg_market_EN,offer_1,Configuração\n"
            ).encode("cp1252"),
            "offers.csv",
        )

        result = read_source_file(uploaded_file)

        self.assertEqual(
            result.iloc[0]["Checkpoint"],
            "Configuração",
        )

    def test_reads_xlsx_file(self):
        source_dataframe = pd.DataFrame(
            {
                "Country": ["hkg_market_EN"],
                "Offer ID": ["offer_1"],
                "Checkpoint": ["Processor"],
            }
        )

        excel_content = BytesIO()
        source_dataframe.to_excel(
            excel_content,
            index=False,
        )

        uploaded_file = UploadedFile(
            excel_content.getvalue(),
            "offers.xlsx",
        )

        result = read_source_file(uploaded_file)

        pd.testing.assert_frame_equal(
            result,
            source_dataframe,
        )

    def test_rejects_unsupported_file_format(self):
        uploaded_file = UploadedFile(
            b"invalid content",
            "offers.txt",
        )

        with self.assertRaisesRegex(
            ValueError,
            "Unsupported file format",
        ):
            read_source_file(uploaded_file)

    def test_rejects_invalid_xlsx_content(self):
        uploaded_file = UploadedFile(
            b"invalid Excel content",
            "offers.xlsx",
        )

        with self.assertRaises(ValueError):
            read_source_file(uploaded_file)


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
