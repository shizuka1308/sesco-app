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