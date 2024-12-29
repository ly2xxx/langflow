from bs4 import BeautifulSoup
from typing import Optional
import time
import random 
from pathlib import Path
from langflow.load import run_flow_from_json
TWEAKS = {
  "ChatInput-eU8kJ": {},
  "URL-ngSFm": {},
  "ChatOutput-dNxBs": {}
}
 
def run_web_flow(scrape_url):
	# Get current file's directory
	current_dir = Path(__file__).parent

	# Construct path to json relative to current file
	flow_path = current_dir / "web-scrape-flow.json"

	# Convert to string if needed
	flow_path_str = str(flow_path)
	raw_result = run_flow_from_json(flow=flow_path_str,#"D:\code\langflow\SampleFlows\WebAgent\web-scrape-flow.json",
                            input_value=scrape_url,
                            session_id="", # provide a session id if you want to use session state
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)
	
	print("Type of data:", type(raw_result))

	result = raw_result[0].outputs[0].results['message'].data['text']

	return result

    
def _get_used_price(soup: BeautifulSoup) -> Optional[str]:
    """Extract used item price."""
    used_section = soup.find('div', id='usedBuySection')
    if not used_section:
        return None
        
    price_elem = used_section.find('span', 
        class_='a-size-base a-color-price offer-price a-text-normal')
    return price_elem.text.strip() if price_elem else None

def _get_new_price(soup: BeautifulSoup) -> Optional[str]:
    """Extract new item price."""
    price_elem = soup.find("span", class_="a-price")
    if not price_elem:
        return None
        
    price_text = price_elem.find("span", class_="a-offscreen")
    return price_text.get_text().strip() if price_text else None

def get_product_html(url):
	print(url)
	product_html = run_web_flow(url)
	soup = BeautifulSoup(product_html, "html.parser")
	return soup


def extract_product_info(soup):
    products = []
    product_divs = soup.find_all("div", attrs={"data-cy": "title-recipe"})
    
    for div in product_divs:
        product = {}
        
        # Extract brand name
        brand_element = div.find("span", class_="a-size-medium a-color-base")
        if brand_element:
            product['brand'] = brand_element.get_text(strip=True)
        
        # Extract full product title
        title_element = div.find("h2", class_=["a-size-medium a-spacing-none a-color-base a-text-normal", 
                                     "a-size-base-plus a-spacing-none a-color-base a-text-normal"])
        if title_element:
            product['title'] = title_element.find("span").get_text(strip=True)

        # Extract product URL
        link = div.find("a", class_=["a-link-normal s-line-clamp-2 s-link-style a-text-normal","a-link-normal s-line-clamp-4 s-link-style a-text-normal"])
        if link:
            product['href'] = link.get('href')
        
        # Extract rating
        rating_element = div.find_next("span", class_="a-icon-alt")
        if rating_element:
            product['rating'] = rating_element.get_text(strip=True)
        
        # Extract reviews count
        reviews_element = div.find_next("span", class_="a-size-base s-underline-text")
        if reviews_element:
            product['reviews'] = reviews_element.get_text(strip=True)
        
        # Extract popularity/bought count
        popularity_element = div.find_next("span", class_="a-size-base a-color-secondary")
        if popularity_element:
            product['popularity'] = popularity_element.get_text(strip=True)
        
        if product.get('title'):
            products.append(product)
    
    return products

def process_product_prices(new_url, used_url):
	#"""Process product prices and calculate discount."""        
    # Get prices and calculate discount
    new_price = _get_new_price(get_product_html(new_url))
    print(f"New price = {new_price}")
    
    used_price = _get_used_price(get_product_html(used_url))
    print(f"Used price = {used_price}")
    
    try:
        discount = float(used_price[1:]) / float(new_price.split()[0][1:])
    except Exception as e:
        discount = 1.8
        
    print("Price discount =", discount)
    if discount < 0.6:
        print("BARGAIN!!!")

    return discount


if __name__ == '__main__':

	#https://www.octoparse.com/blog/how-to-scrape-amazon-data-using-python
	#c:/code/py_playground/.venv/Scripts/python.exe c:/code/py_playground/crawlamazonwarehouse.py >> results\golf.txt
	#.venv/Scripts/python.exe SampleFlows\WebAgent\crawlamazonwarehouse.py >> laptop.txt
	#https://www.zenrows.com/blog/stealth-web-scraping-in-python-avoid-blocking-like-a-ninja#full-set-of-headers
    #python SampleFlows\WebAgent\crawlamazonwarehouse.py >> golf.txt

	domain_url = "https://www.amazon.co.uk"
	# base_url = "https://www.amazon.co.uk/s?k=ddr4+ram+32gb&i=warehouse-deals&page="
	base_url = "https://www.amazon.co.uk/s?k=nvidia+laptop&i=warehouse-deals&page="
	for page_number in range(1, 2):
		time.sleep(2)
		# Create the new URL by replacing the page number
		page_url = base_url + str(page_number)
		print(page_url)

		# doctype_html = run_web_flow(page_url)
		soup2 = get_product_html(page_url) #BeautifulSoup(doctype_html, "html.parser")
		
		products = extract_product_info(soup2)

		if len(products)==0:
			print("===THE END===")
			break
		for product in products:
			print (product.get("title"))

			try:
				href = product.get("href")
				parts = href.split('/')
				new_url = domain_url+"/dp/"+parts[3]
				used_url = domain_url+"/"+href
			except Exception as e:
				continue

			discount = process_product_prices(new_url, used_url)
			if (discount < 0.6):
				print("BARGAIN!!!")
				print(product.get("rating"))
				print(product.get("reviews"))
				print(product.get("popularity"))
            	
			time.sleep(1)
			print()
			print()
			print()
			print()

