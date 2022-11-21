#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib.request
import requests
import pandas as pd


# In[2]:


website = input("Enter the website name")

URL = "https://" + website + "/sitemap.xml"
req = urllib.request.urlopen(URL)
xml = BeautifulSoup(req, 'xml')

for feed in xml.findAll('loc'):
    if website + "/sitemap_products" in feed.text:
        product_feed = feed.text
        print("Done", product_feed)
        


# In[3]:


page_links = []
req = urllib.request.urlopen(product_feed)
xml = BeautifulSoup(req, 'xml')

for item in xml.findAll('loc'):
    if website + "/products" in item.text:
        page_links.append(item.text)
        print("Done", item.text)

print(len(page_links))
        


# In[ ]:


header = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' }

test = ['https://themagictoyshop.co.uk/products/100-coloured-wooden-blocks-in-a-tub']
videos = []
for i in page_links:
    r = requests.get(i)
    soup = BeautifulSoup(r.content,'html.parser')
    sku = soup.find('span', class_="product-meta__sku-number").text
    youtube = soup.find('div', class_='video-wrapper')
    video_object = soup.find('video')
    number_of_image_pro = soup.find('div', class_="product-gallery__carousel product-gallery__carousel--zoomable")
    number_of_image = number_of_image_pro.get('data-media-count')
    
    if video_object:
        video_pre_url = video_object.find('source')
        video_url = video_pre_url.get('src')    
    elif youtube:
        video_pre_url = youtube.find('iframe')
        video_url = video_pre_url.get('src')      
    else:
        video_url = "No Video"
    buy_it_button = soup.find('div', class_='product-form__payment-container').text
    if 'Sold out' in buy_it_button:
        available = 'Sold Out'
    else:
        available = 'In Stock'
    
    video = {
            'URL' : video_url,
            'SKU' : sku,
            'Number Of Images': number_of_image,
            'Available' : available
        }
    print(video)
    videos.append(video)

print(videos)


# In[5]:


df = pd.DataFrame(videos)
df.to_csv(website +'-videos.csv') 

