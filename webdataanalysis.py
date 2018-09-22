import urllib
import bs4
import pandas as pd
import numpy as np
import json

def parse_comment_page(page_url):
    #Adding a User-Agent String in the request to prevent getting blocked while scraping 
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    request = urllib.request.Request(page_url,headers={'User-Agent': user_agent})
    html = urllib.request.urlopen(request).read()
    soup = bs4.BeautifulSoup(html,'html.parser')
    main_post = soup.find('div',attrs={'id':'siteTable'})
    title = main_post.find('a',attrs={'class':'title'}).text
    upvotes = main_post.find('div',attrs={'class':'score unvoted'}).text
    original_poster = main_post.find('a',attrs={'class':'author'}).text
    comments_count = main_post.find('a',attrs={'class':'bylink comments may-blank'}).text
    comment_area = soup.find('div',attrs={'class':'commentarea'})
    comments = comment_area.find_all('div', attrs={'class':'entry unvoted'})
    extracted_comments = []
    for comment in comments: 
        if comment.find('form'):
            #We are now looking for any element with a class of author in the comment, instead of just looking for a tags. 
            #We noticed some comments whose authors have deleted their account shows up with a span tag instead of an a 
            commenter = comment.find(attrs={'class':'author'}).text
            comment_text = comment.find('div',attrs={'class':'md'}).text.strip()
            permalink = comment.find('a',attrs={'class':'bylink'})['href']
            extracted_comments.append({'commenter':commenter,'comment_text':comment_text,'permalink':permalink})
    #Lets put the data in dict 
    post_data = {
        'title':title,
        'no_of_upvotes':upvotes,
        'poster':original_poster,
        'no_of_comments':comments_count,
        'comments':extracted_comments
    }
    return post_data
try:
    # url = 'https://www.google.com/search?q=python'

    # now, with the below headers, we defined ourselves as a simpleton who is
    # still using internet explorer.
    url = "https://old.reddit.com/top/"
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = urllib.request.Request(url, headers = headers)
    # resp = urllib.request.urlopen(req)
    # respData = resp.read()
    beautiful = urllib.request.urlopen(req).read()
    soup = bs4.BeautifulSoup(beautiful, 'html.parser')
    # saveFile = open('withHeaders.txt','w')
    # saveFile.write(str(beautiful))
    # saveFile.close()
    # soup = BeautifulSoup(html, 'html.parser')
    # for i in soup.findAll('h2'):
    #     print (i.text)
    # print (soup.findAll('h2').contents)
    # print (soup.prettify())
    #get the HTML of the table called site Table where all the links are displayed
    main_table = soup.find("div",attrs={'id':'siteTable'})
    #Now we go into main_table and get every a element in it which has a class "title" 
    comment_a_tags = main_table.find_all('a',attrs={'class':'bylink comments may-blank'})
    #from each link extract the text of link and the link itself
    #List to store a dict of the data we extracted 
    #from each link extract the text of link and the link itself
    #List to store a dict of the data we extracted 
    extracted_records = []
    for link in comment_a_tags: 
        title = link.text
        url = link['href']
        #There are better ways to check if a URL is absolute in Python. For sake simplicity we'll just stick to .startwith method of a string 
        # https://stackoverflow.com/questions/8357098/how-can-i-check-if-a-url-is-absolute-using-python 
        if not url.startswith('http'):
            url = "https://reddit.com"+url 
        # You can join urls better using urlparse library of python. 
        # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin
        print('Extracting data from %s'%url)
        #Lets wait for 5 seconds before we make requests, so that we don't get blocked while scraping. 
        #if you see errors that say HTTPError: HTTP Error 429: Too Many Requests , increase this value by 1 second, till you get the data. 
        extracted_records.append(parse_comment_page(url))
        #Lets wait for 10 seconds before we ma 
        # record = {
        #     'title':title,
        #     'url':url
        #     }
        # extracted_records.append(record)
    # print(extracted_records)
    with open('data.json', 'w') as outfile:
        json.dump(extracted_records, outfile)
except Exception as e:
    print(str(e))
