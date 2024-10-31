import os
from toolhouse import Toolhouse
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

# Let's set our API Keys.
# Please remember to use a safer system to store your API KEYS 
# after finishing the quick start.
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
th = Toolhouse(api_key=os.environ.get('TOOLHOUSE_API_KEY'),
               provider= "openai")
th.set_metadata('id', 'Zuhaib')


# Define the OpenAI model we want to use
MODEL = 'gpt-4o-mini'

# The URL of the SF Bay events page on Gary's Guide
url = "https://www.garysguide.com/events?region=sfbay"

# Ask the user how many events to scrape
num_events = int(input("Starting with Gary's Guide, how many events would you like to scrape? "))
print ()

# Make a request to fetch the page content
response = requests.get(url)

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the list of events and limit to the specified number
events = soup.find_all('font', class_='ftitle')[:num_events]
parsed_events = []

# Loop through the events and extract relevant details
for event in events:
    # Event Title
    title = event.find('a').text.strip()
  
    # Event Link
    link = event.find('a')['href']
    
    # Make a request to the event page
    event_response = requests.get(link)
    event_soup = BeautifulSoup(event_response.text, 'html.parser')
    
    # Extract the date text from the next sibling of the calendar icon
    date = event_soup.find('i', class_='far fa-calendar-alt fa-lg').next_sibling.strip()
    
     # Store the event details in a dictionary and append it to the list
    parsed_events.append({
        "title": title,
        "date": date,
        "link": link
    })

# Print out the parsed events to verify
for event in parsed_events:
    print(f"Event: {event['title']}")
    print(f"Date: {event['date']}")
    print(f"Link: {event['link']}\n")


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
print("Using OpenAI API to rank by relevancy\n")

messages = [{
    "role": "user",
    "content":
        f"Rank these events in order of most applicable to Toolhouse AI customer acquisition \n{parsed_events}\n"
        "Show me the order based on relevancy"
        "Store these events in memory with Title, Date, Link" 
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

messages = [{
    "role": "user",
    "content":
        "Fetch from memory the Gen AI events in their exact format and list them here"
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
