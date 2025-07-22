import pandas as pd
import numpy as np


def preprocess_raw_file(dataframe):
    dataframe["Month"] = dataframe["UPC"][
        dataframe["UPC"].apply(lambda x: isinstance(x, str))
    ]
    dataframe["UPC"] = pd.to_numeric(dataframe["UPC"], errors="coerce")
    dataframe["Month"] = pd.to_datetime(dataframe["Month"], errors="coerce")
    dataframe["Month"] = dataframe["Month"].fillna(method="ffill")
    dataframe = dataframe[dataframe["UPC"].notnull()]

    cols_to_align = ["UPC", "Purch QTY", "QTY", "QTY, On Hand"]
    for col in cols_to_align:
        dataframe[col] = dataframe[col].apply(lambda x: int(float(x)))

    dataframe["Month"] = dataframe["Month"].dt.to_period("M")

    return dataframe


def get_vendor_pivot_table(dataframe, vendor_name):
    df_vendor = dataframe[dataframe["Vendor"] == vendor_name]

    min_month = df_vendor["Month"].min()
    max_month = df_vendor["Month"].max()
    unique_months = pd.date_range(
        min_month.to_timestamp().date(), max_month.to_timestamp().date(), freq="MS"
    ).to_period("M")

    df_pivot = pd.pivot_table(
        data=df_vendor,
        columns="Month",
        index="Item Name",
        values=["Purch QTY", "QTY", "QTY, On Hand"],
        aggfunc=np.sum,
    )
    df_pivot = df_pivot.swaplevel(axis=1).sort_index(axis=1, level=0)

    # insert missing months
    column_order = ["Purch QTY", "QTY", "QTY, On Hand"]
    new_columns = []
    for month in unique_months:
        for col_name in column_order:
            new_columns.append((month, col_name))
    df_pivot = df_pivot.reindex(columns=new_columns)
    df_pivot = df_pivot.fillna(0)
    return df_pivot, unique_months


def update_on_hand_qty(df_pivot, unique_months):
    for current_month in unique_months:
        if current_month == unique_months.min():
            df_pivot[(current_month, "QTY, On Hand")] = (
                df_pivot[(current_month, "Purch QTY")]
                - df_pivot[(current_month, "QTY")]
            )

        else:
            previous_month = current_month - 1
            df_pivot[(current_month, "QTY, On Hand")] = (
                df_pivot[(previous_month, "QTY, On Hand")]
                + df_pivot[(current_month, "Purch QTY")]
                - df_pivot[(current_month, "QTY")]
            )

    return df_pivot


def add_liq_percent(df_pivot, unique_months):

    for current_month in unique_months:
        qty = df_pivot[(current_month, "QTY")]
        on_hand = df_pivot[(current_month, "QTY, On Hand")]

        with np.errstate(divide="ignore", invalid="ignore"):
            liq_percent = qty / (qty + on_hand)
            liq_percent[np.isinf(liq_percent)] = 0
            liq_percent = np.nan_to_num(liq_percent, nan=0)  # handle NaNs if needed

        df_pivot[(current_month, "LIQ %")] = liq_percent
        column_order = ["Purch QTY", "QTY", "QTY, On Hand", "LIQ %"]

        new_columns = []
        for month in unique_months:
            for col_name in column_order:
                if (month, col_name) in df_pivot.columns:
                    new_columns.append((month, col_name))
        df_pivot = df_pivot[new_columns]  # Reassign with ordered columns

    return df_pivot


def add_sale_qty(df_pivot, unique_months):

    for current_month in unique_months:
        if current_month == unique_months.min():
            df_pivot["Sale QTY"] = df_pivot[(current_month, "QTY")]
        else:
            df_pivot["Sale QTY"] += df_pivot[(current_month, "QTY")]
    return df_pivot


def add_shelf_life(df_pivot, unique_months):

    df_pivot["Shelf Life"] = 0
    for current_month in unique_months:
        df_pivot.loc[df_pivot[(current_month, "QTY")] > 0, "Shelf Life"] += 1
    return df_pivot


def add_avg_sales_per_month(df_pivot):

    df_pivot["Avg Sales/Mnth"] = df_pivot["Sale QTY"] / df_pivot["Shelf Life"]
    df_pivot["Avg Sales/Mnth"] = df_pivot["Avg Sales/Mnth"].fillna(0)
    return df_pivot


def mround_excel(number, multiple):
    import math

    return (
        multiple * round((number + 1e-10) / multiple)
        if number >= 0
        else multiple * round((number - 1e-10) / multiple)
    )


def add_bi_weekly_sale_forecasting(df_pivot):

    df_pivot["Bi-Weekly Sale Fsct"] = df_pivot["Avg Sales/Mnth"].apply(
        lambda x: mround_excel(x / 2, 1)
    )

    return df_pivot


def add_safety_stock(df_pivot):

    df_pivot["Safety STK"] = df_pivot["Bi-Weekly Sale Fsct"].apply(
        lambda x: mround_excel(x * 0.5, 1)
    )
    return df_pivot


def add_order(df_pivot, latest_month):
    df_pivot.loc[
        df_pivot["Safety STK"] + df_pivot["Bi-Weekly Sale Fsct"]
        > df_pivot[(latest_month, "QTY, On Hand")],
        "Order",
    ] = (
        df_pivot["Safety STK"]
        + df_pivot["Bi-Weekly Sale Fsct"]
        - df_pivot[(latest_month, "QTY, On Hand")]
    )
    df_pivot.loc[
        df_pivot["Safety STK"] + df_pivot["Bi-Weekly Sale Fsct"]
        <= df_pivot[(latest_month, "QTY, On Hand")],
        "Order",
    ] = 0
    return df_pivot
