from extract_cleaner_webpage import extract_clean_content
import asyncio
import json
from datetime import datetime

class FlightPriceExtractor:
    def __init__(self):
        self.outbound_prices = {str(i): "£na" for i in range(1, 32)}
        self.inbound_prices = {str(i): "£na" for i in range(1, 32)}

    async def extract_prices(self, url):
        clean_content = await extract_clean_content(url)

        found_monthly_prices = False
        prices_data = []
        
        for item in clean_content['main_content']:
            if item['type'] == 'h1' and 'Monthly prices' in item['text']:
                found_monthly_prices = True
                continue
            if found_monthly_prices:
                text = item['text']
                if text:
                    prices_data.append(text)
                    
        current_number = None
        for item in prices_data:
            if item.startswith('£'):
                if current_number:
                    self.outbound_prices[str(current_number)] = item
                current_number = None
            elif item.isdigit():
                current_number = int(item)
        
        return self._prepare_output()

    def _prepare_output(self):
        output = {
            "outbound_month": "July 2025",
            "outbound_prices": self.outbound_prices,
            "inbound_month": "August 2025",
            "inbound_prices": self.inbound_prices
        }
        
        filename = f"flight_prices_{datetime.now().strftime('%Y_%m_%d')}.json"
        with open(filename, 'w') as f:
            json.dump(output, f, indent=4)
            
        # Find lowest outbound price and its date
        outbound_valid_prices = {day: int(price.replace('£', '')) 
                                for day, price in self.outbound_prices.items() 
                                if price != '£na'}
        if outbound_valid_prices:
            lowest_outbound_day = min(outbound_valid_prices, key=outbound_valid_prices.get)
            lowest_outbound = f"£{outbound_valid_prices[lowest_outbound_day]}"
            lowest_outbound_date = f"July {lowest_outbound_day}, 2025"
        else:
            lowest_outbound = "£na"
            lowest_outbound_date = "no date available"

        # Find lowest inbound price and its date
        inbound_valid_prices = {day: int(price.replace('£', '')) 
                            for day, price in self.inbound_prices.items() 
                            if price != '£na'}
        if inbound_valid_prices:
            lowest_inbound_day = min(inbound_valid_prices, key=inbound_valid_prices.get)
            lowest_inbound = f"£{inbound_valid_prices[lowest_inbound_day]}"
            lowest_inbound_date = f"August {lowest_inbound_day}, 2025"
        else:
            lowest_inbound = "£na"
            lowest_inbound_date = "no date available"
        
        print(f"Lowest outbound price (July 2025): \033[91m{lowest_outbound}\033[0m on {lowest_outbound_date}")
        print(f"Lowest inbound price (August 2025): \033[91m{lowest_inbound}\033[0m on {lowest_inbound_date}")
        print(f"Outbound July 21st price: \033[97m{self.outbound_prices['21']}\033[0m")
        print(f"Inbound August 11th price: \033[97m{self.inbound_prices['11']}\033[0m")
        
        return output


if __name__ == "__main__":
    url = "https://www.skyscanner.net/transport/flights/GLAS/CSHA/cheapest-flights-from-Glasgow-to-Shanghai.html?oym=2507&iym=2508&preferDirects=false&qp_prevPrice=378&qp_prevProvider=mas_adfeeds&qp_prevCurrency=GBP&utm_medium=display&utm_source=criteo&utm_campaign=uk-flights-conversion-cookiepool&utm_content=feed&utm_term=71517&AssociateID=DIS_FLI_00053_00000&campaign_id=21172&adgroupid=71517&click_timestamp=1738103951&utm_id=71517&cto_pld=sZgC93gLAAD9us0aCVsoLg&selectedoday=21&selectediday=11"
    extractor = FlightPriceExtractor()
    asyncio.run(extractor.extract_prices(url))

