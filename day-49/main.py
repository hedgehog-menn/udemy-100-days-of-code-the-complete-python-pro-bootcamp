import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ACCOUNT_EMAIL = "student@test.com"
# ACCOUNT_PASSWORD = "password123"

# ACCOUNT_NAME = "KenTesting"
ACCOUNT_EMAIL = "bphjhp@tnraod.ctrs"
ACCOUNT_PASSWORD = "sivcas-wywtok-wUvmi2"
GYM_URL = "https://appbrewery.github.io/gym/"

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
# If True, you need to *manually* QUIT Chrome before you re-run the script.
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)

driver.get(GYM_URL)

# Alternative to using time.sleep(): use a standalone wait object
wait = WebDriverWait(driver, 2)

# Simple retry wrapper
def retry(func, retries=7, description=None):
    for i in range(retries):
        print(f"Trying {description}. Attempt: {i + 1}")
        try:
            return func()
        except TimeoutException:
            if i == retries - 1:
                raise
            time.sleep(1)
def login():
    # Click login button to go to login page
    login_btn =  wait.until(ec.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()

    # Fill in login form
    email_input =  wait.until(ec.presence_of_element_located((By.ID, "email-input")))
    email_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)
    pass_input = wait.until(ec.presence_of_element_located((By.ID, "password-input")))
    pass_input.clear()
    pass_input.send_keys(ACCOUNT_PASSWORD)
    # Click Login
    submit_btn = driver.find_element(By.ID, "submit-button")
    submit_btn.click()

    # Wait for schedule page to load
    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

# Function to book a class process that checks if the button text changed with retry
def book_class(booking_button):
    booking_button.click()
    # Wait for button state to change - will time out if booking failed
    wait.until(lambda d: booking_button.text == "Booked")

# Put the entire login flow into the retry-wrapper
retry(login, description="login")

class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")
processed_classes = []
count_booking = 0 # to book
count_waitlisting = 0 # to join waitlist
count_already = 0 # already booked/on waitlist

for card in class_cards:
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    # Check if this is a Tuesday OR Thursday
    if "Tue" in day_title or "Thu" in day_title:
        time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in time_text:
            class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")
            class_info = f"{class_name} on {day_title}"

            match button.text:
                case "Booked":
                    count_already += 1
                    print(f"✓ Already booked: {class_info}")
                    processed_classes.append(f"[Booked]: {class_info}")
                case "Waitlisted":
                    count_already += 1
                    print(f"✓ Already on waitlist: {class_info}")
                    processed_classes.append(f"[Waitlisted]: {class_info}")
                case "Join Waitlist":
                    # Use retry for entire booking action
                    retry(lambda: book_class(button), description="Booking")
                    count_waitlisting += 1
                    print(f"✓ Joined waitlist for: {class_info}")
                    processed_classes.append(f"[New Waitlisted]: {class_info}")
                    time.sleep(0.5)
                case _:
                    # Use retry for entire waitlist action
                    retry(lambda: book_class(button), description="Waitlisting")
                    count_booking += 1
                    print(f"✓ Booked: {class_info}")
                    processed_classes.append(f"[New Booked]: {class_info}")
                    time.sleep(0.5)

# print("\n--- BOOKING SUMMARY ---")
# print(f"Classes booked: {count_booking}")
# print(f"Waitlists joined: {count_waitlisting}")
# print(f"Already booked/waitlisted: {count_already}")
# print(f"Total Tuesday & Thursday 6pm classes processed: {count_booking + count_waitlisting + count_already}")
#
# print("\n--- DETAILED CLASS LIST ---")
# for processed_class in processed_classes:
#     print(f"  • {processed_class}")

total_booked = count_booking + count_waitlisting + count_already
print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_booked} ---")
print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")

# Function to navigate to my bookings with retry
def get_my_bookings():
    # Navigate to My Bookings page
    my_bookings_link = driver.find_element(By.ID, "my-bookings-link")
    my_bookings_link.click()

    # Wait for My Bookings page to load
    wait.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))

    # Find ALL booking cards (both confirmed and waitlist)
    cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")

    # Ensure we actually found cards - if empty, the page might not have loaded
    if not cards:
        raise TimeoutException("No booking cards found - page may not have loaded")
    return cards

# Count all Tuesday/Thursday 6pm bookings
verified_count = 0

# Put navigation to the Bookings page and get cards in the retry wrapper
all_cards = retry(get_my_bookings, description="Get my bookings")

for card in all_cards:
    try:
        when_paragraph = card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
        when_text = when_paragraph.text

        # Check if it's a Tuesday or Thursday 6pm class
        if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
            class_name = card.find_element(By.TAG_NAME, "h3").text
            print(f"  ✓ Verified: {class_name}")
            verified_count += 1
    except NoSuchElementException:
        # Skip if no "When:" text found (not a booking card)
        pass

# Simple comparison
print(f"\n--- VERIFICATION RESULT ---")
print(f"Expected: {total_booked} bookings")
print(f"Found: {verified_count} bookings")

if total_booked == verified_count:
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: Missing {total_booked - verified_count} bookings")
