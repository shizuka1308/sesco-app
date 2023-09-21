import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Set the base URL
BASE_URL = os.getenv('BASE_URL')

# Streamlit app
st.title("Nuclear Reactor Information")

# Function to make API requests and handle JSON decoding errors
def get_api_data(endpoint, params=None):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP Error: {http_err}")
    except json.JSONDecodeError as json_err:
        st.error(f"JSON Decode Error: {json_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    return None

# Function to display the list of reactors
def display_reactors(reactors):
    if not reactors:
        st.warning("No reactors found.")
    else:
        st.subheader("List of Reactors")
        for reactor in reactors:
            st.write(f"Name: {reactor['PlantNameUnitNumber']}")
            st.write(f"Location: {reactor['Location']}")
            st.write(f"State: {reactor['State']}")
            st.write(f"LicenseNumber: {reactor['LicenseNumber']}")
            st.write("---")

button_clicked = False  # Flag to track button clicks

# Sidebar for filtering reactors
st.sidebar.header("Filter Reactors")

# Filter by State
state_filter = st.sidebar.text_input("Filter by State (e.g., AR):", key="reactor_details_state_input")
if st.sidebar.button("Get Reactor"):
    button_clicked = True
    reactors = get_api_data("reactors/filter", {'state': state_filter})
    display_reactors(reactors)

# Filter by License Number
license_number = st.sidebar.text_input("Filter by License Number", key="reactor_details_license_input")
if st.sidebar.button("Get Reactors"):
    button_clicked = True
    reactors = get_api_data("reactors/license", {'license_number': license_number})
    display_reactors(reactors)

# Filter by Reactor Name for Details
reactor_name_input = st.sidebar.text_input("Reactor Name for Details:", key="reactor_details_input")
if st.sidebar.button("Get Reactor Details"):
    button_clicked = True
    reactors = get_api_data("reactors/details", {'reactor_name': reactor_name_input})
    display_reactors(reactors)

# Sidebar for listing reactors on outage
st.sidebar.subheader("List Reactors on Outage")
start_date = st.sidebar.text_input("Outage Start Date (YYYY-MM-DD):", key="outage_start_date_input")
end_date = st.sidebar.text_input("Outage End Date (YYYY-MM-DD):", key="outage_end_date_input")
if st.sidebar.button("List Reactors on Outage"):
    button_clicked = True
    reactors_on_outage = get_api_data("reactors/on_outage/filter", {'start_date': start_date, 'end_date': end_date})
    if reactors_on_outage:
        st.subheader("Reactors on Outage")
        for reactor in reactors_on_outage:
            st.write(f"Reactor Name: {reactor['reactor_name']}")
            st.write(f"Outage Date: {reactor['report_date']}")
    else:
        st.warning("No reactors on outage found.")

# Placeholder for getting the last known outage date
st.sidebar.subheader("Get Last Known Outage Date")
last_known_outage_reactor_input = st.sidebar.text_input("Reactor Name for Last Known Outage Date:", key="last_known_outage_reactor_input")
if st.sidebar.button("Get Last Known Outage Date"):
    button_clicked = True
    reactor_name = last_known_outage_reactor_input
    last_known_outage_reactor = get_api_data("reactors/last_known_outage", {'reactor_name': reactor_name})
    if last_known_outage_reactor:
        st.subheader(f"Last Known Outage Date for {reactor_name}")
        for reactor in last_known_outage_reactor:
            st.write(f"Reactor Name: {reactor['reactor_name']}")
            st.write(f"Outage Date: {reactor['report_date']}")
    else:
        st.warning("Reactor not found.")

# Display all reactors by default if no button is clicked
if button_clicked == False:
    reactors = get_api_data("reactors/all")
    display_reactors(reactors)