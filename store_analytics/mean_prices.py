import requests
import json
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt

# Must start scrapyrt server. (In project, execute scrapyrt -p <PORT>)
link = "http://localhost:3000/crawl.json?start_requests=true&spider_name=BookSpider"
response = requests.get(link)
data = response.json()

# with open('data') as json_file:
#     data = json.load(json_file)

for item in data['items']:
    item['stars'] = item['stars'][0]
    item['title'] = item['title'][0]
    item['price'] = item['price'][0]

books_data = json_normalize(data['items']).sort_values('stars')
mdf = books_data.groupby(['stars'])['stars', 'price'].mean()
p = mdf.plot(kind='bar', x='stars', y='price', color='red')
p.set_xlabel("Stars")
p.set_ylabel("Mean Price")
plt.show()
