"""
Offer Readiness QA Tool — Main GUI
Run with: streamlit run app.py
"""

import pandas as pd
import streamlit as st

from comparison import (
    compare_specs,
    get_summary,
    parse_specs,
)
from pdp_parser import analyze_pdp_content, get_audit_summary
from rules import get_all_rules, get_by_category
from source_data import (
    detect_columns,
    extract_source_specs,
    filter_offer_rows,
    get_offer_ids,
    read_source_file,
)

# Page configuration
st.set_page_config(
    page_title="Offer Readiness QA Tool",
    page_icon="🔍",
    layout="wide",
)

if "comparison_results" not in st.session_state:
    st.session_state["comparison_results"] = None

# Header
st.title("🔍 Offer Readiness QA Tool")
st.markdown(
    "Compare source data (Excel/CSV) against "
    "live PDP page specifications."
)
st.markdown("___")

# Manual comparison
st.subheader("Manual Spec Comparison")
st.caption(
    "Enter one specification per line using the format "
    "`Checkpoint: Value`."
)

source_column, live_column = st.columns(2)

with source_column:
    st.markdown("#### Source Specifications")
    source_text = st.text_area(
        "Source specifications",
        height=300,
        placeholder=(
            "Processor: Intel Core Ultra 7\n"
            "Memory: 16GB DDR5\n"
            "Storage: 512GB SSD"
        ),
        label_visibility="collapsed",
    )

with live_column:
    st.markdown("#### Live PDP Specifications")
    live_text = st.text_area(
        "Live PDP specifications",
        height=300,
        placeholder=(
            "Processor: Intel Core Ultra 7\n"
            "Memory: 32GB DDR5\n"
            "Storage: 512GB SSD"
        ),
        label_visibility="collapsed",
    )

compare_clicked = st.button(
    "Compare Specifications",
    type="primary",
    use_container_width=True,
)

if compare_clicked:
    source_specs = parse_specs(source_text)
    live_specs = parse_specs(live_text)

    if not source_specs:
        st.session_state["comparison_results"] = None
        st.warning(
            "Enter at least one valid source specification using "
            "`Checkpoint: Value`."
        )
    elif not live_specs:
        st.session_state["comparison_results"] = None
        st.warning(
            "Enter at least one valid live specification using "
            "`Checkpoint: Value`."
        )
    else:
        st.session_state["comparison_results"] = compare_specs(
            source_specs,
            live_specs,
        )

comparison_results = st.session_state["comparison_results"]

