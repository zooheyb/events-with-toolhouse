import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def parse_luma(start_date, end_date):
    lu_ma_url = "https://lu.ma/sf"
    events = []
    
    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(lu_ma_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the main page. Status code: {response.status_code}")
        return events

    soup = BeautifulSoup(response.text, 'html.parser')
    event_cards = soup.find_all('div', class_='jsx-3881972913 jsx-1809949297 content-card hoverable actionable')
    
    unique_identifiers = []
    max_attempts = 10
    attempts = 0
    
    for event_card in event_cards:
        if attempts >= max_attempts:
            break
        link_element = event_card.find('a', class_='event-link content-link')
        if link_element:
            href_value = link_element['href']
            unique_identifier = href_value.split('/')[-1]
            unique_identifiers.append(unique_identifier)
            attempts += 1
        else:
            print("Warning: Event link not found.")

    base_url = "https://lu.ma/"
    full_links = [base_url + uid for uid in unique_identifiers]

    for link in full_links:
        print(f"\nInspecting event page at: {link}")
        retry_attempts = 3
        
        for attempt in range(retry_attempts):
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                break
            print(f"Failed to fetch event page. Status code: {response.status_code}. Retrying...")
            time.sleep(1)  # Add a small delay between retries
        
        if response.status_code != 200:
            print(f"Skipping {link} due to errors.")
            continue

        event_soup = BeautifulSoup(response.text, 'html.parser')
        
        # Debug: Print out all div elements with class containing 'calendar'
        calendar_divs = event_soup.find_all('div', class_=lambda x: x and 'calendar' in x.lower())
        print("\nFound calendar-related divs:")
        for div in calendar_divs:
            print(f"Class: {div.get('class')}")
            print(f"Content: {div.text}")
            
        # Debug: Print out potential date-related elements
        print("\nLooking for date elements:")
        for div in event_soup.find_all('div'):
            if div.text and any(month in div.text for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                print(f"Potential date element found:")
                print(f"Class: {div.get('class')}")
                print(f"Content: {div.text}")
                print(f"Parent class: {div.parent.get('class')}")
                
        # Debug: Print title elements
        print("\nLooking for title:")
        title_elements = event_soup.find_all(['h1', 'h2', 'h3'])
        for elem in title_elements:
            print(f"Title element class: {elem.get('class')}")
            print(f"Content: {elem.text.strip()}")
            
        print("\n" + "="*50)  # Separator for readability
        
        # Add a small delay between requests to avoid rate limiting
        time.sleep(1)

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