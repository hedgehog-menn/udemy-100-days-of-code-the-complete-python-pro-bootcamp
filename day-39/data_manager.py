import requests
import os

class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self._token = os.environ["SHEETY_TOKEN"]
        self._sheety_endpoint = os.environ["SHEETY_ENDPOINT"]
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}",
        }

    def get_data(self):
        sheety_response = requests.get(url=self._sheety_endpoint, headers=self._headers)
        sheety_response.raise_for_status()
        return sheety_response.json()["prices"]

    def update_data_row(self, new_data_row):
        sheety_response = requests.put(url=f"{self._sheety_endpoint}/{new_data_row['id']}", headers=self._headers, json={ "price": new_data_row})
        sheety_response.raise_for_status()