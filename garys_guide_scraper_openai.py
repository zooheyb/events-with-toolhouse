import requests
from bs4 import BeautifulSoup

# The URL of the SF Bay events page on Gary's Guide
url = "https://www.garysguide.com/events?region=sfbay"

# Make a request to fetch the page content
response = requests.get(url)

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the list of events
events = soup.find_all('font', class_='ftitle')

for event in events:
    print (event)


# Loop through the events and extract relevant details
for event in events:
    #Event Title
    title = event.find('a').text.strip()
    '''
   # Event Date
    date = event.find('div', class_='event-date').text.strip()
    
    # Event Link
    link = event.find('a', class_='event-title')['href']
    
    # Full link (in case it's a relative URL)
    full_link = f"https://www.garysguide.com{link}"

    # Output the event details
    print(f"Event: {title}")
    print(f"Date: {date}")
    print(f"Link: {full_link}\n")
    '''