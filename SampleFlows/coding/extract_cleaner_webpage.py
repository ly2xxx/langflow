from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio

async def extract_clean_content(url):
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state('networkidle')
        
        html_content = await page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove all style and script elements
        for element in soup(['style', 'script', 'link', 'meta']):
            element.decompose()
            
        # Extract just the meaningful text content
        clean_data = {
            'title': soup.title.string.strip() if soup.title else '',
            'main_content': [],
            'links': []
        }
        
        # Get main content (headings and paragraphs)
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p']):
            text = tag.get_text().strip()
            if text:
                clean_data['main_content'].append({
                    'type': tag.name,
                    'text': text
                })
        
        # Get links with their text
        for link in soup.find_all('a'):
            href = link.get('href')
            text = link.get_text().strip()
            if href and text:
                clean_data['links'].append({
                    'text': text,
                    'url': href
                })
                
        await browser.close()

        print("Title:", clean_data['title'])
        print("\nMain Content:")
        for item in clean_data['main_content']:
            print(f"{item['type'].upper()}: {item['text']}")
        print("\nLinks:")
        for link in clean_data['links']:
            print(f"- {link['text']}: {link['url']}")
        return clean_data

# Usage
async def main(url):
    # url = "https://www.skyscanner.net/transport/flights/GLAS/CSHA/cheapest-flights-from-Glasgow-to-Shanghai.html?oym=2504&iym=2504&preferDirects=false&qp_prevPrice=378&qp_prevProvider=mas_adfeeds&qp_prevCurrency=GBP&utm_medium=display&utm_source=criteo&utm_campaign=uk-flights-conversion-cookiepool&utm_content=feed&utm_term=71517&AssociateID=DIS_FLI_00053_00000&campaign_id=21172&adgroupid=71517&click_timestamp=1738103951&utm_id=71517&cto_pld=sZgC93gLAAD9us0aCVsoLg&selectedoday=01&selectediday=01"
    # url = "https://www.skyscanner.net/transport/flights/GLAS/CSHA/cheapest-flights-from-Glasgow-to-Shanghai.html?oym=2507&iym=2508&preferDirects=false&qp_prevPrice=378&qp_prevProvider=mas_adfeeds&qp_prevCurrency=GBP&utm_medium=display&utm_source=criteo&utm_campaign=uk-flights-conversion-cookiepool&utm_content=feed&utm_term=71517&AssociateID=DIS_FLI_00053_00000&campaign_id=21172&adgroupid=71517&click_timestamp=1738103951&utm_id=71517&cto_pld=sZgC93gLAAD9us0aCVsoLg&selectedoday=21&selectediday=11"
    clean_content = await extract_clean_content(url)

if __name__ == "__main__":
    url = "https://footballdatabase.com/ranking/world/1"
    asyncio.run(main(url))
