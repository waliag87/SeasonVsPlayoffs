import csv
import requests
import os
import sys
from bs4 import BeautifulSoup
from enums import TimeOfYear    
# Scrapes all players for any given season available on natural stat trick
# Only supports 1 season at a time
def scrape(year, timeOfYear):
    print(f'scrape called with year {year} and timeOfYear {timeOfYear}')
    url = f'https://www.naturalstattrick.com/playerteams.php?fromseason={year}&thruseason={year}&stype={timeOfYear.value}&sit=5v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')

    # Create a CSV file to save the scraped data
    filename = f'scraped_data_{year}_{timeOfYear}.csv'
    os.makedirs(f'data/{year}/', exist_ok=True)
    filepath = os.path.join('data', f'{year}', filename)
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the table headers to the CSV file
        headers = [header.text for header in table.find_all('th')]
        writer.writerow(headers)
        
        # Write each row of data to the CSV file
        rows = table.find_all('tr')
        for row in rows[1:]:
            data = [cell.text for cell in row.find_all('td')]
            writer.writerow(data)

    print(f'Successfully scraped and saved data to data/{filename}.')


if __name__ == '__main__':
    # Check if three arguments are provided
    if len(sys.argv) != 5:
        print("Usage: python player_data_scraper.py --year <value1> --timeOfYear <value2>")
        sys.exit(1)

    # Extract the arguments
    year = None
    timeofYear = None
    arg3 = None

    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == '--year':
            # Year should be formatted like 20222023
            year = sys.argv[i+1]
        elif sys.argv[i] == '--timeOfYear':
            if sys.argv[i+1] in [member.name for member in TimeOfYear]:
                timeofYear = TimeOfYear[sys.argv[i+1]]
            else:
                memberList = [member.name for member in TimeOfYear]
                print(f'--timeOfYear should be one of {memberList}')
                sys.exit(1)
        else:
            print(f"Unknown argument: {sys.argv[i]}")
            sys.exit(1)

    # Verify that all arguments are provided
    if year is None or timeofYear is None:
        print("Missing one or more arguments.")
        sys.exit(1)
    
    scrape(year, timeofYear)
