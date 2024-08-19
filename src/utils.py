import pandas as pd
from src.logger import custom_logger as logger


def process_data(product_list):
    logger.info("Processing scraped data")
    df = pd.DataFrame(product_list)

    # Replace spaces with underscores and lowercase in DataFrame columns
    df.columns = [col.replace(" ", "_").lower() for col in df.columns]

    # Rename columns to match SQL schema
    column_renames = {
        "product_name": "product_name",
        "pricecheck_sku": "pricecheck_sku",
        "case_barcode": "case_barcode",
        "inner_quantity": "inner_quantity",
        "case_quantity": "case_quantity",
        "pallet_case_quantity": "pallet_case_quantity",
        "cases_per_layer": "cases_per_layer",
        "languages": "languages",
        "country_of_origin": "country_of_origin",
        "tariff_code": "tariff_code",
        "expiry_date": "expiry_date",
        "vat": "vat",
        "piece_price_(excl._vat)": "piece_price",
        "image_url": "image_url",
    }
    df = df.rename(columns=column_renames)

    # Handle NaN values and convert data types as necessary
    df = df.where(pd.notnull(df), None)
    df["inner_quantity"] = df["inner_quantity"].astype("int", errors="ignore")
    df["case_quantity"] = df["case_quantity"].astype("int", errors="ignore")
    df["pallet_case_quantity"] = df["pallet_case_quantity"].astype(
        "int", errors="ignore"
    )
    df["cases_per_layer"] = df["cases_per_layer"].astype("int", errors="ignore")
    df["vat"] = df["vat"].str.replace("%", "").astype("float", errors="ignore")

    return df
