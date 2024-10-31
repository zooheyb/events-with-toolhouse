import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL of the Lu.ma events page
lu_ma_url = "https://lu.ma/sf"

def parse_luma(start_date, end_date):
    events = []  # Local variable to store events
    response = requests.get(lu_ma_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Print to confirm page was fetched
    print("Fetched Lu.ma page content successfully.")

    attempt_count = 0

    for event in soup.find_all('div', class_='jsx-3851280986'):
        if attempt_count >= 10:
            break
        
        attempt_count += 1
        
        # Attempt to extract title
        title_element = event.find('h3')
        if title_element:
            title = title_element.text.strip()
        else:
            print("Warning: Event title not found.")
            continue
        
        # Attempt to extract link using unique identifier
        link_element = event.find('a', class_='event-link content-link')
        if link_element:
            link = link_element.get('href')  # Use get() for safe attribute access
            if link:
                unique_identifier = link.split('/')[-1]  # Extract unique identifier
                full_link = f"https://lu.ma/{unique_identifier}"  # Construct full URL
            else:
                print("Warning: Link element does not have an href attribute.")
                continue
        else:
            print("Warning: Event link not found.")
            continue

        # Print the event title and link
        print(f"Event Title: {title}, Event Link: {full_link}")

        # Now fetch the event page to get date and time
        event_response = requests.get(full_link)
        if event_response.status_code != 200:
            print(f"Failed to fetch the event page. Status code: {event_response.status_code}")
            continue

        event_soup = BeautifulSoup(event_response.text, 'html.parser')

        # Attempt to extract date and time
        date_element = event_soup.find('div', class_='jsx-2370077516 title text-ellipses')
        time_element = event_soup.find('div', class_='jsx-2370077516 desc text-ellipses')

        if date_element and time_element:
            date_text = date_element.text.strip()
            time_text = time_element.text.strip()

            # Debug: Print the raw date and time strings
            print(f"Raw Date String: '{date_text}', Raw Time String: '{time_text}'")

            try:
                # Adjust the date format based on the expected output
                event_date = datetime.strptime(date_text, '%A, %B %d').date()  # Example: "Monday, October 28"
            except ValueError as e:
                print(f"Error parsing date: {date_text} | Error: {e}")
                continue  # Skip if date parsing fails

            # Check if the event date is within the specified range
            if start_date <= event_date <= end_date:
                events.append({
                    "title": title,
                    "date": date_text,
                    "link": full_link  # Use the full link here
                })
                print(f"Event added: {title} - {full_link}")  # Print title and link for the event
            else:
                print("Event date is out of the specified range.")
        else:
            print("Warning: Event date not found.")
    
    print(f"\nTotal events found in date range: {len(events)}")
    return events

def main():
    # Get start and end dates from the user
    start_date_input = input("Enter the start date (MM-DD-YY): ")
    end_date_input = input("Enter the end date (MM-DD-YY): ")

    # Parse the input dates
    try:
        start_date = datetime.strptime(start_date_input, '%m-%d-%y').date()
        end_date = datetime.strptime(end_date_input, '%m-%d-%y').date()
    except ValueError as e:
        print(f"Error parsing date input: {e}")
        return

    # Call the parse function
    events = parse_luma(start_date, end_date)

    # Print the results
    for event in events:
        print(f"Event Title: {event['title']}, Link: {event['link']}")

# Run the main function
if __name__ == "__main__":
    main()
