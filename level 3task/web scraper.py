import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import argparse
import os
from urllib.parse import urlparse, urljoin

class WebScraper:
    def __init__(self, user_agent=None, delay=1):
        
        self.session = requests.Session()
        
        default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        self.session.headers.update({
            'User-Agent': user_agent if user_agent else default_user_agent
        })
        
        self.delay = delay
    
    def fetch_page(self, url):
        
        try:
            time.sleep(self.delay + random.uniform(0, 1))
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()  
            
            return BeautifulSoup(response.text, 'html.parser')
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_data(self, soup, selectors):
       
        result = {}
        
        for name, selector in selectors.items():
            try:
                elements = soup.select(selector)
                
                if len(elements) == 1:
                    # Single element case
                    result[name] = elements[0].get_text(strip=True)
                elif len(elements) > 1:
                    # Multiple elements case
                    result[name] = [el.get_text(strip=True) for el in elements]
                else:
                    result[name] = None
                    
            except Exception as e:
                print(f"Error extracting {name} with selector {selector}: {e}")
                result[name] = None
        
        return result
    
    def save_to_csv(self, data_list, filename):
       
        if not data_list:
            print("No data to save.")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = data_list[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for data in data_list:
                    writer.writerow(data)
                
            print(f"Data saved to {filename}")
            
        except Exception as e:
            print(f"Error saving data to CSV: {e}")
    
    def extract_links(self, soup, base_url, filter_same_domain=True):
       
        links = []
        base_domain = urlparse(base_url).netloc
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            absolute_url = urljoin(base_url, href)
            
          
            if filter_same_domain:
                link_domain = urlparse(absolute_url).netloc
                if link_domain != base_domain:
                    continue
            
            links.append(absolute_url)
        
        return links
    
    def crawl(self, start_url, selectors, max_pages=10, same_domain=True):
       
        visited_urls = set()
        urls_to_visit = [start_url]
        extracted_data = []
        
        while urls_to_visit and len(visited_urls) < max_pages:
            current_url = urls_to_visit.pop(0)
            
            if current_url in visited_urls:
                continue
            
            print(f"Crawling: {current_url}")
            soup = self.fetch_page(current_url)
            visited_urls.add(current_url)
            
            if not soup:
                continue
            
            
            data = self.extract_data(soup, selectors)
            data['url'] = current_url
            extracted_data.append(data)
            
            
            links = self.extract_links(soup, current_url, same_domain)
            
            
            for link in links:
                if link not in visited_urls and link not in urls_to_visit:
                    urls_to_visit.append(link)
        
        return extracted_data

def main():
    parser = argparse.ArgumentParser(description='Web Scraper Tool')
    parser.add_argument('url', help='Starting URL to scrape')
    parser.add_argument('--output', '-o', default='scraped_data.csv', help='Output CSV file name')
    parser.add_argument('--pages', '-p', type=int, default=5, help='Maximum number of pages to crawl')
    parser.add_argument('--delay', '-d', type=float, default=1.0, help='Delay between requests in seconds')
    
    args = parser.parse_args()
    
    scraper = WebScraper(delay=args.delay)
    
    selectors = {
        'title': 'title',
        'h1_headings': 'h1',
        'h2_headings': 'h2',
        'paragraphs': 'p',
        'links': 'a',
        'images': 'img'
    }
    
    print(f"Starting web scraping from {args.url}")
    data = scraper.crawl(args.url, selectors, max_pages=args.pages)
    
    if data:
        scraper.save_to_csv(data, args.output)
        print(f"Scraped {len(data)} pages. Data saved to {args.output}")
    else:
        print("No data was scraped.")

if __name__ == "__main__":
    main()