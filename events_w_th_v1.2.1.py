import os
from toolhouse import Toolhouse
from groq import Groq
import requests
from bs4 import BeautifulSoup

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
MODEL = "llama3-groq-70b-8192-tool-use-preview"

# The URL of the SF Bay events page on Gary's Guide
url = "https://www.garysguide.com/events?region=sfbay"

# Ask the user how many events to scrape
num_events = int(input("Starting with Gary's Guide, how many events would you like to scrape? "))

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

# Instantiates the Toolhouse class & creates a message.
th = Toolhouse()
th.set_metadata('id', 'Zuhaib')

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

messages = [{
    "role": "user",
    "content":
         #"Write the code for a table with all events with the columns Title, Date, Link"
        f"Rank these events in order of most applicable to Toolhouse AI customer acquisition \n{parsed_events}\n"
        "Show me the order based on relevancy"
        #"Use the code interpeter tool to create a csv with the events"
        "Use the send email tool to email me a csv of the events to zuhaib.mohiuddin@gmail.com"
        #"Store these events in memeory in their exact format" 
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
tool_run = th.run_tools(response)
messages.extend(tool_run)

response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  tools=th.get_tools(),
)

print(response.choices[0].message.content)

'''
messages = [{
    "role": "user",
    "content":
        "Tell me which events you see"
        f"Use the code interpeter tool to create a csv with \n{parsed_events}\n"
        "Use the send email tool to email me the csv to zuhaib.mohiuddin@gmail.com"
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
tool_run = th.run_tools(response)
messages.extend(tool_run)

response = client.chat.completions.create(
  model=MODEL,
  messages=messages,
  tools=th.get_tools(),
)

print(response.choices[0].message.content)
'''