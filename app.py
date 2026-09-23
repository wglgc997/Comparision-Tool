"""
Offer Readiness QA Tool — Main GUI
Run with: streamlit run app.py
"""

import streamlit as st

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
st.info(
    "🚧 **Tool under construction...**\n\n"
    "This tool will help auditors compare:\n"
    "- **Source data** (Excel/CSV) — e.g., "
    "OfferReadiness audit spreadsheet\n"
    "- **Live PDP page** specs\n\n"
    "Using **59 checkpoint validation rules**"
)

# ── Sidebar (placeholder) ──
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("Mode and filters will go here.")
    st.markdown("---")
    st.header("📋 Rules")
    st.metric("Total Rules", 59)
    st.metric("🔴 Critical", 12)
    st.metric("🟠 High", 18)

# ── Footer ──
st.markdown("---")
st.caption(
    "Offer Readiness QA Tool v1.0 MVP | "
    "59 Checkpoint Rules | "
    "Built for Offer Readiness Audit Team"
)