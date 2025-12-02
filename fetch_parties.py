#!/usr/bin/env python3
"""
Fetch State of the Parties data from the UK Parliament API.
Fetches data for the 1st day of every month from January 1990 to present.
"""

import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import os
import time


def get_parties_data(date):
    """
    Fetch State of the Parties data for a specific date.
    
    Args:
        date: datetime object
    
    Returns:
        JSON data if successful, None otherwise
    """
    # Format date as YYYY-MM-DD
    date_str = date.strftime('%Y-%m-%d')
    
    # Construct URL - the API format is /api/Parties/StateOfTheParties/1/YYYY-MM-DD
    url = f"https://members-api.parliament.uk/api/Parties/StateOfTheParties/1/{date_str}"
    
    try:
        response = requests.get(url, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"No data for {date_str} (Status: {response.status_code})")
            return None
            
    except requests.exceptions.RequestException as e:
        # Handle network errors, timeouts, etc.
        print(f"Error fetching {date_str}: {e}")
        return None


def save_parties_data(date, data, output_dir="parties_data"):
    """
    Save parties data to a file named by the date.
    
    Args:
        date: datetime object
        data: JSON data to save
        output_dir: Directory to save files in
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Format filename as YYYY-MM-DD.json
    filename = date.strftime('%Y-%m-%d.json')
    filepath = os.path.join(output_dir, filename)
    
    # Save data to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved: {filename}")


def main():
    """
    Main function to iterate through months and fetch parties data.
    """
    # Start date: 1st January 1990
    start_date = datetime(1980, 1, 1)
    
    # End date: 1st of current month
    today = datetime.now()
    end_date = datetime(1990, 1, 1)
    
    current_date = start_date
    success_count = 0
    failure_count = 0
    
    print(f"Fetching State of the Parties data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Total months to process: {(end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1}")
    print("-" * 60)
    
    while current_date <= end_date:
        # Fetch data for current date (1st of the month)
        data = get_parties_data(current_date)
        
        if data is not None:
            save_parties_data(current_date, data)
            success_count += 1
        else:
            failure_count += 1
        
        # Move to next month (1st of next month)
        current_date += relativedelta(months=1)
        
        # Be polite to the API - add a small delay
        time.sleep(0.2)
    
    print("-" * 60)
    print(f"Completed! Total successful: {success_count}, Total failed: {failure_count}")


if __name__ == "__main__":
    main()
