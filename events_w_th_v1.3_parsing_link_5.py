import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def parse_event_date(date_text):
    """Parse the event date string and return a datetime.date object."""
    try:
        # Assume the year to be 2024
        event_date_str = f"{date_text}, 2024"  # Append the assumed year
        return datetime.strptime(event_date_str, '%A, %B %d, %Y').date()
    except ValueError as e:
        print(f"Error parsing date: {date_text}. Error: {e}")
        return None

def fetch_event_links(soup):
    """Fetch event links from the main page soup."""
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

def parse_luma(start_date, end_date):
    lu_ma_url = "https://lu.ma/sf"
    events = []
    seen_events = set()  # To keep track of unique event titles and times

    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(lu_ma_url)
    time.sleep(5)  # Allow page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    full_links = fetch_event_links(soup)

    max_events_to_fetch = 5
    for link in full_links[:max_events_to_fetch]:
        print(f"Inspecting event page at: {link}")
        driver.get(link)
        time.sleep(5)  # Allow page to load

        event_soup = BeautifulSoup(driver.page_source, 'html.parser')
        date_element = event_soup.find('div', class_='jsx-2370077516 title text-ellipses')
        time_element = event_soup.find('div', class_='jsx-2370077516 desc text-ellipses')

        if date_element and time_element:
            date_text = date_element.get_text(strip=True)
            time_text = time_element.get_text(strip=True).split('-')[0]  # Get start time
            print(f"Parsing date: '{date_text}'")  # Debugging statement

            event_date = parse_event_date(date_text)
            if event_date and start_date <= event_date <= end_date:
                formatted_date = event_date.strftime('%m-%d-%y')
                event_title = event_soup.find('h1').text.strip()  # Use the correct selector to fetch title

                # Create a unique identifier for the event using title and time
                unique_event_identifier = (event_title, time_text)

                # Check for uniqueness of the event
                if unique_event_identifier not in seen_events:
                    seen_events.add(unique_event_identifier)  # Add the identifier to the set
                    events.append({
                        "title": event_title,
                        "date": formatted_date,
                        "time": time_text,
                        "link": link
                    })
                    print(f"Event found: Title: {event_title}, Link: {link}, Date: {formatted_date}, Time: {time_text}")
                else:
                    print(f"Duplicate event found: {event_title} at {time_text}, skipping.")
            else:
                print(f"Event date {event_date} is out of the specified range or invalid.")
        else:
            print("Skipping event as date or time is missing.")

    driver.quit()  # Close the browser
    return events

def main():
    start_date_str = input("Enter start date (MM-DD-YY): ")
    end_date_str = input("Enter end date (MM-DD-YY): ")

    start_date = datetime.strptime(start_date_str, '%m-%d-%y').date()
    end_date = datetime.strptime(end_date_str, '%m-%d-%y').date()

    events = parse_luma(start_date, end_date)

    print(f"\nTotal events found: {len(events)}")
    for event in events:
        print(f"Title: {event['title']}, Link: {event['link']}, Date: {event['date']}, Time: {event['time']}")

if __name__ == "__main__":
    main()
