import os
from toolhouse import Toolhouse
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
from io import StringIO

# Set API Keys
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
th = Toolhouse(api_key=os.environ.get('TOOLHOUSE_API_KEY'), provider="openai")
th.set_metadata('id', 'Zuhaib')

# Define the OpenAI model to use
MODEL = 'gpt-4o-mini'

# URL of the SF Bay events page on Gary's Guide
url = "https://www.garysguide.com/events?region=sfbay"

print("Welcome to the Gen AI Tech Events Finder!\n")

# Get the date range from user input
start_date = datetime.strptime(input("Enter the start date (MM-DD-YY): "), '%m-%d-%y').date()
end_date = datetime.strptime(input("Enter the end date (MM-DD-YY): "), '%m-%d-%y').date()

# Fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize a list for filtered events
parsed_events = []

# Loop through the events
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
        else:
            break  # Stop parsing if the event date is out of range

    except (AttributeError, ValueError):
        continue  # Skip if date extraction fails

# Print the filtered events
print("\nEvents matching date range:\n")
if parsed_events:
    for event in parsed_events:
        print(f"Event: {event['title']}")
        print(f"Date: {event['date']}")
        print(f"Link: {event['link']}\n")
else:
    print("No events found within the specified date range.")

'''
# Ask the user how many events to search
num_events = int(input("Using Groq, how many events would you like to search? "))
messages = [{
    "role": "user",
        "content": f"Search the internet for the next {num_events} Gen AI tech events in San Francisco after Oct 24, 2024"
        "Print them with their title, date, and link"
   }]
response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  # Passes Code Execution as a tool
  tools=th.get_tools(),
)

# Runs the Code Execution tool, gets the result, 
# and appends it to the context
tool_run = th.run_tools(response)
messages.extend(tool_run)

response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  tools=th.get_tools(),
)

# Extract the content from the response
response_content = response.choices[0].message.content

# Store the response content as a variable
events_info = response_content

print(events_info)
'''

print("Using OpenAI API to rank by relevancy to Toolhouse\n")

messages = [{
    "role": "user",
    "content":
        f"Rank all of these events in order with rationale of most applicable to Toolhouse AI customer acquisition \n{parsed_events}\n"
        "Show me the order based on relevancy"
        #"Make me a simple table of the events with Title, Date, and Link as columns"
        #"Email me the table to zuhaib.mohiuddin@gmail.com"
   }]

# Sends the message to the API and gets the response.
response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  # Passes Code Execution as a tool
  tools=th.get_tools(),
)

# Runs the Code Execution tool, gets the result, 
# and appends it to the context
messages += th.run_tools(response)

response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  tools=th.get_tools(),
)
# Extract the ranked response content
ranked_events = response.choices[0].message.content

# Optionally, you can store the ranked events in a structured format (e.g., list of dicts)
# For example, if the response is a text table, you can parse it into a list of dictionaries.

# Print the ranked events
print("Ranked Events:\n", ranked_events)


messages = [{
    "role": "user",
    "content":
        f"Creat a simple text table with the top 10 \n{ranked_events}\n"
        "Include Title, Date, Link, and rationale as columns for that table"    
        f"Email me the table to zuhaib.mohiuddin@gmail.com"
        #"Resend the email so I have two copies in my inbox"
   }]

# Sends the message to the API and gets the response.
response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  # Passes Code Execution as a tool
  tools=th.get_tools(),
)

# Runs the Code Execution tool, gets the result, 
# and appends it to the context
messages += th.run_tools(response)

response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  tools=th.get_tools(),
)

print(response.choices[0].message.content)