if comparison_results is not None:
    summary = get_summary(comparison_results)
    result_dataframe = pd.DataFrame(comparison_results)

    overall_status = summary["overall_status"]

    if overall_status == "PASS":
        st.success(
            "Overall Status: PASS - all specifications match."
        )
    elif overall_status == "FAIL":
        st.error(
            "Overall Status: FAIL - one or more specifications "
            "do not match."
        )
    else:
        st.info(
            "Overall Status: NO DATA - no specifications were compared."
        )

    total_column, passed_column, failed_column, score_column = (
        st.columns(4)
    )

    total_column.metric("Total", summary["total"])
    passed_column.metric("Passed", summary["passed"])
    failed_column.metric("Failed", summary["failed"])
    score_column.metric(
        "Score",
        f"{summary['score']:.2f}%",
    )

    st.markdown("### Comparison Results")
    st.dataframe(
        result_dataframe,
        use_container_width=True,
        hide_index=True,
    )

    csv_data = result_dataframe.to_csv(
        index=False,
    ).encode("utf-8-sig")

    st.download_button(
        label="Download Results as CSV",
        data=csv_data,
        file_name="results.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.markdown("---")
st.subheader("Upload Source File")
st.caption(
    "Upload an Offer Readiness CSV or Excel file, "
    "then select an Offer ID."
)

uploaded_file = st.file_uploader(
    "Choose a source file",
    type=["csv", "xlsx"],
    help="Supported formats: CSV and XLSX.",
)

# Validation-rule reference
with st.sidebar:
    st.header("Validation Rules")

    all_rules = get_all_rules()
    categories = sorted(
        {rule["category"] for rule in all_rules}
    )

    selected_category = st.selectbox(
        "Category",
        options=categories,
    )

    filtered_rules = get_by_category(selected_category)

    documented_rule_count = sum(
        rule["status"] == "documented"
        for rule in all_rules
    )

    st.metric("Documented Rules", documented_rule_count)
    st.caption(
        f"Showing {len(filtered_rules)} rule(s) "
        f"in {selected_category}"
    )
    st.caption(
        "Rules without complete definitions are shown for reference "
        "and are not evaluated automatically."
    )

    for rule in filtered_rules:
        with st.expander(
            f"#{rule['id']} — {rule['checkpoint']}"
        ):
            st.write(
                f"**Expected:** "
                f"{rule['expected'] or 'Not documented'}"
            )
            st.write(
                f"**Logic:** "
                f"{rule['logic'] or 'Not documented'}"
            )
            st.write(
                f"**Why it matters:** "
                f"{rule['why_it_matters'] or 'Not documented'}"
            )
            st.write(
                f"**Severity:** "
                f"{rule['severity'] or 'Not assigned'}"
            )
            st.write(
                f"**Status:** {rule['status']}"
            )

            if rule["notes"]:
                st.info(rule["notes"])

if uploaded_file is not None:
    try:
        uploaded_dataframe = read_source_file(uploaded_file)
    except Exception as error:
        st.error(
            f"Could not read the uploaded file: {error}"
        )

    else:
        source_columns = detect_columns(uploaded_dataframe)
        offer_id_column = source_columns["offer_id"]

        if offer_id_column is None:
            st.error(
                "The uploaded file does not contain an Offer ID column."
            )
            st.caption(
                "Available columns: "
                + ", ".join(
                    str(column)
                    for column in uploaded_dataframe.columns
                )
            )
        else:
            offer_ids = get_offer_ids(
                uploaded_dataframe,
                offer_id_column,
            )

            if not offer_ids:
                st.warning(
                    "The Offer ID column does not contain any values."
                )
            else:
                selected_offer_id = st.selectbox(
                    "Select an Offer ID",
                    options=offer_ids,
                )

                st.success(
                    f"Loaded {len(uploaded_dataframe)} rows and "
                    f"found {len(offer_ids)} unique Offer IDs."
                )


                offer_dataframe = filter_offer_rows(
                    uploaded_dataframe,
                    offer_id_column,
                    selected_offer_id,
                )

                country_column = source_columns["country"]
                checkpoint_column = source_columns["checkpoint"]
                expected_column = source_columns["expected"]

                required_columns = {
                    "Country": country_column,
                    "Checkpoint": checkpoint_column,
                    "Expected Format / Rule": expected_column,
                }
                missing_columns = [
                    name
                    for name, column in required_columns.items()
                    if column is None
                ]

                if missing_columns:
                    st.error(
                        "The uploaded file is missing required columns: "
                        + ", ".join(missing_columns)
                    )
                else:
                    countries = (
                        offer_dataframe[country_column]
                        .dropna()
                        .astype(str)
                        .str.strip()
                    )
                    countries = sorted(
                        country
                        for country in countries.unique()
                        if country
                    )

                    if not countries:
                        st.warning(
                            "The selected Offer ID has no country values."
                        )
                    else:
                        selected_country = st.selectbox(
                            "Select a Country / Market",
                            options=countries,
                        )

                        filtered_offer_dataframe = filter_offer_rows(
                            uploaded_dataframe,
                            offer_id_column,
                            selected_offer_id,
                            country_column,
                            selected_country,
                        )

                        st.markdown("### Selected Offer Data")
                        st.caption(
                            f"Offer `{selected_offer_id}` in "
                            f"`{selected_country}` contains "
                            f"{len(filtered_offer_dataframe)} row(s)."
                        )
                        st.dataframe(
                            filtered_offer_dataframe,
                            use_container_width=True,
                            hide_index=True,
                        )

                        uploaded_source_specs = extract_source_specs(
                            filtered_offer_dataframe,
                            checkpoint_column,
                            expected_column,
                        )

                        if not uploaded_source_specs:
                            st.warning(
                                "The selected offer and market have no "
                                "complete Checkpoint and Expected Format "
                                "/ Rule values to compare."
                            )
                        else:
                            st.success(
                                f"Extracted "
                                f"{len(uploaded_source_specs)} "
                                f"source specification(s)."
                            )

                            source_preview = pd.DataFrame(
                                [
                                    {
                                        "checkpoint": checkpoint,
                                        "expected": expected,
                                    }
                                    for checkpoint, expected
                                    in uploaded_source_specs.items()
                                ]
                            )

                            st.markdown(
                                "### Extracted Source Specifications"
                            )
                            st.dataframe(
                                source_preview,
                                use_container_width=True,
                                hide_index=True,
                            )

                            uploaded_live_text = st.text_area(
                                "Content copied from the live PDP",
                                height=250,
                                placeholder=(
                                    "Dell Pro 7 Series 14 Laptop\n"
                                    "AMD Ryzen AI 5 PRO 435, 6 Cores\n"
                                    "Windows 11 Pro\n"
                                    "16 GB DDR5\n"
                                    "14\" Non Touch FHD (1920x1200)"
                                ),
                            )
                            st.caption(
                                "Copy the visible product content from the "
                                "Dell page and paste it here. Supported "
                                "checkpoints are evaluated automatically; "
                                "the others are marked REVIEW."
                            )

                            compare_uploaded_clicked = st.button(
                                "Compare Uploaded Offer",
                                type="primary",
                                use_container_width=True,
                            )

                            if compare_uploaded_clicked:
                                if not uploaded_live_text.strip():
                                    st.warning(
                                        "Paste the content copied from the "
                                        "live PDP before comparing."
                                    )
                                else:
                                    uploaded_results = analyze_pdp_content(
                                        uploaded_source_specs,
                                        uploaded_live_text,
                                    )
                                    uploaded_summary = get_audit_summary(
                                        uploaded_results
                                    )
                                    uploaded_result_dataframe = pd.DataFrame(
                                        uploaded_results
                                    )

                                    if (
                                        uploaded_summary["overall_status"]
                                        == "PASS"
                                    ):
                                        st.success(
                                            "Overall Status: PASS - all "
                                            "checkpoints passed."
                                        )
                                    else:
                                        if (
                                            uploaded_summary["overall_status"]
                                            == "REVIEW"
                                        ):
                                            st.warning(
                                                "Overall Status: REVIEW - "
                                                "manual review is required."
                                            )
                                        else:
                                            st.error(
                                                "Overall Status: FAIL - one "
                                                "or more checkpoints failed."
                                            )

                                    (
                                        total_column,
                                        passed_column,
                                        failed_column,
                                        review_column,
                                        score_column,
                                    ) = st.columns(5)

                                    total_column.metric(
                                        "Total",
                                        uploaded_summary["total"],
                                    )
                                    passed_column.metric(
                                        "Passed",
                                        uploaded_summary["passed"],
                                    )
                                    failed_column.metric(
                                        "Failed",
                                        uploaded_summary["failed"],
                                    )
                                    review_column.metric(
                                        "Review",
                                        uploaded_summary["review"],
                                    )
                                    score_column.metric(
                                        "Score",
                                        f"{uploaded_summary['score']:.2f}%",
                                    )

                                    st.dataframe(
                                        uploaded_result_dataframe,
                                        use_container_width=True,
                                        hide_index=True,
                                    )

                                    uploaded_csv_result = (
                                        uploaded_result_dataframe
                                        .to_csv(index=False)
                                        .encode("utf-8-sig")
                                    )

                                    st.download_button(
                                        "Download Uploaded Offer Results",
                                        data=uploaded_csv_result,
                                        file_name=(
                                            f"{selected_offer_id}_"
                                            f"{selected_country}_results.csv"
                                        ),
                                        mime="text/csv",
                                        use_container_width=True,
                                    )
