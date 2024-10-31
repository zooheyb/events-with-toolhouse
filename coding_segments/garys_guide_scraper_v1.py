from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from dataclasses import dataclass
from typing import List
import time
import logging

@dataclass
class Event:
    """Data class to store event information"""
    title: str
    date: str
    description: str
    url: str

class GarysGuideScraper:
    def __init__(self, headless: bool = False):
        self.setup_logger()
        self.logger.info("Initializing scraper...")
        
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument('--headless=new')
        
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--window-size=1920,1080')
        
    def setup_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def start_browser(self):
        try:
            self.logger.info("Starting Chrome browser...")
            self.driver = webdriver.Chrome(options=self.options)
            self.wait = WebDriverWait(self.driver, 10)
            self.logger.info("Browser started successfully")
        except Exception as e:
            self.logger.error(f"Error starting browser: {str(e)}")
            raise

    def close_browser(self):
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
                self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing browser: {str(e)}")

    def scrape_events(self, url: str) -> List[Event]:
        events = []
        self.start_browser()
        
        try:
            self.logger.info(f"Navigating to {url}")
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Find all event containers
            event_containers = self.driver.find_elements(By.CSS_SELECTOR, "div.items > div")
            self.logger.info(f"Found {len(event_containers)} potential events")
            
            for container in event_containers:
                try:
                    # Get the link element if it exists
                    link_element = container.find_element(By.TAG_NAME, "a")
                    
                    # Extract event details
                    title = link_element.text.strip()
                    url = link_element.get_attribute("href")
                    
                    # Skip empty titles or non-event entries
                    if not title or title.startswith("{"):
                        continue
                    
                    # Get text content
                    full_text = container.text
                    
                    # Split the text to separate date and description
                    text_parts = full_text.split("\n", 1)
                    date = text_parts[0].strip()
                    description = text_parts[1].strip() if len(text_parts) > 1 else ""
                    
                    # Create event object
                    event = Event(
                        title=title,
                        date=date,
                        description=description,
                        url=url
                    )
                    
                    events.append(event)
                    self.logger.info(f"Scraped event: {title[:50]}...")
                    
                except Exception as e:
                    self.logger.error(f"Error processing event: {str(e)}")
                    continue
            
            self.logger.info(f"Successfully scraped {len(events)} events")
            return events
            
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")
            return []
            
        finally:
            self.close_browser()

if __name__ == "__main__":
    try:
        print("Starting scraper...")
        scraper = GarysGuideScraper(headless=False)
        
        print("\nScraping events...")
        events = scraper.scrape_events("https://www.garysguide.com/events?region=sfbay")
        
        print(f"\nFound {len(events)} events:")
        print("-" * 80)
        
        for event in events:
            print(f"\nTitle: {event.title}")
            print(f"Date: {event.date}")
            print(f"URL: {event.url}")
            print(f"Description: {event.description[:200]}...")  # First 200 chars
            print("-" * 80)
        
        input("\nPress Enter to exit...")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        input("\nPress Enter to exit...")