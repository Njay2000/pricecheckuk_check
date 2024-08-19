import sys
import os
import logging
import pytest
import yaml
import pymysql

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def config():
    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../config/config.yaml")
    )
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def test_database_connection(config):
    db_config = config["database"]
    try:
        connection = pymysql.connect(
            host=db_config["host"],
            user=db_config["username"],
            password=db_config["password"],
            database=db_config["database_name"],
        )
        assert connection.open, "Database connection failed"
        connection.close()
    except pymysql.MySQLError as err:
        pytest.fail(f"Database connection error: {err}")
