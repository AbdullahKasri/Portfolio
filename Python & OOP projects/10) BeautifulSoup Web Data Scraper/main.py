import pandas as pd
import requests
from bs4 import BeautifulSoup


url = input("Enter URL of the page containing the table: ")
headers = {'User-Agent': 'Mozilla/5.0'}
res = requests.get(url, headers=headers)

if res.status_code == 200:
    soup = BeautifulSoup(res.content, 'html.parser')
    table = soup.find_all('table')[0] # assuming there is only one table on the page

    df = pd.read_html(str(table))[0] # convert table HTML to dataframe

    csv_file = input("Enter name of the CSV file to save the data: ")
    df.to_csv(f"{csv_file}.csv", index = False)
    print(f"Table data saved to {csv_file}")
else:
    print("Unable to access the website for scraping. Please check the URL or try again later.")
