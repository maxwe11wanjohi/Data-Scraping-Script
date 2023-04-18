import requests
from bs4 import BeautifulSoup
import pandas as pd

keyword = 'alcohol'
url = f'https://www.google.com/search?q={keyword}&start=0'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(response.content, 'html.parser')

data_list = []
for element in soup.find_all('div', {'class': 'g'}):
    data = {}
    try:
        # Extract query
        data['query'] = keyword
        
        # Extract summary
        data['summary'] = element.find('h3').get_text()
        
        # Extract number of searches
        search_result_stats = element.find('div', {'class': 's'}).get_text()
        num_searches = search_result_stats.split('About ')[1].split(' results')[0].replace(',', '')
        data['num_searches'] = int(num_searches)
        
        # Extract explanation
        data['explanation'] = search_result_stats.split(' - ')[1]
        
        data_list.append(data)
    except:
        pass

df = pd.DataFrame(data_list)
df.to_csv('search_results.csv', index=False)
