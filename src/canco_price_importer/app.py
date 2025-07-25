import streamlit as st
import pandas as pd
from pathlib import Path
import base64

from src.canco_price_importer.apps.utils.functions import *


def run():
    # Set page config
    st.set_page_config(page_title="Canco Price Importer", page_icon="⛽", layout="wide")

    # Load logo
    logo_path = Path("assets/images/gen7_logo.png")
    if logo_path.exists():
        logo_base64 = base64.b64encode(logo_path.read_bytes()).decode()
        st.markdown(
            f"""
            <div style="text-align: right;">
                <img src="data:image/png;base64,{logo_base64}" width="160"/>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Title and subtitle
    st.write()
    st.markdown("## ⛽ Canco Price Importer")
    st.write()
    st.markdown(
        """
        The Canco Price Importer is designed to streamline your daily fuel pricing workflow
        by automatically consolidating wholesale price data directly from Canco.

        This tool efficiently imports and cleans raw pricing files, transforms the data into a standardized format,
        and outputs Bookworks-compatible CSVs ready for immediate use.
        
        By automating these steps, the app reduces manual effort, minimizes errors, and ensures your pricing data is always up to date
        — enabling your team to make faster, data-driven decisions with confidence.
        """
    )

    st.markdown("---")

    east_price = st.file_uploader("Upload Eastern rack price file from Canco 🔍", type=".xlsx")
    rest_price = st.file_uploader("Upload Rest of rack price file from Canco 🔍", type=".xlsx")
    original_csv = st.file_uploader("Upload Bookworks price importing format 🔍", type=".csv")

    if east_price and rest_price and original_csv:
        try:
            # Load CSV
            df_csv = pd.read_csv(original_csv)

            # Load and clean East
            df_east = pd.read_excel(east_price, engine="openpyxl")
            df_east = df_east.dropna(how="all").dropna(how="all", axis=1)
            formatted_datetime = get_effective_date(df_east)
            results = parse_east(df_east)
            df_east_cleaned = get_dataframe(results, df_csv.columns, formatted_datetime)

            # Load and clean Rest
            df_rest = pd.read_excel(rest_price, engine="openpyxl")
            df_rest = df_rest.dropna(how="all").dropna(how="all", axis=1)
            formatted_datetime = get_effective_date(df_rest)
            results = parse_rest(df_rest)
            df_rest_cleaned = get_dataframe(results, df_csv.columns, formatted_datetime)

            # Concatenate East and Rest
            df_concat = pd.concat([df_east_cleaned, df_rest_cleaned]).sort_values(
                by=["Supplier Code", "Inventory Item", "Cost"], ascending=True
            )
            df_concat = df_concat.drop_duplicates(
                subset=["Supplier Code", "Inventory Item"], keep="last"
            )

            # Merge new prices with original CSV
            df_merge = pd.merge(
                left=df_csv,
                right=df_concat[
                    ["Supplier Code", "Inventory Item", "Cost", "Effective DateTime"]
                ],
                how="left",
                on=["Supplier Code", "Inventory Item"],
                suffixes=("", "_new"),
            )

            # Overwrite only if there's an update
            df_update = df_csv.copy()
            df_update["Cost"] = df_merge["Cost_new"].combine_first(df_update["Cost"])
            df_update["Effective DateTime"] = df_merge[
                "Effective DateTime_new"
            ].combine_first(df_update["Effective DateTime"])

            st.write("")
            st.markdown("###### *Updated CSV.")
            st.dataframe(df_update)

            # Function to convert DataFrame to CSV bytes
            @st.cache_data
            def convert_for_download(df):
                return df.to_csv(index=False).encode("utf-8")

            csv = convert_for_download(df_update)
            today = get_today()

            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"canco_price_importer_{today}.csv",
                mime="text/csv",
                icon=":material/download:",
            )

        except Exception as e:
            st.error(
                "🐞 **Something went wrong!**\n\n"
                "Please make sure all file formats and structures are correct.\n"
                "If the issue persists, contact [Peter@gen7fuel.com](mailto:Peter@gen7fuel.com) for help 💌"
            )

            with st.expander("🔍 Show technical details (for debugging)"):
                st.exception(e)