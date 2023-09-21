from clickhouse_driver import Client
from dotenv import load_dotenv
import os

load_dotenv()

def create_clickhouse_client():
    clickhouse_host = os.getenv('CLICKHOUSE_HOST')  
    clickhouse_database = os.getenv('CLICKHOUSE_DATABASE')

    return Client(host=clickhouse_host, database=clickhouse_database)

# Function to retrieve all reactors with an optional filter by state
def get_all_reactors(state_filter=None):
    client = create_clickhouse_client()
    query = f"SELECT * FROM reactors"
    if state_filter:
        query += f" WHERE State ILIKE '%{state_filter}%'"
    result = client.execute(query)
    client.disconnect()
    reactors_list = []
    for row in result:
        reactor_dict = {
            "YearOfUpdate": row[0],
            "PlantNameUnitNumber": row[1],
            "NRCReactorUnitWebPage": row[2],
            "DocketNumber": row[3],
            "LicenseNumber": row[4],
            "Location": row[5], 
            "NRCRegion": row[6],  
            "State": row[7],  
        }
        reactors_list.append(reactor_dict)

    return reactors_list

# Function to retrieve reactor details by name
def get_reactor_details(reactor_name):
    client = create_clickhouse_client()
    query = f"SELECT * FROM reactors WHERE PlantNameUnitNumber ILIKE '%{reactor_name}%'"
    result = client.execute(query)
    client.disconnect()
    reactors_list = []
    for row in result:
        reactor_dict = {
            "YearOfUpdate": row[0],
            "PlantNameUnitNumber": row[1],
            "NRCReactorUnitWebPage": row[2],
            "DocketNumber": row[3],
            "LicenseNumber": row[4],
            "Location": row[5], 
            "NRCRegion": row[6],  
            "State": row[7],  
        }
        reactors_list.append(reactor_dict)

    return reactors_list if result else None

# Function to list reactors on outage for a given date range
def list_reactors_on_outage_query(start_date, end_date):
    client = create_clickhouse_client()
    query = f"""
        SELECT reactor_name, report_date
        FROM reactor_status
        WHERE report_date BETWEEN '{start_date}' AND '{end_date}' AND power = 0
    """
    result = client.execute(query)
    client.disconnect()
    reactors_list = []
    for row in result:
        reactor_dict = {
            "reactor_name": row[0],
            "report_date": row[1]
        }
        reactors_list.append(reactor_dict)

    return reactors_list

# Function to get the last known outage date of a reactor
def get_last_known_outage_date(reactor_name):
    client = create_clickhouse_client()
    query = f"""
        SELECT reactor_name, report_date
        FROM reactor_status
        WHERE reactor_name ILIKE '%{reactor_name}%' AND power = 0
        ORDER BY report_date DESC
        LIMIT 1
    """
    result = client.execute(query)
    client.disconnect()
    reactors_list = []
    for row in result:
        reactor_dict = {
            "reactor_name": row[0],
            "report_date": row[1]
        }
        reactors_list.append(reactor_dict)

    return reactors_list if result else None

# Function to retrieve reactor details by license number
def get_reactor_by_license_number(license_number):
    client = create_clickhouse_client()
    query = f"""
        SELECT *
        FROM reactors
        WHERE LicenseNumber ILIKE '%{license_number}%'
        LIMIT 1
    """
    result = client.execute(query)
    client.disconnect()
    reactors_list = []
    for row in result:
        reactor_dict = {
            "YearOfUpdate": row[0],
            "PlantNameUnitNumber": row[1],
            "NRCReactorUnitWebPage": row[2],
            "DocketNumber": row[3],
            "LicenseNumber": row[4],
            "Location": row[5], 
            "NRCRegion": row[6],  
            "State": row[7],  
        }
        reactors_list.append(reactor_dict)

    return reactors_list if result else None
