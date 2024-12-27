from bs4 import BeautifulSoup
import requests
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

user_agents = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
] 

# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})

		# Inner NavigableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value.strip()

		# # Printing types of values for efficient understanding
		# print(type(title))
		# print(type(title_value))
		# print(type(title_string))
		# print()

	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Product Price
def get_price(soup):

	try:
		price = soup.find("span", attrs={'class':'aok-offscreen'}).string.strip()

	except AttributeError:
		price = ""	

	return price

# # Function to extract Product Price
# def get_discount_ratio(soup):

# 	try:
# 		new_price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()
# 		print("New = ", new_price)
# 		# prices = soup.select('span."a-price aok-align-center centralizedApexPricePriceToPayMargin" span.a-offscreen')
# 		prices = soup.find("span", attrs={'class':'a-price aok-align-center centralizedApexPricePriceToPayMargin'})
# 		used_price = prices[0].get_text().strip()
# 		# used_price = soup.find("div",attrs={'data-csa-c-buying-option-type':'USED'}).string.strip()
# 		print("Used = ", used_price)
# 		price = float(used_price[1:]) / float(new_price[1:])
# 		if (price < 0.6):
# 			print("BARGAIN!!!")
# 	except AttributeError:
# 		price = ""	

# 	return price

# # Function to extract Product Rating
# def get_rating(soup):

# 	try:
# 		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
# 	except AttributeError:
		
# 		try:
# 			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
# 		except:
# 			rating = ""	

# 	return rating

# # Function to extract Number of User Reviews
# def get_review_count(soup):
# 	try:
# 		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
# 	except AttributeError:
# 		review_count = ""	

# 	return review_count

# # Function to extract Availability Status
# def get_availability(soup):
# 	try:
# 		available = soup.find("div", attrs={'id':'availability'})
# 		available = available.find("span").string.strip()

# 	except AttributeError:
# 		available = ""	

# 	return available	

def get_product_price(url):
	print(url)
	product_html = run_web_flow(url)
	soup = BeautifulSoup(product_html, "html.parser")
	price = get_price(soup)
	return price

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


if __name__ == '__main__':

	#https://www.octoparse.com/blog/how-to-scrape-amazon-data-using-python
	#c:/code/py_playground/.venv/Scripts/python.exe c:/code/py_playground/crawlamazonwarehouse.py >> results\golf.txt
	#.venv/Scripts/python.exe SampleFlows\WebAgent\crawlamazonwarehouse.py >> golf.txt
	#https://www.zenrows.com/blog/stealth-web-scraping-in-python-avoid-blocking-like-a-ninja#full-set-of-headers
	headers2 = {
	"User-Agent": random.choice(user_agents)}
	domain_url = "https://www.amazon.co.uk"
	# base_url = "https://www.amazon.co.uk/s?k=ddr4+ram+32gb&i=warehouse-deals&page="
	base_url = "https://www.amazon.co.uk/s?k=golf&i=warehouse-deals&page="
	for page_number in range(3, 4):
		time.sleep(2)
		# Create the new URL by replacing the page number
		page_url = base_url + str(page_number)
		print(page_url)

		doctype_html = run_web_flow(page_url)
		soup2 = BeautifulSoup(doctype_html, "html.parser")
		
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

			new_price = get_product_price(new_url)
			print(f"New price = {new_price}")
			used_price = get_product_price(used_url)
			print(f"Used price = {used_price}")
			try:
				discount = float(used_price[1:]) / float(new_price.split()[0][1:])#deal with "£14.99 with 39 percent savings"
			except Exception as e:
				discount = 1.8
			print("Price discount =", discount)
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