# Import Libraries
import requests
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tqdm.notebook import tqdm
from tqdm import tqdm as tqdm2
from tqdm.contrib.concurrent import thread_map
import pandas as pd 
import os 
import string 
# User Agent Declaration
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
headers = {'user-agent':useragent}

# Initializing Empty Lists for Templates # 01 & 02
Templates_1 = []
Templates_2 = []



# FUNCTIONS FOR TEMPLATE DATA
def get_templates1(link , Products):
    r = requests.get(link, headers=headers).text
    soup = BeautifulSoup(r , 'lxml')
    items = soup.select('.tm-templates_grid_item')
    for i in items:
        # Name
        name = i.select_one('.template-name').text.strip()
        # Thumbnail
        thumbnail = i.select_one('.tm-card_image')['src']
        # URL
        tname = i.select_one('.template-name')['href']
        URL = 'https://webflow.com'+tname
        # PRICE
        price = i.select_one('.price-tag').text.replace('USD','').strip().replace('Use for','').strip()
        # MAIN TAG
        maintag = i.select_one('.icons-wrap .category-text').text.strip()
        data1 = {
            'Name' : name,
            'Price' : price,
            'Main Tag': maintag,
            'Thumbnail': thumbnail,
            'URL': URL
        }
        # Product URL of a category
        Products.append(URL)
        # Data-Template - 1
        Templates_1.append(data1)
    return

def get_templates2(link):
    r = requests.get(link,headers=headers).text
    soup = BeautifulSoup(r , 'lxml')
    # By 
    try:
        by = soup.select_one('.template-designer-name').text.strip()
    except:
        by = 'NAN'
    
    # Tags
    tags_list = soup.find_all('a' , class_='hero_tag-list_link w-inline-block')
    tags = []
    for i in range(0,len(tags_list)):
        tags.append(tags_list[i].text.strip())
    tags = ','.join(tags)

    # Excerpt
    excerpt = soup.select_one('.cc-templates').text.strip()

    # Preview in Browser
    preview = soup.find('div' , class_='templates_button-flexrow').find_all('a')
    for i in preview:
        if 'Preview in browser' in i.text:
            pib = i['href']
            break
    # Preview in Designer
    for i in preview:
        if 'Preview in Designer' in i.text:
            pid = i['href']
    
    # Slider Images
    imageslist = soup.select('#owl-carousel img')
    imglinklist = []
    for i in imageslist:
        imagelink = i['src']
        imglinklist.append(imagelink)
    SliderImages = ",".join(imglinklist)

    # Overview
    overview = soup.find('div' , class_='templates_rtf w-richtext')

    # Features
    featuresdiv = soup.select('.feature_accordion_cms-name')
    featureslist = []
    for i in featuresdiv:
        featureslist.append(i.text.strip())
    features = ','.join(featureslist)
    data2 = {
        'By': by,
        'Tags': tags,
        'Excerpt': excerpt,
        'Preview in Browser': pib,
        'Preview in Designer': pid,
        'Slider Images': SliderImages,
        'Overview': overview,
        'Features':features
    }
    # Data-Template-2
    Templates_2.append(data2)
    return



# Empty list for Tags Data
DATA_tags = []



# FUNCTION FOR TAGS DATA
def get_tag(link):
    r = requests.get(link , headers=headers).text
    soup = BeautifulSoup(r , 'lxml')
    # Tag
    Tag = link.split('/')[-1].replace('-websites','').strip()
    # URL
    URL = link
    # TITLE
    title = soup.select_one('.page-title').text.strip()
    # TEXT
    text = soup.select_one('.w-embed p').text.strip()
    # TEMPLATES
    TemplatesList = []
    templates_css = soup.select('.primary-tag-list .template-name')
    for i in templates_css:
        TemplatesList.append(i.text.strip())
    
    
    Templates = ','.join(TemplatesList)
    # Data
    TagsData = {
        'Tag': Tag,
        'URL': URL,
        'Title': title,
        'Text': text,
        'Templates': Templates
    }
    # print(TagsData)
    DATA_tags.append(TagsData)
    return


# Empty list for Features Data
DATA_Features = []

