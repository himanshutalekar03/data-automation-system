import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_processor import load_file, clean_data, generate_summary, validate_data
from database import save_to_database
from email_sender import send_email

st.set_page_config(page_title="Business Data Automation Tool", layout="wide")

st.title("📊 Business Data Automation Tool")
st.write("Enterprise Data Processing System")

uploaded_files = st.file_uploader(
    "Upload CSV/Excel files (batch supported)",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

if uploaded_files:

    for uploaded_file in uploaded_files:

        st.divider()
        st.subheader(f"Processing: {uploaded_file.name}")

        df = load_file(uploaded_file)

        st.write("### Original Data")
        st.dataframe(df.head())

        # Data validation
        issues = validate_data(df)
        if issues:
            st.warning("Validation Issues:")
            for issue in issues:
                st.write("-", issue)

        if st.button(f"Clean Data - {uploaded_file.name}"):

            cleaned_df, original_rows, cleaned_rows, original_cols, cleaned_cols = clean_data(df)

            st.write("### Cleaned Data")
            st.dataframe(cleaned_df.head())

            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Original Rows", original_rows)
            col2.metric("Cleaned Rows", cleaned_rows)
            col3.metric("Original Columns", original_cols)
            col4.metric("Cleaned Columns", cleaned_cols)

            # Summary
            st.write("### Data Summary")
            st.json(generate_summary(cleaned_df))

            # Charts
            st.write("### Data Visualization")

            numeric_cols = cleaned_df.select_dtypes(include=["int64", "float64"]).columns

            if len(numeric_cols) > 0:
                fig, ax = plt.subplots()
                cleaned_df[numeric_cols].hist(ax=ax)
                st.pyplot(fig)

            # Save to database
            if st.button("Save to Database"):
                save_to_database(cleaned_df)
                st.success("Saved to database!")

            # Download cleaned data
            csv = cleaned_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Cleaned Data",
                data=csv,
                file_name="cleaned_data.csv"
            )

            # Email report
            email = st.text_input("Enter email to receive report")
            if st.button("Send Email Report") and email:
                send_email(email, "Your data has been processed successfully.")
                st.success("Email sent!")
