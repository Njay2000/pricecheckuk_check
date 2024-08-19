import pymysql
from src.logger import custom_logger as logger


def create_table(cursor, table_name):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        `barcode` VARCHAR(255) NOT NULL PRIMARY KEY,
        `product_name` TEXT,
        `pricecheck_sku` TEXT,
        `case_barcode` TEXT,
        `inner_quantity` INT,
        `case_quantity` INT,
        `pallet_case_quantity` INT,
        `cases_per_layer` INT,
        `languages` VARCHAR(100),
        `country_of_origin` VARCHAR(100),
        `tariff_code` VARCHAR(20),
        `expiry_date` DATE,
        `vat` DECIMAL(5, 2),
        `piece_price` VARCHAR(50),
        `image_url` TEXT
    );
    """
    cursor.execute(create_table_query)
    logger.info("Table created or verified successfully")
    logger.debug(f"SQL Create Table Query: {create_table_query}")


def insert_data(cursor, df, table_name):
    for _, row in df.iterrows():
        if row["barcode"] is None:
            logger.warning("Skipping row with no barcode")
            continue  # Skip rows with no barcode

        # Check if barcode already exists
        cursor.execute(
            f"SELECT COUNT(*) FROM `{table_name}` WHERE `barcode` = %s",
            (row["barcode"],),
        )
        if cursor.fetchone()[0] > 0:
            logger.info(f"Skipping duplicate barcode: {row['barcode']}")
            continue

        columns = ", ".join([f"`{col}`" for col in row.index])
        placeholders = ", ".join(["%s"] * len(row))
        insert_query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
        cursor.execute(insert_query, tuple(row))
        logger.debug(f"SQL Insert Query: {cursor.mogrify(insert_query, tuple(row))}")


def connect_to_db(cfg):
    logger.info("Connecting to the database")
    return pymysql.connect(
        host=cfg.database.host,
        user=cfg.database.username,
        password=cfg.database.password,
        database=cfg.database.database_name,
    )


def save_to_db(cfg, df):
    connection = connect_to_db(cfg)
    try:
        with connection.cursor() as cursor:
            create_table(cursor, cfg.database.table_name)
            insert_data(cursor, df, cfg.database.table_name)
        connection.commit()
        logger.info("Data saved to the database successfully")
    finally:
        connection.close()
