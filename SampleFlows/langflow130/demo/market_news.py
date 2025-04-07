import requests
url = "http://localhost:7880/api/v1/run/09072bb7-b3fb-4650-8d36-f4d58794dd1b"  # The complete API endpoint URL for this flow

# Request payload configuration
payload = {
    "input_value": "Research amazon stocks",  # The input value to be processed by the flow
    "output_type": "chat",  # Specifies the expected output format
    "input_type": "chat"  # Specifies the input format
}

# Request headers
headers = {
    "Content-Type": "application/json"
}

try:
    # Send API request
    response = requests.request("POST", url, json=payload, headers=headers)
    response.raise_for_status()  # Raise exception for bad status codes

    # Print response
    print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
except ValueError as e:
    print(f"Error parsing response: {e}")
    