import os
from toolhouse import Toolhouse
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set API Keys
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
th = Toolhouse(api_key=os.environ.get('TOOLHOUSE_API_KEY'), provider="openai")
th.set_metadata('id', 'Zuhaib')

# Define the OpenAI model to use
MODEL = 'gpt-4o-mini'

# URLs of the SF Bay events pages on Gary's Guide and Lu.ma
garys_guide_url = "https://www.garysguide.com/events?region=sfbay"
luma_url = "https://lu.ma/sf"

print("Welcome to the Gen AI Tech Events Finder!\n")

# Get the date range from user input
start_date = datetime.strptime(input("Enter the start date (MM-DD-YY): "), '%m-%d-%y').date()
end_date = datetime.strptime(input("Enter the end date (MM-DD-YY): "), '%m-%d-%y').date()

# Initialize a list for filtered events
parsed_events = []

# Parse events from Gary's Guide
response = requests.get(garys_guide_url)
soup = BeautifulSoup(response.text, 'html.parser')

for event in soup.find_all('font', class_='ftitle'):
    title = event.find('a').text.strip()
    link = event.find('a')['href']
    
    # Fetch the event page and parse the date
    event_response = requests.get(link)
    event_soup = BeautifulSoup(event_response.text, 'html.parser')
    
    try:
        date_text = event_soup.find('i', class_='far fa-calendar-alt fa-lg').next_sibling.strip()
        event_date = datetime.strptime(date_text, '%a, %b %d, %Y @ %I:%M %p').date()
        
        # Check if the event date is within the specified range
        if start_date <= event_date <= end_date:
            parsed_events.append({
                "title": title,
                "date": date_text,
                "link": link
            })
            print(f"Gary's Guide Event Added: Title: {title}, Date: {date_text}, Link: {link}")  # Debug print statement

    except (AttributeError, ValueError):
        continue  # Skip if date extraction fails

# Parse events from Lu.ma
def parse_luma_events(start_date, end_date):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(luma_url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    unique_identifiers = [link['href'].split('/')[-1] for link in soup.select('a.event-link.content-link')]
    driver.quit()
    
    events = []
    for uid in unique_identifiers[:5]:  # Limit to 5 events
        link = f"https://lu.ma/{uid}"
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(link)
        time.sleep(5)
        event_soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        date_element = event_soup.find('div', class_='jsx-2370077516 title text-ellipses')
        time_element = event_soup.find('div', class_='jsx-2370077516 desc text-ellipses')
        
        if date_element and time_element:
            date_text = date_element.get_text(strip=True)
            time_text = time_element.get_text(strip=True).split('-')[0]
            try:
                # Include time in the date format
                event_date_time = f"{date_text}, 2024 at {time_text}"
                event_datetime = datetime.strptime(event_date_time, '%A, %B %d, %Y at %I:%M %p').date()
                
                if start_date <= event_datetime <= end_date:
                    title_element = event_soup.find('h1')
                    title = title_element.text.strip() if title_element else "Unnamed Event"
                    events.append({
                        "title": title,
                        "date": event_date_time,
                        "link": link
                    })
                    print(f"Lu.ma Event Added: Title: {title}, Date: {event_date_time}, Link: {link}")  # Debug print statement
            except ValueError:
                continue
        driver.quit()
    return events

# Fetch and add Lu.ma events
parsed_events.extend(parse_luma_events(start_date, end_date))

# Print the filtered events
print("\nEvents matching date range:\n")
if parsed_events:
    for event in parsed_events:
        print(f"Event: {event['title']}")
        print(f"Date: {event['date']}")
        print(f"Link: {event['link']}\n")
else:
    print("No events found within the specified date range.")

print("Using OpenAI API to rank by relevancy to Toolhouse\n")

# Request ranking from OpenAI API via Toolhouse
messages = [{
    "role": "user",
    "content":
        f"Rank these events in order of relevance to Toolhouse AI customer acquisition:\n{parsed_events}\n"
        "Provide the order based on relevance, along with rationale."
}]

# Sends the message to the API and gets the response.
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=th.get_tools(),
)
messages += th.run_tools(response)
ranked_response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=th.get_tools(),
)

# Extract and print the ranked events
ranked_events = ranked_response.choices[0].message.content
print("Ranked Events:\n", ranked_events)

# Request a text table with the top 10 ranked events
messages = [{
    "role": "user",
    "content":
        f"Create a simple text table with the top 10 ranked events.\n{ranked_events}\n"
        "Include Title, Date, Link, and rationale as columns."
        "Email me the table to zuhaib.mohiuddin@gmail.com"
}]

# Sends the message to the API and gets the response.
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=th.get_tools(),
)
messages += th.run_tools(response)

# Print the final response for confirmation
print(response.choices[0].message.content)
