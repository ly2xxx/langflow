from langflow.load import run_flow_from_json
TWEAKS = {
  "ChatInput-eU8kJ": {},
  "URL-ngSFm": {},
  "ChatOutput-dNxBs": {}
}

result = run_flow_from_json(flow="web-scrape-flow.json",
                            input_value="https://nobids.net/ebay-items-with-no-bids/?site_id=EBAY-GB&category_id=&keyword=golf&distance=anywhere&distance_miles=10&buyerPostalCode=&MinPrice=&MaxPrice=&FreeShipping=no&sortorder=EndTimeSoonest",
                            session_id="", # provide a session id if you want to use session state
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)

print(result)