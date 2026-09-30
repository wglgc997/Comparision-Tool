"""
Offer Readiness QA Tool — Main GUI
Run with: streamlit run app.py
"""

import streamlit as st

from rules import get_all_rules, get_by_category
from comparison import compare_specs, parse_specs

#Page config
st.set_page_config(
    page_title="Offer Readiness QA Tool",
    page_icon="🔍",
    layout="wide",
)

#Header
st.title("🔍 Offer Readiness QA Tool")
st.markdown(
    "Compare Source data(Excel/CSV) against"
    "live PDP page specs"
)
st.markdown("___")

# ── Main Area (placeholder) ──
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
        st.warning(
            "Enter at least one valid source specification using "
            " `Checkpoint: Value`."
        )
    elif not live_specs:
        st.warning(
            "Enter at least one valid live specification using "
            "`Checkpoint: Value`."
        )
    else:
        comparison_results = compare_specs(
            source_specs,
            live_specs,
        )

        st.markdown("### Comparison Results")
        st.dataframe(
            comparison_results,
            use_container_width=True,
            hide_index=True,
        )


# ── Sidebar (placeholder) ──
with st.sidebar:
    st.header("Settings")
    st.markdown("Mode and additional filters will go here.")
    st.markdown("---")

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

    st.metric("Total Rules", len(all_rules))
    st.caption(
        f"Showing {len(filtered_rules)} rule(s) "
        f"in {selected_category}"
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