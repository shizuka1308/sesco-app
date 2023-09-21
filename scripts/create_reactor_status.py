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

def download_and_insert_data(client):
    """Download data from the URL and insert it into the reactor_status table."""
    url = os.getenv("DATA_FILE_URL")

    # Download the data from the URL
    response = requests.get(url)
    data_text = response.text

    # Read the data into a StringIO object for processing
    data_io = StringIO(data_text)

    # Process and insert data into the database
    for line in data_io:
        if not line.startswith("ReportDt"):  # Skip the header line
            # Split the line by "|" to extract fields
            fields = line.strip().split("|")

            if len(fields) < 3:
                continue  # Skip this row if it doesn't have enough fields

            # Extract relevant fields
            report_date_str, reactor_name, power = fields[:3]

            # Parse the original date format (e.g., "9/19/2023 12:00:00 AM")
            original_date = datetime.strptime(report_date_str, "%m/%d/%Y %I:%M:%S %p")

            # Convert the parsed date to the desired format (YYYY-MM-DD)
            formatted_date = original_date.strftime("%Y-%m-%d")

            # Check if the same date and reactor data already exist in the database
            query = f"""
            SELECT count() FROM reactor_status 
            WHERE report_date = '{formatted_date}' AND reactor_name = '{reactor_name}'
            """
            result = client.execute(query)

            # If no matching record exists, insert the data
            if result[0][0] == 0:
                insert_query = f"""
                INSERT INTO reactor_status (report_date, reactor_name, power)
                VALUES
                ('{formatted_date}', '{reactor_name}', {int(power)})
                """
                client.execute(insert_query)
                 
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