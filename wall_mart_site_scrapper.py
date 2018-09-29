import requests
import json
from bs4 import BeautifulSoup
import pandas as pd 
import matplotlib.pyplot as plt

all_laptop_data = []
url = "https://www.walmart.com/browse/electronics/laptop-computers/hp/3944_3951_132960/YnJhbmQ6SFAie?page=1#searchProductResult"
def data_to_csv(data):
    with open('laptop_data.json','w') as f:
        json.dump(data,f)

def url_parser(wall_mart_laptop_url):
    laptop_info_list = []
    # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page =  requests.get(wall_mart_laptop_url)
    page_html = BeautifulSoup(page.text,'html.parser')
    laptop_html_info_list = page_html.find_all("li",attrs = {'class':'Grid-col'})
    for laptop_html_info in laptop_html_info_list:
        data = {}
        # print (laptop_html_info)
        name_html = laptop_html_info.find("div",attrs = {'class':'search-result-product-title'})
        data['name'] = name_html.find("a",attrs = {'class':'product-title-link'})['aria-label']
        # print (laptop_html_info.find("span",attrs = {'class':'price-group'}))
        # data['price'] = None if laptop_html_info.find("span",attrs = {'class':'price-group'}) == None else  laptop_html_info.find("span",attrs = {'class':'price-group'})['aria-label']
        # print (laptop_html_info.find("span",attrs = {'class':'stars-reviews-count'}).span.text)
        
        data['review_count'] = int(laptop_html_info.find("span",attrs = {'class':'stars-reviews-count'}).span.text) if laptop_html_info.find("span",attrs = {'class':'stars-reviews-count'}) else 0
        # print (data['review_count'])
        # data['review_count'] = laptop_html_info.find("span",attrs = {'class':'stars-reviews-count'}).span.span.text
        # data['rating'] = laptop_html_info.find("span",attrs = {'class':'stars-container'})['aria-label']
        laptop_info_list.append(data)
    return laptop_info_list
for page_no in range(1,26):
    print ("processing {} page".format(page_no))
    url_page = "https://www.walmart.com/browse/electronics/laptop-computers/hp/3944_3951_132960/YnJhbmQ6SFAie?page="+str(page_no)+"#searchProductResult"
    all_laptop_data.extend(url_parser(url_page))
data_to_csv(all_laptop_data)

with open('laptop_data.json','r') as f:
    data = json.load(f)

pandas_data = pd.DataFrame.from_dict(data)
# print (pandas_data)
# pandas_data.reset_index(drop = True, inplace = True)
# pandas_data = pandas_data.set_index('name')

plot = pandas_data.sort_values(by=['review_count'],ascending=False).head(10)
# print ( plot.loc[:, 'review_count'].tolist())
slices = plot.loc[:, 'review_count'].tolist()
# print (slices)
activities = plot.loc[:, 'name'].tolist()


plt.pie(slices,
        labels=activities,
        startangle=90,
        shadow= True)

plt.title('Interesting Graph\nCheck it out')
plt.show()