import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests

def parse_event_date(date_text):
    """Parse the event date string and return a datetime.date object."""
    try:
        event_date_str = f"{date_text}, 2024"  # Assume the year is 2024
        return datetime.strptime(event_date_str, '%A, %B %d, %Y').date()
    except ValueError as e:
        print(f"Error parsing date: {date_text}. Error: {e}")
        return None

def fetch_event_links(soup):
    """Fetch event links from the main Lu.ma page soup."""
    event_cards = soup.find_all('div', class_='jsx-3881972913 jsx-1809949297 content-card hoverable actionable')
    unique_identifiers = []

    for event_card in event_cards:
        link_element = event_card.find('a', class_='event-link content-link')
        if link_element:
            href_value = link_element['href']
            unique_identifier = href_value.split('/')[-1]
            unique_identifiers.append(unique_identifier)

    base_url = "https://lu.ma/"
    return [base_url + uid for uid in unique_identifiers]

def parse_luma_events(start_date, end_date, parsed_events):
    """Parse events from Lu.ma within the date range and add them to parsed_events."""
    lu_ma_url = "https://lu.ma/sf"
    seen_events = set()  # Track unique events by title and time

    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(lu_ma_url)
    time.sleep(5)  # Allow page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    full_links = fetch_event_links(soup)

    for link in full_links:
        print(f"Inspecting event page at: {link}")
        driver.get(link)
        time.sleep(5)  # Allow page to load

        event_soup = BeautifulSoup(driver.page_source, 'html.parser')
        date_element = event_soup.find('div', class_='jsx-2370077516 title text-ellipses')
        time_element = event_soup.find('div', class_='jsx-2370077516 desc text-ellipses')

        if date_element and time_element:
            date_text = date_element.get_text(strip=True)
            time_text = time_element.get_text(strip=True).split('-')[0]  # Extract start time
            print(f"Parsing date: '{date_text}'")  # Debug statement

            event_date = parse_event_date(date_text)
            if event_date:
                if event_date < start_date or event_date > end_date:
                    print(f"Event date {event_date} is out of range. Stopping parse for Lu.ma.")
                    break  # Stop parsing if an out-of-range date is encountered

                event_title = event_soup.find('h1').text.strip()  # Fetch event title
                unique_event_identifier = (event_title, time_text)

                if unique_event_identifier not in seen_events:
                    seen_events.add(unique_event_identifier)  # Track event
                    formatted_date = event_date.strftime('%m-%d-%y')
                    parsed_events.append({
                        "title": event_title,
                        "date": formatted_date,
                        "time": time_text,
                        "link": link
                    })
                    print(f"Lu.ma Event added: {event_title} on {formatted_date} at {time_text}")
                else:
                    print(f"Duplicate Lu.ma event found: {event_title} at {time_text}, skipping.")
        else:
            print("Skipping event due to missing date or time.")

    driver.quit()
    return parsed_events  # Return the list of parsed events

def parse_garys_guide_events(start_date, end_date, parsed_events):
    """Parse events from Gary's Guide within the date range and add them to parsed_events."""
    url = "https://www.garysguide.com/events?region=sfbay"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for event in soup.find_all('font', class_='ftitle'):
        title = event.find('a').text.strip()
        link = event.find('a')['href']
        
        # Fetch the event page and parse the date and time
        event_response = requests.get(link)
        event_soup = BeautifulSoup(event_response.text, 'html.parser')
        
        try:
            date_text = event_soup.find('i', class_='far fa-calendar-alt fa-lg').next_sibling.strip()
            # Parse the date and time
            event_datetime = datetime.strptime(date_text, '%a, %b %d, %Y @ %I:%M %p')
            event_date = event_datetime.date()  # Extract just the date part
            
            # Check if the event date is within the specified range
            if start_date <= event_date <= end_date:
                formatted_date = event_date.strftime('%m-%d-%y')
                formatted_time = event_datetime.strftime('%I:%M %p')
                
                # Append event with date and time to parsed_events
                parsed_events.append({
                    "title": title,
                    "date": formatted_date,
                    "time": formatted_time,
                    "link": link
                })
                print(f"Gary's Guide Event added: {title} on {formatted_date} at {formatted_time}")
        except (AttributeError, ValueError):
            continue


def main():
    start_date_str = input("Enter start date (MM-DD-YY): ")
    end_date_str = input("Enter end date (MM-DD-YY): ")

    start_date = datetime.strptime(start_date_str, '%m-%d-%y').date()
    end_date = datetime.strptime(end_date_str, '%m-%d-%y').date()

    # List to hold all parsed events within the date range
    parsed_events = []

    # Parse events from Gary's Guide and Lu.ma
    parse_garys_guide_events(start_date, end_date, parsed_events)
    parse_luma_events(start_date, end_date, parsed_events)

    print(f"\nTotal events found: {len(parsed_events)}")
    for event in parsed_events:
        print(f"Title: {event['title']}, Link: {event['link']}, Date: {event['date']}, Time: {event.get('time', 'N/A')}")
    
if __name__ == "__main__":
    main()