import requests
from datetime import datetime
import os

GENDER = YOUR GENDER # male/female
WEIGHT_KG = YOUR WEIGHT
HEIGHT_CM = YOUR HEIGHT
AGE = YOUR AGE

APP_ID =os.environ["NT_APP_ID"]
API_KEY = os.environ["NT_API_KEY"]
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = os.environ["SHEETY_ENDPOINT"]

headers = {
    "Content-Type": "application/json",
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": input("Tell me which exercise you did: "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

exercise_response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
exercise_response.raise_for_status()
print(exercise_response.text)

exercises_data = exercise_response.json()["exercises"]

sheety_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SHEETY_TOKEN}",
}

now = datetime.now()
today = now.strftime("%d/%m/%Y") # dd/mm/yyyy
time = now.strftime("%X") # hh:mm:ss

for exercise in exercises_data:
    sheet_input = {
        "workout": {
            "day": today,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    # print(sheet_body)
    sheety_response = requests.post(url=sheety_endpoint, json=sheet_input, headers=sheety_headers)
    sheety_response.raise_for_status()
    print(sheety_response.text)