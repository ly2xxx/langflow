import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime

async def extract_webpage(url):
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state('networkidle')
        await page.screenshot(path="example.png")
        
        # Get page content with await
        html_content = await page.content()

        # Save raw HTML
        with open(f'extracted_page_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract data
        data = {
            'title': soup.title.string if soup.title else '',
            'text': soup.get_text(),
            'links': [a.get('href') for a in soup.find_all('a')]
        }
        
        await browser.close()
        return data

async def run():
    url = "https://identitysso.betfair.com/view/login"
    data = await extract_webpage(url)
    print(data)

if __name__ == "__main__":
    asyncio.run(run())