# FUNCTION FOR FEATURES
def get_features(link):
    r = requests.get(link , headers=headers).text
    soup = BeautifulSoup(r , 'lxml')
    # Feature
    Feature = link.split('/')[-1].replace('-websites','').strip()
    # URL
    URL = link
    # TITLE
    title = soup.select_one('.page-title').text.strip()
    # TEXT
    text = soup.select_one('.w-embed p').text.strip()
    # TEMPLATES
    TemplatesList = []
    templates_css = soup.select('.template-name')
    for i in templates_css:
        TemplatesList.append(i.text.strip())
    
    
    Templates = ','.join(TemplatesList)
    
    # Data
    TagsData = {
        'Feature': Feature,
        'URL': URL,
        'Title': title,
        'Text': text,
        'Templates': Templates
    }
    DATA_Features.append(TagsData)
    return


  
  
# Empty lists for URLs

Category_Links = []
Tags_Links = []
Features_Link = []

# FUNCTION to get Template Category LINKS
def getcategorylinks():
    link = 'https://webflow.com/sitemap'
    r = requests.get(link , headers=headers).text
    soup = BeautifulSoup(r , 'lxml')
    div = soup.select('.tag-link')
    for i in div:
        Category_Links.append(i['href'])
    return

# FUNCTION to get Tags LINKS
def gettaglinks():
    link = 'https://webflow.com/templates/tags'
    r = requests.get(link , headers=headers).text
    soup = BeautifulSoup(r , 'lxml')
    tagdiv = soup.find('div' , {'id': 'all-tags-section'})
    atags = tagdiv.find_all('a' , class_='all-tags_link')
    for i in atags:
        taglink = 'https://webflow.com'+ i['href']
        Tags_Links.append(taglink)
    return


# FUNCTION to get FEATURES LINKS
def getfeaturelinks():
    link = 'https://webflow.com/templates/tags'
    r = requests.get(link, headers=headers).text
    soup = BeautifulSoup(r , 'lxml')
    div = soup.select('#w-node-ea53e9d9-bdc8-2fe2-cc65-8f65d5cf8cf5-cefe9c24 .all-tags_link')
    for i in div:
        featurelink = 'https://webflow.com'+ i['href']
        Features_Link.append(featurelink)
    return

# Getting LINKS
getcategorylinks()
gettaglinks()
getfeaturelinks()

print(f'Total Templates Categories: {len(Category_Links)}')
print(f'Total Tags: {len(Tags_Links)}')
print(f'Total Features: {len(Features_Link)}')

print('\n')
print('Starting to scrape the Categories')
print('\n')

for i in range(len(Category_Links)):
    Products = []
    get_templates1(Category_Links[i] , Products) # Templates_1 filled.
    if len(Products)==0:
        continue

    print(f'Scraping Category: {i+1} of {len(Category_Links)} ---- Total Templates: {len(Products)}')
    for j in tqdm(Products):
        get_templates2(j) # Templates_2 filled.
    



###########################################
print('Starting to scrape the Tags')
thread_map(get_tag , Tags_Links , max_workers=10)
print('Starting to scrape the Features')
thread_map(get_features , Features_Link , max_workers=10)


print('\n')

print('Scrapping Completed........')
print('\n')
print('Storing the Data')

df1 = pd.DataFrame(Templates_1)
df2 = pd.DataFrame(Templates_2)
Templates_df = pd.concat([df1, df2], axis=1, join='inner')
# Arrange the columns
Templates_df = Templates_df[
    [
        'Name',
        'By',
        'Price',
        'Thumbnail',
        'Main Tag',
        'Tags',
        'Excerpt',
        'URL',
        'Preview in Browser',
        'Preview in Designer',
        'Slider Images',
        'Overview',
        'Features'
    ]
]


df_tag = pd.DataFrame(DATA_tags)
df_feature = pd.DataFrame(DATA_Features)

with pd.ExcelWriter('MasterData.xlsx') as writer:
    Templates_df.to_excel(writer , sheet_name='Templates' , index=False)
    df_tag.to_excel(writer , sheet_name = 'Tags' , index=False)
    df_feature.to_excel(writer , sheet_name='Features' , index=False)


print('Data stored to EXCEL Sheet')
print('\n')


Templates_df.to_csv('Templates.csv' , index=False)
df_tag.to_csv('Tags.csv' , index=False)
df_feature.to_csv('Features.csv' , index=False)

print('Data stored to CSV')

print('\n Bye Bye ......')
