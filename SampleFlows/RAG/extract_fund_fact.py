from bs4 import BeautifulSoup
import requests
from pathlib import Path
from langflow.load import run_flow_from_json

TWEAKS = {
  "ChatInput-eU8kJ": {},
  "URL-ngSFm": {},
  "ChatOutput-dNxBs": {}
}
 
def run_web_flow(scrape_url):
	# Get current file's directory
	current_dir = Path(__file__).parent.parent

	# Construct path to json relative to current file
	flow_path = current_dir / "WebAgent" / "web-scrape-flow.json"

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

# Replace this URL with the URL of the page you want to scrape
url = 'https://fundcentres.lgim.com/en/uk/workplace-employee/fund-centre/?isin_code=B1D3#Product=WorkSave-Pension-Plan-(non-generation-3)'

# Get the webpage content
# response = requests.get(url)
# data = response.text
data = run_web_flow(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(data, 'html.parser')

# Find all "Fact sheet" download URLs
fact_sheet_urls = []
for link in soup.find_all('a', href=True):
    if 'Fact sheet' in link.text:
        fact_sheet_urls.append(link['href'])

# Print the URLs
for url in fact_sheet_urls:
    print(url)
