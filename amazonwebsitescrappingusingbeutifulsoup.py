import bs4
import json
import requests


def parse(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    try:
        title = soup.find("span",attrs={'id':'productTitle'}).text.strip()
        saleprice1 = soup.find("span",attrs={'id':'priceblock_ourprice'})
        salesprice = saleprice1.text.strip() if saleprice1 else None
        availability = soup.find("div",attrs={'id':'availability'}).text.strip()
        category = soup.find("span",attrs={'id':'productTitle'}).text.strip()

        data = {
                'NAME':title,
                'SALE_PRICE':salesprice,
                'CATEGORY':category,
                'AVAILABILITY':availability,
                'URL':url,
                }

        return data
    except Exception as e:
        print (e)

def Scrapper():
    webList = ['B0046UR4F4',
    'B00JGTVU5A',
    'B00GJYCIVK',
    'B00EPGK7CQ',
    'B00EPGKA4G',
    'B00YW5DLB4',
    'B00KGD0628',
    'B00O9A48N2',
    'B00O9A4MEW',
    'B00UZKG8QU']
    extracted_data = []
    for i in webList:
        url = "http://www.amazon.com/dp/"+i
        print ("Processing: "+url)
        parse(url)
        extracted_data.append(parse(url))
    f=open('data.json','w')
    # print (extracted_data)
    json.dump(extracted_data,f,indent=4)


if __name__ == "__main__":
    Scrapper()