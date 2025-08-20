import time
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from datetime import datetime, timedelta
from notification_manager import NotificationManager

# Set your origin airport code
ORIGIN_CITY_IATA = "TPE" # Taipai, Taiwan

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_data()

# # Find IATA Code
for row in sheet_data:
    if row["iataCode"] in ["", "N/A", "Not Found"]:
        print("Find missing IATA Code...")
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        print(f"{row["city"]} - {row["iataCode"]}")

        data_manager.update_data_row(row)
        # slowing down requests to avoid rate limit
        time.sleep(2)

# Find cheap flights
date_format = "%Y-%m-%d" # yyyy-mm-dd
depart_date = (datetime.now() + timedelta(days=1)).strftime(date_format) # tomorrow
return_date = (datetime.now() + timedelta(days=30*6)).strftime(date_format) # six months onwards

print(f"Find cheapest flights from {ORIGIN_CITY_IATA}")
for row in sheet_data:
    found_flights = flight_search.check_flights(origin_city_code=ORIGIN_CITY_IATA, destination_city_code=row["iataCode"], from_time=depart_date, to_time=return_date)
    cheapest_flight = find_cheapest_flight(found_flights)
    print(f"{row['city']} ({row["iataCode"]}): ${cheapest_flight.price}")

    row["lowestPrice"] = cheapest_flight.price
    data_manager.update_data_row(row)

    if cheapest_flight.price != "N/A" and cheapest_flight.price < row["lowestPrice"]:
        print(f"Lower price flight found to {row['city']}!")
        # notification_manager.send_sms(
        #     message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
        #                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
        #                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        # )

        # SMS not working? Try whatsapp instead.
        notification_manager.send_whatsapp(
            message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )

    # slowing down requests to avoid rate limit
    time.sleep(2)