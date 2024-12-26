from bs4 import BeautifulSoup
import requests
import time
import random 
from langflow.load import run_flow_from_json
TWEAKS = {
  "ChatInput-eU8kJ": {},
  "URL-ngSFm": {},
  "ChatOutput-dNxBs": {}
}
 
def run_web_flow(scrape_url):
	result = run_flow_from_json(flow="D:\code\langflow\SampleFlows\WebAgent\web-scrape-flow.json",
                            input_value=scrape_url,
                            session_id="", # provide a session id if you want to use session state
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)

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
		price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

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

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

# Function to extract Availability Status
def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = ""	

	return available	

def print_product_info(url):
	print(url)
	# Headers for request
	#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
	HEADERS = ( {
	"User-Agent": random.choice(user_agents)})

	# The webpage URL
	# URL = "https://www.amazon.co.uk/dp/B08688GFPD/"

	# HTTP Request
	webpage = requests.get(url, headers=HEADERS)

	# Soup Object containing all data
	# soup = BeautifulSoup(webpage.content, "lxml")
	soup = BeautifulSoup(webpage.content, "html.parser")

	price = get_price(soup)

	# Function calls to display all necessary product information
	print("Product Title =", get_title(soup))
	print("Product Price =", price)
	print("Product Rating =", get_rating(soup))
	print("Number of Product Reviews =", get_review_count(soup))
	print("Availability =", get_availability(soup))
	print()

	return price

def extract_product_info(soup):
    products = []
    product_divs = soup.find_all("div", class_="a-section a-spacing-small puis-padding-left-small puis-padding-right-small")
    
    for div in product_divs:
        product = {}
        
        # Extract title and href
        title_element = div.find("h2", class_="a-size-base-plus a-spacing-none a-color-base a-text-normal")
        if title_element:
            product['title'] = title_element.get_text(strip=True)
            # Find link within title container
            link = div.find("a", class_="a-link-normal s-line-clamp-4 s-link-style a-text-normal")
            if link:
                product['href'] = link.get('href')
        
        # Extract rating
        rating_element = div.find("span", class_="a-icon-alt")
        if rating_element:
            product['rating'] = rating_element.get_text(strip=True)
        
        # Extract reviews
        reviews_element = div.find("span", class_="a-size-base s-underline-text")
        if reviews_element:
            product['reviews'] = reviews_element.get_text(strip=True)
        
        # Extract popularity
        popularity_element = div.find("span", class_="a-size-base a-color-secondary")
        if popularity_element:
            product['popularity'] = popularity_element.get_text(strip=True)
        
        if product.get('title'):
            products.append(product)
    
    return products


