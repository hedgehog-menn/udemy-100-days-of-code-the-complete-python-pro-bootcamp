import requests
import os

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]
        self._amadeus_endpoint = "https://test.api.amadeus.com"
        self._token = self._get_new_token()

    def _get_new_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }
        response = requests.post(url=f"{self._amadeus_endpoint}/v1/security/oauth2/token", headers=headers, data=body)

        # New bearer token. Typically expires in 1799 seconds (30min)
        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def get_destination_code(self, city_name: str):
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        parameter = {
            "keyword": city_name,
            "max": 3,
        }

        response = requests.get(url=f"{self._amadeus_endpoint}/v1/reference-data/locations/cities", headers=headers,
                                params=parameter)

        # print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        parameter = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time,
            "returnDate": to_time,
            "nonStop": "true",
            "currencyCode": "USD",
            "adults": 1,
            "max": 10,
        }

        response = requests.get(url=f"{self._amadeus_endpoint}/v2/shopping/flight-offers", headers=headers,
                                params=parameter)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()