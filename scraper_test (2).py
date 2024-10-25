from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dataclasses import dataclass
from typing import List, Optional
import time
import logging

@dataclass
class ScrapedContent:
    """Data class to store scraped content"""
    title: str
    text: str
    url: str
    timestamp: str

class DynamicScraper:
    def __init__(self, headless: bool = True):
        """
        Initialize the scraper with Chrome WebDriver
        
        Args:
            headless (bool): Whether to run browser in headless mode
        """
        self.logger = self._setup_logger()
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def start_browser(self):
        """Initialize and start the browser"""
        try:
            self.driver = webdriver.Chrome(options=self.options)
            self.wait = WebDriverWait(self.driver, 10)
            self.logger.info("Browser started successfully")
        except Exception as e:
            self.logger.error(f"Failed to start browser: {str(e)}")
            raise

    def close_browser(self):
        """Close the browser and clean up"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            self.logger.info("Browser closed successfully")

    def wait_for_element(self, selector: str, by: By = By.CSS_SELECTOR) -> Optional[object]:
        """
        Wait for an element to be present on the page
        
        Args:
            selector (str): Element selector
            by (By): Type of selector to use
            
        Returns:
            Optional[object]: The web element if found, None otherwise
        """
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, selector))
            )
            return element
        except TimeoutException:
            self.logger.warning(f"Element {selector} not found after waiting")
            return None

    def scrape_page(self, url: str, content_selector: str, 
                    title_selector: str, 
                    timestamp_selector: str = None) -> Optional[ScrapedContent]:
        """
        Scrape content from a single page
        
        Args:
            url (str): URL to scrape
            content_selector (str): CSS selector for main content
            title_selector (str): CSS selector for title
            timestamp_selector (str): CSS selector for timestamp (optional)
            
        Returns:
            Optional[ScrapedContent]: Scraped content or None if failed
        """
        try:
            self.driver.get(url)
            
            # Wait for main content to load
            content_element = self.wait_for_element(content_selector)
            title_element = self.wait_for_element(title_selector)
            
            if not content_element or not title_element:
                self.logger.error(f"Required elements not found for {url}")
                return None
            
            # Get timestamp if selector provided
            timestamp = ""
            if timestamp_selector:
                timestamp_element = self.wait_for_element(timestamp_selector)
                if timestamp_element:
                    timestamp = timestamp_element.text
            
            return ScrapedContent(
                title=title_element.text,
                text=content_element.text,
                url=url,
                timestamp=timestamp
            )
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return None

    def scrape_multiple_pages(self, urls: List[str], content_selector: str, 
                            title_selector: str, 
                            timestamp_selector: str = None) -> List[ScrapedContent]:
        """
        Scrape content from multiple pages
        
        Args:
            urls (List[str]): List of URLs to scrape
            content_selector (str): CSS selector for main content
            title_selector (str): CSS selector for title
            timestamp_selector (str): CSS selector for timestamp (optional)
            
        Returns:
            List[ScrapedContent]: List of scraped content
        """
        results = []
        self.start_browser()
        
        try:
            for url in urls:
                self.logger.info(f"Scraping {url}")
                result = self.scrape_page(url, content_selector, 
                                        title_selector, timestamp_selector)
                if result:
                    results.append(result)
                time.sleep(1)  # Be nice to the server
                
        finally:
            self.close_browser()
            
        return results

# Example usage
if __name__ == "__main__":
    # Example selectors for a blog website
    urls = [
        'https://www.garysguide.com/events?region=sfbay'  
    ]
    
    scraper = DynamicScraper(headless=True)
    results = scraper.scrape_multiple_pages(
        urls=urls,
        content_selector="article.content",
        title_selector="h1.title",
        timestamp_selector="time.published"
    )
    
    for result in results:
        print(f"Title: {result.title}")
        print(f"Content length: {len(result.text)} characters")
        print(f"URL: {result.url}")
        print(f"Timestamp: {result.timestamp}")
        print("-" * 50)