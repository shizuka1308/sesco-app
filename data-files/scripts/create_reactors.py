import pandas as pd
from clickhouse_driver import Client
import numpy as np 
from dotenv import load_dotenv
import os

load_dotenv()

def load_data():
    try:
       # Read the file path from the .env file
        data_file_relative_path = os.getenv('DATA_FILE_PATH')
        # Get the current working directory
        current_directory = os.getcwd()
        # Construct the absolute path by joining the current directory and the relative path
        data_file_path = os.path.join(current_directory, data_file_relative_path)
        
        # Load data from the specified Excel file and select the first 7 columns
        data = pd.read_excel(data_file_path, usecols=range(7))
        # Rename the selected columns
        data.columns = [
            'YearOfUpdate',
            'PlantNameUnitNumber',
            'NRCReactorUnitWebPage',
            'DocketNumber',
            'LicenseNumber',
            'Location',
            'NRCRegion',
        ]

        # Extract state from the Location column and add it as a new column 'State'
        data['State'] = data['Location'].str.split(',').str[1].str.strip().str[:2]

        # Replace empty or missing values with NaN
        data = data.replace(r'^\s*$', np.nan, regex=True)

        # Fill missing values with None
        data = data.where(pd.notna(data), None)
        return data
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None