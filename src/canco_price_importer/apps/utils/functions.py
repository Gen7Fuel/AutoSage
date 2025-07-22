import pandas as pd
from datetime import timedelta, date
from src.canco_price_importer.apps.utils.constants import *


def get_effective_date(data):
    original_datetime = pd.to_datetime(
        data["Unnamed: 1"][data["Unnamed: 1"].str.contains("Effective") == True]
        .str.split("Effective date: ")
        .str[-1]
    ).values[0]

    # Add 1 minute
    adjusted_datetime = pd.Timestamp(original_datetime) + timedelta(minutes=1)

    # Manually format date to '1/25/25 0:01'
    formatted_datetime = f"{adjusted_datetime.month}/{adjusted_datetime.day}/{adjusted_datetime.strftime('%y')} {adjusted_datetime.hour}:{adjusted_datetime.strftime('%M')}"

    return formatted_datetime


def parse_east(data):
    df = data.iloc[5:]

    results = []
    i = 0
    while i < len(df):
        row = df.iloc[i]

        # Detect city names (non-NaN in column 0, NaNs elsewhere)
        if pd.notna(row[0]) and row[1:].isna().all():
            city = row[0]
            # Look ahead to find 'Base Price' row
            for j in range(i + 1, min(i + 10, len(df))):
                if str(df.iloc[j, 0]).strip() == "Base Price":
                    grades = df.iloc[
                        j - 1
                    ]  # One row above 'Base Price' has fuel grade headers
                    prices = df.iloc[j]

                    price_dict = {"grades": {}}
                    for k in range(1, len(grades)):
                        if pd.notna(grades[k]):
                            price_dict["grades"][grades[k]] = prices[k]
                            if grades[k] == "Diesel":
                                price_dict["grades"]["Winter Diesel"] = prices[k]
                    result = {"city": city}
                    result.update(price_dict)
                    results.append(result)
                    i = j  # skip to after 'Base Price'
                    break
        i += 1
    return results


def parse_rest(data):
    df = data.iloc[5:-6]

    results = []

    for row_num in range(len(df)):
        row = df.iloc[row_num]

        result = {}
        result["grades"] = {}

        if pd.notna(row[0]) and pd.isna(row[1]):
            city = row[0].split(",")[0]
            result["city"] = city

            for j in range(row_num + 2, min(row_num + 5, len(df))):
                grade = df.iloc[j][0]
                price = df.iloc[j][1]
                result["grades"][grade] = price
                if grade == "Diesel":
                    result["grades"]["Dyd Diesel"] = price
                    result["grades"]["Winter Diesel"] = price
            results.append(result)

    return results


def get_dataframe(results, columns, formatted_datetime):
    num = 0
    df = pd.DataFrame(columns=columns)
    for result in results:
        if result["city"] in supplier_code_map:
            for grade, price in result["grades"].items():
                df.loc[num] = [
                    supplier_code_map[result["city"]],
                    supplier_item_map[inventory_item_map[grade]],
                    inventory_item_map[grade],
                    formatted_datetime,
                    price,
                ]
                num += 1
    return df


def get_today():
    today = date.today()
    today = f"{today.month}_{today.day}_{today.strftime('%y')}"
    return today
