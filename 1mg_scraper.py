import random
import time
from copy import deepcopy
import cloudscraper
import pandas as pd 
import os 


class Crawler:
    def __init__(self):
        # Base URL for 1mg website (not used directly in requests)
        self.base_url = 'https://www.1mg.com/drugs-all-medicines?label=A'
        
        # Headers to mimic a browser request and avoid bot detection
        self.get_headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }
        self.session = cloudscraper.create_scraper()  # Persistent session for making requests

        # Template object structure to store extracted data
        self.obj = {
            "name": "", "manufacturer_name": "", "marketer_name": "", "type": "", 
            "price": "", "sku_id": "", "available": "", "pack_size_label": "", 
            "quantity": "", "short_composition": "", "url": ""
        }
        self.all_data = []  # List to store all extracted product data

    # Function to handle GET requests with retries on failure
    def get_request(self, url):
        mycount = 0  # Counter to limit the number of retries
        while True:
            try:
                # Make a GET request with the specified headers
                res = self.session.get(url, headers=self.get_headers)
                print(res)
                # If request is successful, return True with the response
                if res.status_code == 200:
                    return True, res
                # Sleep for a random interval between retries
                time.sleep(random.randint(1, 3))
            except Exception as e:
                print(e)  # Print the exception if any error occurs during the request
            self.session = cloudscraper.create_scraper()  # Create a new scraper instance after failure
            print("Trying again to fetch data")
            mycount += 1
            
            # Exit loop after 30 failed attempts
            if mycount > 30:
                break
        return False, False  # Return False if all retries fail

    # Function to extract details of each product from the received JSON data
    def get_details(self, data):
        extracted_data = []  # Store the data for the current page
        for item in data:
            # Create a copy of the object structure for each product
            Obj = deepcopy(self.obj)
            try:
                # Extract and assign relevant product details
                Obj['manufacturer_name'] = item.get('manufacturer_name', '')
                Obj['marketer_name'] = item.get('marketer_name', '')
                Obj['type'] = item.get('type', '')
                Obj['price'] = item.get('price', 0)
                Obj['name'] = item.get('name', '')
                Obj['sku_id'] = item.get('sku_id', '')
                Obj['available'] = item.get('available', False)            
                Obj['pack_size_label'] = item.get('pack_size_label', '') 
                Obj['quantity'] = item.get('quantity', 0)
                Obj['url'] = 'https://www.1mg.com'+item.get('slug', '') 
            except Exception as e:
                print(f"Error processing item {item}: {e}")  # Handle errors during data extraction
            self.all_data.append(Obj)  # Append the extracted data to the list

        return extracted_data  # Return the extracted data for the current page

    # Function to export data to an Excel file page by page and append it
    def export_to_excel_append(self, file_name="scraped_data.xlsx"):
        try:
            df = pd.DataFrame(self.all_data)  # Convert the data into a pandas DataFrame
            
            # Check if file exists
            file_exists = os.path.exists(file_name)
            
            # If the file exists, append data. Otherwise, create a new file.
            with pd.ExcelWriter(file_name, mode='a' if file_exists else 'w', engine='openpyxl') as writer:
                # If file doesn't exist, write data with header; if exists, append data
                df.to_excel(writer, index=False, header=not file_exists)
            
            print(f"Data successfully {'appended to' if file_exists else 'written to'} {file_name}")
            
        except Exception as e:
            print(f"Error appending data to Excel: {e}")
    # Main process that handles logic for fetching product data by pages
    def process_logic(self):
        try:
            page = 1  # Start from page 1
            while True:
                time.sleep(3)  # Sleep between requests to avoid rate limiting
                print("Scraping for page :- ", page)
                
                # API URL to fetch product data based on page number
                url = f'https://www.1mg.com/pharmacy_api_gateway/v4/drug_skus/by_prefix?prefix_term=a&page={str(page)}&per_page=30'
                
                isloaded, res = self.get_request(url)
                if isloaded:
                    data = res.json()  # Parse the JSON response
                    skus = data.get('data', {}).get('skus', [])  # Get the product SKU details
                    if skus and len(skus) > 0:
                        extracted_data = self.get_details(skus)  # Extract product details from the page
                        if page == 100:
                            self.export_to_excel_append(extracted_data)  # Export and append data for each page
                            break
                        page += 1  # Go to the next page if more products exist
                    else:
                        break  # Exit loop if no products found
                else:
                    break  # Exit if unable to fetch data
        except Exception as e:
            print(e)  # Handle unexpected errors during the process

if __name__ == "__main__":
    scraper = Crawler()
    scraper.process_logic()  # Start the scraping process
