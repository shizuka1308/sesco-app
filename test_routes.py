import unittest
import json
from app import app  
from datetime import datetime

class TestReactorAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_filter_reactors_by_state(self):
        response = self.app.get('/reactors/filter?state=CA')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        for reactor in data:
            self.assertIn("State", reactor) 
            state = reactor["State"]
            self.assertEqual(state, "CA")

    def test_get_all_reactors(self):
        response = self.app.get('/reactors/all')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        for reactor in data:
            self.assertIn("State", reactor) 
            self.assertIn("DocketNumber", reactor) 
            self.assertIn("PlantNameUnitNumber", reactor) 

    def test_get_reactor_details(self):
        response = self.app.get('/reactors/details?reactor_name=Braidwood')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        for reactor in data:
            self.assertIn("Braidwood", reactor["PlantNameUnitNumber"])

    def test_get_reactor_by_license_number(self):
        response = self.app.get('/reactors/license?license_number=NPF-77')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        for reactor in data:
            self.assertIn("LicenseNumber", reactor) 
            license_number = reactor["LicenseNumber"]
            self.assertEqual(license_number, "NPF-77")

    def test_filter_reactors_on_outage_by_date(self):
        response = self.app.get('/reactors/on_outage/filter?start_date=2023-09-19&end_date=2023-09-20')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        for reactor in data:
            report_date = reactor["report_date"]
            original_date = datetime.strptime(report_date, '%a, %d %b %Y %H:%M:%S %Z')
            formatted_date = original_date.strftime('%Y-%m-%d')
            self.assertTrue("2023-09-19" <= formatted_date <= "2023-09-20")

    def test_get_last_known_outage_date_for_reactor(self):
        response = self.app.get('/reactors/last_known_outage?reactor_name=Clinton')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
    
        # Iterate over each dictionary in the data list
        for reactor in data:
            self.assertIn("reactor_name", reactor)  # Ensure "reactor_name" key exists in the dictionary
            reactor_name = reactor["reactor_name"]
            self.assertEqual(reactor_name, "Clinton")  # Check if the reactor_name is "Clinton"


if __name__ == '__main__':
    unittest.main()
