"""
Utilities for processing Offer Readiness source data.
"""

import pandas as pd

def read_source_file(uploaded_file):
    """Read an uploaded CSV or XLSX file into a Dataframe"""
    file_name = uploaded_file.name.casefold()

    uploaded_file.seek(0)

    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if file_name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

    raise ValueError(
        "Unsupported file format. Use a CSV or XLSX file."
    )








def detect_columns(dataframe):
    """Find required source columns, ignoring spaces and case."""
    normalized_columns = {
        "".join(
            character
            for character in str(column).casefold()
            if character.isalnum()
        ): column
        for column in dataframe.columns
    }

    return {
        "offer_id": normalized_columns.get("offerid"),
        "country": normalized_columns.get("country"),
        "checkpoint": normalized_columns.get("checkpoint"),
        "expected": normalized_columns.get("expectedformatrule"),
    }


def get_offer_ids(dataframe, offer_id_column):
    """Return sorted, unique, non-empty Offer IDs."""
    offer_ids = (
        dataframe[offer_id_column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    return sorted(
        offer_id
        for offer_id in offer_ids.unique()
        if offer_id
    )


def filter_offer_rows(
    dataframe,
    offer_id_column,
    selected_offer_id,
    country_column=None,
    selected_country=None,
):
    """Filter rows by Offer ID and optionally by country."""
    offer_id_values = (
        dataframe[offer_id_column]
        .astype("string")
        .str.strip()
    )

    mask = (
        offer_id_values
        .eq(selected_offer_id)
        .fillna(False)
    )

    if country_column is not None and selected_country is not None:
        country_values = (
            dataframe[country_column]
            .astype("string")
            .str.strip()
        )

        country_mask = (
            country_values
            .eq(selected_country)
            .fillna(False)
        )

        mask = mask & country_mask

    return dataframe.loc[mask].copy()


def extract_source_specs(
    dataframe,
    checkpoint_column,
    expected_column,
):
    """Extract complete checkpoint and expected-value pairs."""
    source_specs = {}

    for _, row in dataframe.iterrows():
        checkpoint = row[checkpoint_column]
        expected = row[expected_column]

        if pd.isna(checkpoint) or pd.isna(expected):
            continue

        checkpoint = str(checkpoint).strip()
        expected = str(expected).strip()

        if checkpoint and expected:
            source_specs[checkpoint] = expected

    return source_specs
