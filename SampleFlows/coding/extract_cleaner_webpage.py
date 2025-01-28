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
        return clean_data

# Usage
async def main():
    url = "https://sports.ladbrokes.com/sport/football/matches/today"
    clean_content = await extract_clean_content(url)
    print("Title:", clean_content['title'])
    print("\nMain Content:")
    for item in clean_content['main_content']:
        print(f"{item['type'].upper()}: {item['text']}")
    print("\nLinks:")
    for link in clean_content['links']:
        print(f"- {link['text']}: {link['url']}")

if __name__ == "__main__":
    asyncio.run(main())
