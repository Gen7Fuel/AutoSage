import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import base64

from src.demand_analysis_assistant.apps.utils.functions import *


def run():

    # Set page config
    st.set_page_config(page_title="Demand Analysis Assistant", page_icon="🚀", layout="wide")

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
    st.markdown("## 🚀 Demand Analysis Assistant")
    st.write()
    st.markdown(
        """
        The Demand Analysis Assistant empowers your inventory and purchasing team with data-driven insights
        by transforming vendor sales history into actionable forecasts.

        This tool ingests raw purchasing and sales data, cleans and organizes it into a pivot-based structure,
        and calculates key metrics like monthly sales averages, liquidity ratios, shelf life, and safety stock levels.
        It then uses these insights to automatically recommend bi-weekly order quantities.

        Whether you're managing fast-moving vapes or cannabis products with variable demand,
        the Demand Analysis Assistant helps ensure optimal stock levels and reduces the risk of over/under-ordering.
        """
    )

    st.markdown("---")


    file_to_format = st.file_uploader("Choose a file 🔍", type=".xlsx")

    try:

        if file_to_format:

            df = pd.read_excel(file_to_format, engine="openpyxl")

            st.write("")
            st.markdown("###### *Raw document uploaded.")
            st.dataframe(df)

            df.columns = df.iloc[7]
            df.columns.name = None

            df = df.loc[8:].reset_index(drop=True)
            df_processed = preprocess_raw_file(df)

            unique_vendors = df_processed["Vendor"].unique()

            option = st.selectbox(
                "Which vendor would you like to see?",
                (unique_vendors),
            )

            st.write("You selected:", option)

            target_vendor = option

            if target_vendor:
                ## Create Pivot table
                df_pivot, unique_months = get_vendor_pivot_table(
                    df_processed, target_vendor
                )
                df_pivot
                ### Update QTY, On Hand
                df_pivot = update_on_hand_qty(df_pivot, unique_months)
                ### Add LIQ %
                df_pivot = add_liq_percent(df_pivot, unique_months)
                ### Add Sale QTY
                df_pivot = add_sale_qty(df_pivot, unique_months)
                ### Add Shelf Life
                df_pivot = add_shelf_life(df_pivot, unique_months)
                ### Add Avg Sales/Mnth
                df_pivot = add_avg_sales_per_month(df_pivot)
                ### Add Bi-Weekly Sale Fsct
                df_pivot = add_bi_weekly_sale_forecasting(df_pivot)
                ### Add Safety STK
                df_pivot = add_safety_stock(df_pivot)
                ### Order
                latest_month = unique_months.max()
                df_pivot = add_order(df_pivot, latest_month)
                # sorting
                df_pivot = df_pivot.sort_values(by="Avg Sales/Mnth", ascending=False)
                # export
                # df_pivot.to_csv('df_pivot.csv')

                st.write("")
                st.markdown("###### *Converted document.")
                st.dataframe(df_pivot)

                def convert_for_download(df):
                    return df.to_csv().encode("utf-8")

                # Function to convert DataFrame to Excel bytes
                from io import BytesIO

                def to_excel_bytes(df):
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        df.to_excel(writer, index=True, sheet_name="Pivot")
                    output.seek(0)
                    return output

                excel_data = to_excel_bytes(df_pivot)

                # Streamlit download button
                st.download_button(
                    label="📥 Download processed document",
                    data=excel_data,
                    file_name="pivot_table.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

    except Exception as e:
        st.error(
            "🐞 **Something went wrong!**\n\n"
            "Please make sure all file formats and structures are correct.\n"
            "If the issue persists, contact [Peter@gen7fuel.com](mailto:Peter@gen7fuel.com) for help 💌"
        )

        with st.expander("🔍 Show technical details (for debugging)"):
            st.exception(e)