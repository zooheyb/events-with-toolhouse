import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parse_luma(start_date, end_date):
    lu_ma_url = "https://lu.ma/sf"
    events = []
    
    response = requests.get(lu_ma_url)
    
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
        print(f"Inspecting event page at: {link}")
        retry_attempts = 3
        for attempt in range(retry_attempts):
            response = requests.get(link)
            if response.status_code == 200:
                break
            print(f"Failed to fetch event page. Status code: {response.status_code}. Retrying...")
        
        if response.status_code != 200:
            print(f"Skipping {link} due to errors.")
            continue

        event_soup = BeautifulSoup(response.text, 'html.parser')

        # Attempt to find date and time
        date_element = event_soup.find('div', class_='jsx-2370077516 title text-ellipses')
        time_element = event_soup.find('div', class_='jsx-2370077516 desc text-ellipses')

        if date_element and time_element:
            date_text = date_element.get_text(strip=True)
            time_text = time_element.get_text(strip=True).split('-')[0]  # Get start time

            # Assuming the date is well formatted
            try:
                event_date = datetime.strptime(date_text, '%A, %B %d').date()
            except ValueError as e:
                print(f"Error parsing date: {date_text}. Error: {e}")
                continue

            # Check if the event date is within the specified range
            if start_date <= event_date <= end_date:
                events.append({
                    "title": event_card.find('h3').text.strip(),
                    "date": date_text,
                    "time": time_text,
                    "link": link
                })
                print(f"Event found: Title: {event_card.find('h3').text.strip()}, Link: {link}, Date: {date_text}, Time: {time_text}")
            else:
                print("Event date is out of the specified range.")
        else:
            print("Skipping event as date or time is missing.")

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
