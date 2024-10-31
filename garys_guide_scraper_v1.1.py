import requests
from bs4 import BeautifulSoup

# The URL of the SF Bay events page on Gary's Guide
url = "https://www.garysguide.com/events?region=sfbay"

# Ask the user how many events to scrape
num_events = int(input("Starting with Gary's Guide, how many events would you like to scrape? "))

# Make a request to fetch the page content
response = requests.get(url)

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the list of events and limit to the specified number
events = soup.find_all('font', class_='ftitle')[:num_events]  # Slicing to get the specified number of events

#for event in events:
#    print(event)

# Loop through the events and extract relevant details
for event in events:
    #Event Title
    title = event.find('a').text.strip()
    #print (title)
  
    # Event Link
    link = event.find('a')['href']
    #print (link)
    
    # Make a request to the event page
    event_response = requests.get(link)
    event_soup = BeautifulSoup(event_response.text, 'html.parser')
    
    # Extract the date text from the next sibling of the calendar icon
    date = event_soup.find('i', class_='far fa-calendar-alt fa-lg').next_sibling.strip()
    #print("Event Date:", date)
    
    '''
    # Full link (in case it's a relative URL)
    full_link = f"https://www.garysguide.com{link}"
    '''
    # Output the event details
    print(f"Event: {title}")
    print(f"Date: {date}")
    print(f"Link: {link}\n")