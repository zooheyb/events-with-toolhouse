import os
import time
import requests
from toolhouse import Toolhouse
from openai import OpenAI
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set API Keys
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
th = Toolhouse(api_key=os.environ.get('TOOLHOUSE_API_KEY'), provider="openai")
th.set_metadata('id', 'Zuhaib')

MODEL = 'gpt-4o-mini'

def parse_garys_guide_events(start_date, end_date, parsed_events):
    # Parse events from Gary's Guide within the date range
    response = requests.get("https://www.garysguide.com/events?region=sfbay")
    soup = BeautifulSoup(response.text, 'html.parser')

    for event in soup.find_all('font', class_='ftitle'):
        title = event.find('a').text.strip()
        link = event.find('a')['href']
        event_response = requests.get(link)
        event_soup = BeautifulSoup(event_response.text, 'html.parser')

        try:
            date_text = event_soup.find('i', class_='far fa-calendar-alt fa-lg').next_sibling.strip()
            event_datetime = datetime.strptime(date_text, '%a, %b %d, %Y @ %I:%M %p')
            if start_date <= event_datetime.date() <= end_date:
                parsed_events.append({
                    "title": title,
                    "date": event_datetime.strftime('%m-%d-%y'),
                    "time": event_datetime.strftime('%I:%M %p'),
                    "link": link
                })
                print(f"Gary's Guide event added: {title}")
        except (AttributeError, ValueError):
            continue

def parse_event_date(date_text, start_date, end_date):
    # Parse the event date string and return a properly formatted year based on the date range.
    try:
        event_date_str = f"{date_text}, {end_date.year}"
        event_date = datetime.strptime(event_date_str, '%A, %B %d, %Y').date()
        if start_date.year != end_date.year and event_date < datetime(end_date.year, 1, 1).date():
            event_date = event_date.replace(year=start_date.year)
        return event_date
    except ValueError:
        print(f"Error parsing date: {date_text}")
        return None

def fetch_event_links(soup):
    # Fetch unique event links from the main Lu.ma page
    base_url = "https://lu.ma/"
    return [base_url + card.find('a', class_='event-link content-link')['href'].split('/')[-1]
            for card in soup.find_all('div', class_='jsx-3881972913 jsx-1809949297 content-card hoverable actionable')]

def parse_luma_events(start_date, end_date, parsed_events):
    # Parse events from Lu.ma within the date range and add them to parsed_events
    lu_ma_url = "https://lu.ma/sf"
    seen_titles = {event["title"] for event in parsed_events}

    # Set up Chrome WebDriver with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    driver.get(lu_ma_url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    full_links = fetch_event_links(soup)

    # Parse through the known event elements
    for link in full_links:
        driver.get(link)
        time.sleep(5)

        event_soup = BeautifulSoup(driver.page_source, 'html.parser')
        date_element = event_soup.find('div', class_='jsx-2370077516 title text-ellipses')
        time_element = event_soup.find('div', class_='jsx-2370077516 desc text-ellipses')

        if date_element and time_element:
            date_text = date_element.get_text(strip=True)
            time_text = time_element.get_text(strip=True).split('-')[0]
            
            event_date = parse_event_date(date_text, start_date, end_date)
            if event_date and start_date <= event_date <= end_date:
                event_title = event_soup.find('h1').text.strip()
                if event_title not in seen_titles:
                    seen_titles.add(event_title)
                    parsed_events.append({
                        "title": event_title,
                        "date": event_date.strftime('%m-%d-%y'),
                        "time": time_text,
                        "link": link
                    })
                    print(f"Lu.ma event added: {event_title}")
            else:
                break
    driver.quit()
    return parsed_events

def main():
    print("Welcome to Zuhaib's Gen AI Tech Event Finder!\n")
    start_date = datetime.strptime(input("Enter start date (MM-DD-YY): "), '%m-%d-%y').date()
    end_date = datetime.strptime(input("Enter end date (MM-DD-YY): "), '%m-%d-%y').date()
    print("\n")
    parsed_events = []

    parse_garys_guide_events(start_date, end_date, parsed_events)
    parse_luma_events(start_date, end_date, parsed_events)

    print(f"\nTotal events found: {len(parsed_events)} \n")
    for event in parsed_events:
        print(f"Title: {event['title']}, Date: {event['date']}, Time: {event.get('time', 'N/A')}")
    print("\nUsing OpenAI API to Rank these events by order of helpfulness to Toolhouse AI\n")

    messages = [{
        "role": "user",
        "content": "Toolhouse AI is a platform that helps developers leverage AI models into their software development." 
                   "We need to identify events that are relevant to our target audience for customer acquisition."
                   f"Rank all \n{len(parsed_events)}\n of these events in order of relevance to Toolhouse AI customer acquisition:\n{parsed_events}\n."
                   "Provide the order of all events based on relevance, with rationale."
    }]
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=th.get_tools())
    messages += th.run_tools(response)
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=th.get_tools())
    ranked_events = response.choices[0].message.content
    print("Ranked Events:\n", ranked_events,"\n")

    top_events_choice = int(input("\nEnter the number of ranked events to be sent to email: "))

    messages = [{
        "role": "user",
        "content": f"Create a text table with the top \n{top_events_choice}\n ranked events:\n{ranked_events}\n"
                   "Include Title, Date, Link, and Rationale. Email it to zuhaib.mohiuddin@gmail.com."
                   "Subject: Top Events for Toolhouse AI Customer Acquisition + the date range."
                   "Confirm email sent."
    }]
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=th.get_tools())
    messages += th.run_tools(response)
    response = client.chat.completions.create(model=MODEL, messages=messages, tools=th.get_tools())
    
    print("\n",response.choices[0].message.content,"\n")

if __name__ == "__main__":
    main()