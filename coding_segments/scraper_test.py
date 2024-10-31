from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Chrome options (optional headless mode)
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without opening a window)

# Set up the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the URL
url = 'https://www.garysguide.com/events?region=sfbay'
driver.get(url)

# Wait for the elements to be present on the page before proceeding
try:
    # Wait for up to 10 seconds for the elements to be loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'listing'))
    )
    print("Page loaded, starting scraping...")
except Exception as e:
    print(f"Error while waiting for page to load: {e}")
    driver.quit()

# Once the page is loaded, extract the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find the section that contains the event listings
events = soup.find_all('div', class_='listing')

# If events are found, loop through each and extract details
if events:
    for event in events:
        # Find and print the event title
        title = event.find('a', class_='name').get_text(strip=True)
        # Extract the URL for the event
        link = event.find('a', class_='name')['href']
        # Get the event date if available
        date = event.find('div', class_='date').get_text(strip=True) if event.find('div', class_='date') else 'No date'
        
        print(f'Title: {title}')
        print(f'Date: {date}')
        print(f'Link: {link}')
        print('-' * 40)
else:
    print("No events found on the page.")

# Close the browser when done
driver.quit()

'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Chrome options (optional headless mode)
chrome_options = Options()
chrome_options.add_argument('--headless')  # Uncomment this line if you don't want to open a browser window

# Path to chromedriver (update this path to your chromedriver location)
chrome_driver_path = 'C:/Users/zuhai/.wdm/drivers/chromedriver/win64/129.0.6668.100/chromedriver-win32/chromedriver.exe'

# Set up the webdriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL
url = 'https://www.garysguide.com/events?region=sfbay'
driver.get(url)

# Wait for the elements to be present on the page before proceeding try:
    # Wait for up to 10 seconds for the elements to be loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'listing'))
    )
print("Page loaded, starting scraping...")
except Exception as e:
print(f"Error while waiting for page to load: {e}")
driver.quit()

# Give the page some time to load its dynamic content (adjust as needed)
#time.sleep(5)

# Parse the dynamically loaded content using BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the driver (browser) after loading
driver.quit()

# Find the section that contains the event listings
events = soup.find_all('div', class_='listing')

# Loop through each event and extract details
for event in events:
    # Find and print the event title
    title = event.find('a', class_='name').get_text(strip=True)
    # Extract the URL for the event
    link = event.find('a', class_='name')['href']
    # Get the event date if available
    date = event.find('div', class_='date').get_text(strip=True) if event.find('div', class_='date') else 'No date'
    
    print(f'Title: {title}')
    print(f'Date: {date}')
    print(f'Link: {link}')
    print('-' * 40)
'''