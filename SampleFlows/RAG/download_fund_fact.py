import pandas as pd
import requests
import os
from pathlib import Path

def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    return False

def main():
    # Create output directory if it doesn't exist
    output_dir = Path('input/factsheets')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read the CSV file
    df = pd.read_csv('input/LGIM Fund Centre Download 2025-01-02_nongen3.csv')
    
    # Process each row
    for _, row in df.iterrows():
        fund_code = row['L&G Fund Code']
        fact_sheet_url = row['Fact sheet'].split(',')[0]  # Get URL before first comma
        
        # Extract original filename from URL
        original_filename = fact_sheet_url.split('/')[-1]
        # Create new filename with fund code prefix
        new_filename = f"{fund_code}_{original_filename}"
        
        # Full path for saving
        output_path = output_dir / new_filename
        
        print(f"Downloading {fund_code} fact sheet...")
        success = download_pdf(fact_sheet_url, output_path)
        if success:
            print(f"Successfully downloaded: {new_filename}")
        else:
            print(f"Failed to download: {fact_sheet_url}")

if __name__ == "__main__":
    main()
