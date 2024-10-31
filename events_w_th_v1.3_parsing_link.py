import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parse_luma(start_date, end_date):
    events = []  # Local variable to store events
    lu_ma_url = "https://lu.ma/sf"
    
    # Fetch the page content
    response = requests.get(lu_ma_url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all event cards
    event_cards = soup.find_all('div', class_='jsx-3881972913 jsx-1809949297 content-card hoverable actionable')

    # Initialize a list to hold unique identifiers
    unique_identifiers = []

    # Limit parsing attempts to 10
    max_attempts = 10
    attempts = 0

    # Loop through each event card and extract titles and links, up to the maximum attempts
    for event_card in event_cards:
        if attempts >= max_attempts:
            break  # Stop if we've reached the maximum attempts

        # Attempt to extract title
        title_element = event_card.find('h3', class_='jsx-3851280986')
        title = title_element.text.strip() if title_element else "Title not found"

        # Attempt to extract link
        link_element = event_card.find('a', class_='event-link content-link')
        if link_element:
            # Extract the href attribute
            href_value = link_element['href']
            # Capture the unique identifier
            unique_identifier = href_value.split('/')[-1]  # Gets the last part after the last '/'
            unique_identifiers.append(unique_identifier)
            full_link = f"https://lu.ma/{unique_identifier}"  # Construct full URL
            
            # Print title and link immediately after parsing
            print(f"Parsed Event Title: {title}, Event Link: {full_link}")
            
            attempts += 1  # Increment attempts
        else:
            print("Warning: Event link not found.")
            continue

    # Process each unique identifier to extract the event date from the main page
    for unique_id in unique_identifiers:
        full_link = f"https://lu.ma/{unique_id}"
        event_response = requests.get(full_link)
        if event_response.status_code != 200:
            print(f"Failed to fetch the event page. Status code: {event_response.status_code}")
            continue
        
        event_soup = BeautifulSoup(event_response.text, 'html.parser')

        # Attempt to extract date and time from the event page
        date_element = event_soup.find('div', class_='jsx-2370077516 title text-ellipses')
        time_element = event_soup.find('div', class_='jsx-2370077516 desc text-ellipses')

        # Debug: Print the raw HTML to troubleshoot
        if date_element:
            print("Raw date element HTML:", date_element)
            date_text = date_element.text.strip()
            if not date_text:
                print("Warning: Date text is empty.")
        else:
            print("Warning: Date element not found.")

        if time_element:
            print("Raw time element HTML:", time_element)
            time_text = time_element.text.strip()
        else:
            print("Warning: Time element not found.")

        # Ensure we have both date and time text before parsing
        if date_text and time_text:
            # Attempt to parse the date
            try:
                # Adjusted format to match what is expected
                event_date = datetime.strptime(date_text, '%A, %B %d').date()  # Example: "Monday, October 28"
                
                # Check if the event date is within the specified range
                if start_date <= event_date <= end_date:
                    events.append({
                        "title": title,
                        "date": date_text,
                        "link": full_link  # Use the full link here
                    })
            except ValueError as e:
                print(f"Error parsing date: '{date_text}' | Error: {e}")
                continue
        else:
            print("Skipping event as date or time is missing.")

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
