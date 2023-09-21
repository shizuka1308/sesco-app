import requests
from clickhouse_driver import Client
from io import StringIO
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def establish_clickhouse_connection():
    """Establish a connection to ClickHouse."""
    clickhouse_host = os.getenv("CLICKHOUSE_HOST")
    clickhouse_database = os.getenv("CLICKHOUSE_DATABASE")
    return Client(host=clickhouse_host, database=clickhouse_database)

def create_reactor_status_table(client):
    """Create the reactor_status table in ClickHouse if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS reactor_status
    (
        report_date Date,
        reactor_name String,
        power Int32
    )
    ENGINE = MergeTree()
    ORDER BY report_date;
    """
    client.execute(create_table_query)
    
def main():
    try:
        client = establish_clickhouse_connection()
        create_reactor_status_table(client)
        download_and_insert_data(client)
        print("Data processing and insertion completed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if client:
            client.disconnect()

if __name__ == "__main__":
    main()