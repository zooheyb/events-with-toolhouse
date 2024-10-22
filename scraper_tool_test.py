from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL of the website
url = "https://lu.ma/sf?utm_source=dp_email"

# Open the website
driver.get(url)

# Wait for the event elements to load (adjust the class name based on inspection)
try:
    # Wait until the events are loaded (you may need to adjust the class name)
    event_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "event-link content-link"))
    )
except Exception as e:
    print("Error waiting for events:", e)
    driver.quit()
    exit()

# Check if events were found
if not event_elements:
    print("No events found. Please check the class name or page structure.")
    driver.quit()
    exit()

# Get the next 5 events (or fewer if there are less than 5)
events = []
for event in event_elements[:5]:
    event_title = event.text.strip()
    events.append(event_title)

# Output the results
if events:
    print("Next 5 events:")
    for i, event in enumerate(events, 1):
        print(f"{i}. {event}")
else:
    print("No events to display.")

# Close the browser
driver.quit()