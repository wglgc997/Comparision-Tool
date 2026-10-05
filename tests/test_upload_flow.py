import unittest
from datetime import date

import pandas as pd

from pdp_parser import analyze_pdp_content
from source_data import (
    detect_columns,
    extract_source_specs,
    filter_offer_rows,
)


class UploadFlowTests(unittest.TestCase):
    def test_processes_uploaded_offer_and_compares_specs(self):
        dataframe = pd.DataFrame(
            {
                "Country": [
                    "hkg_market_EN",
                    "hkg_market_EN",
                ],
                "Offer ID": [
                    "offer_1",
                    "offer_1",
                ],
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

        columns = detect_columns(dataframe)

        filtered = filter_offer_rows(
            dataframe,
            columns["offer_id"],
            "offer_1",
            columns["country"],
            "hkg_market_EN",
        )

        source_specs = extract_source_specs(
            filtered,
            columns["checkpoint"],
            columns["expected"],
        )

        results = analyze_pdp_content(
            source_specs,
            (
                "Processor: Intel Core Ultra 7\n"
                "Memory: 32GB DDR5"
            ),
            today=date(2026, 10, 5),
        )

        self.assertEqual(
            [result["status"] for result in results],
            ["PASS", "FAIL"],
        )


if __name__ == "__main__":
    unittest.main()