if __name__ == '__main__':

	#https://www.octoparse.com/blog/how-to-scrape-amazon-data-using-python
	#c:/code/py_playground/.venv/Scripts/python.exe c:/code/py_playground/crawlamazonwarehouse.py >> results\golf.txt
	#.venv/Scripts/python.exe crawlamazonwarehouse.py >> results\gpu.txt
	#https://www.zenrows.com/blog/stealth-web-scraping-in-python-avoid-blocking-like-a-ninja#full-set-of-headers
	headers2 = {
	"User-Agent": random.choice(user_agents)}
	domain_url = "https://www.amazon.co.uk"
	# base_url = "https://www.amazon.co.uk/s?k=ddr4+ram+32gb&i=warehouse-deals&page="
	base_url = "https://www.amazon.co.uk/s?k=swim+goggle&i=warehouse-deals&page="
	for page_number in range(1, 2):
		time.sleep(2)
		# Create the new URL by replacing the page number
		page_url = base_url + str(page_number)
		print(page_url)

		response2 = run_web_flow(page_url)
		print("Type of data:", type(response2))

		doctype_html = response2[0].outputs[0].results['message'].data['text']
		soup2 = BeautifulSoup(doctype_html, "html.parser")
		
		#<div class="a-section a-spacing-small puis-padding-left-small puis-padding-right-small"><div data-cy="title-recipe" class="a-section a-spacing-none a-spacing-top-small s-title-instructions-style"><a class="a-link-normal s-line-clamp-4 s-link-style a-text-normal" href="/Swimming-Goggles-Men-Women-Adults/dp/B097PVPKV4/ref=sr_1_6?dib=eyJ2IjoiMSJ9.CZq0nhNp9DsMI5PLCYaVG_FoAJhz1WwEF6HHkmkolY7d99OrfPzfOCO2fGD99GeyJOfdKB4eAl4Upfax5yb821GbRH5JRD7YDzGZZFU2pUDIbx-ANBRjDgx9DhFKnHu1Ri9YkQ8Wu-q3upykjtLLxFRE7p9q4JU6CkACyxiWG9yAkFyOvPhMRVyKqaCbggz-PswkHi6eyaXXKkDLddAVo_X-UVxgyl-K0QvNPUEFHymTliCqcAonz5aVvN8TTPWdAh0l-iDaw6GHzTj0kCkMwBDlWUfv2UmAB3NllPaUUmU.kG6icoQlFJuHMwnxOb77hILW1iAOpJckjS8g9WZ1odU&amp;dib_tag=se&amp;keywords=swim+goggle&amp;m=A2OAJ7377F756P&amp;nsdOptOutParam=true&amp;qid=1735230177&amp;s=warehouse-deals&amp;sr=8-6"><h2 aria-label="Swimming Goggles for Men Women Adults - Anti Fog Swim Goggles with Uv Protection, Clear Vision, No Leaking Silicone Cushion" class="a-size-base-plus a-spacing-none a-color-base a-text-normal"><span>Swimming Goggles for Men Women Adults - Anti Fog Swim Goggles with Uv Protection, Clear Vision, No Leaking Silicone Cushion</span></h2></a> </div><div data-cy="reviews-block" class="a-section a-spacing-none a-spacing-top-micro"><div class="a-row a-size-small"><span class="a-declarative" data-version-id="v1a1xfkvrhpsev211ons9lsmfw1" data-render-id="r32ppgk3yqgs9i2kh2vbe319xi1" data-action="a-popover" data-csa-c-func-deps="aui-da-a-popover" data-a-popover="{&quot;closeButton&quot;:true,&quot;closeButtonLabel&quot;:&quot;&quot;,&quot;activate&quot;:&quot;onmouseover&quot;,&quot;name&quot;:&quot;&quot;,&quot;position&quot;:&quot;triggerBottom&quot;,&quot;popoverLabel&quot;:&quot;4.3 out of 5 stars, rating details&quot;,&quot;url&quot;:&quot;/review/widgets/average-customer-review/popover/ref=acr_search__popover?ie=UTF8&amp;asin=B097PVPKV4&amp;ref_=acr_search__popover&amp;contextId=search&quot;}" data-csa-c-type="widget"><a aria-label="4.3 out of 5 stars, rating details" href="javascript:void(0)" role="button" class="a-popover-trigger a-declarative"><i data-cy="reviews-ratings-slot" aria-hidden="true" class="a-icon a-icon-star-small a-star-small-4-5"><span class="a-icon-alt">4.3 out of 5 stars</span></i><i class="a-icon a-icon-popover"></i></a></span> <a aria-label="2,117 ratings" class="a-link-normal s-underline-text s-underline-link-text s-link-style" href="/Swimming-Goggles-Men-Women-Adults/dp/B097PVPKV4/ref=sr_1_6?dib=eyJ2IjoiMSJ9.CZq0nhNp9DsMI5PLCYaVG_FoAJhz1WwEF6HHkmkolY7d99OrfPzfOCO2fGD99GeyJOfdKB4eAl4Upfax5yb821GbRH5JRD7YDzGZZFU2pUDIbx-ANBRjDgx9DhFKnHu1Ri9YkQ8Wu-q3upykjtLLxFRE7p9q4JU6CkACyxiWG9yAkFyOvPhMRVyKqaCbggz-PswkHi6eyaXXKkDLddAVo_X-UVxgyl-K0QvNPUEFHymTliCqcAonz5aVvN8TTPWdAh0l-iDaw6GHzTj0kCkMwBDlWUfv2UmAB3NllPaUUmU.kG6icoQlFJuHMwnxOb77hILW1iAOpJckjS8g9WZ1odU&amp;dib_tag=se&amp;keywords=swim+goggle&amp;m=A2OAJ7377F756P&amp;nsdOptOutParam=true&amp;qid=1735230177&amp;s=warehouse-deals&amp;sr=8-6#customerReviews"><span aria-hidden="true" class="a-size-base s-underline-text">2,117</span> </a> </div><div class="a-row a-size-base"><span class="a-size-base a-color-secondary">100+ bought in past month</span></div></div>
		products = extract_product_info(soup2)

		if len(products)==0:
			print("===THE END===")
			break
		for product in products:
			print (product.get("title"))
			# item = title.find('a', attrs={'class':'a-link-normal s-line-clamp-4 s-link-style a-text-normal'})
			try:
				href = product.get("href")
			except Exception as e:
				continue
			# print (href)
			# Split the string using '/'
			parts = href.split('/')
			new_url = domain_url+"/dp/"+parts[3]
			used_url = domain_url+"/"+href
			new_price = print_product_info(new_url)
			used_price = print_product_info(used_url)
			try:
				discount = float(used_price[1:]) / float(new_price[1:])
			except Exception as e:
				discount = 1.8
			print("Price discount =", discount)
			if (discount < 0.6):
				print("BARGAIN!!!")
            	
			time.sleep(1)
			print()
			print()
			print()
			print()

 	# titles = [title.get_text() for title in titles]

	# print(titles)