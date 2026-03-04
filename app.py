import streamlit as st
from main import run_pipeline

st.set_page_config(page_title="Portfolio Proposal Generator", layout="centered")

st.title("Portfolio Proposal Generator")

st.write(
"Upload a portfolio file with the following columns:\n"
"Q/NQ, Account, Symbol, Market Value, Unrealized"
)

portfolio_file = st.file_uploader(
    "Upload Portfolio File",
    type=["xlsx"]
)

if portfolio_file is not None:

    if st.button("Generate Report"):

        with st.spinner("Running analytics..."):

            ppt_bytes = run_pipeline(portfolio_file)

        st.success("Report Ready")

        st.download_button(
            label="Download Proposal",
            data=ppt_bytes,
            file_name="Proposal_Report.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )