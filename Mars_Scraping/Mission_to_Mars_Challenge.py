#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


import pandas as pd


# In[3]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[5]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[6]:


# title and summary text
slide_elem = news_soup.find_all('div', class_= 'list_text')

for results in slide_elem:

    titles = results.find('div', class_= 'content_title')
    summary = results.find('div', class_= 'article_teaser_body')
    
    if(titles and summary):
        print("------------------")
        print("TITLE: ")
        print(titles.text)
        print("SUMMARY: ")
        print(summary.text)    


# ### Featured Images

# In[7]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[8]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[9]:


# Parse the resulting html with soup

html = browser.html
img_soup = soup(html, 'html.parser')


# In[10]:


# Find the relative image url
img_url_rel =  img_soup.find('img',class_='fancybox-image').get('src')
img_url_rel


# In[11]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # Tables

# In[12]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description','Mars','Earth']
df.set_index('description', inplace=True)
df


# In[13]:


# onvert our DataFrame back into HTML-ready code 
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[14]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[15]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

for i in range(0,4):
    image_title_link = browser.find_by_tag('h3')[i]
    image_title_link.click()
    
    # Parse the HTML
    html = browser.html
    html_soup = soup(html, 'html.parser')
    
    # Create a dictionary
    hemispheres = {}
    
    # Scrapes the image
    img_url_div = html_soup.find_all('div', class_ = 'downloads')
    img_url_li = img_url_div[0].find('li')
    img_url_rel = img_url_li.a['href']
    img_url = f'https://marshemispheres.com/{img_url_rel}'
    
    # Scrapes the title
    title = html_soup.find('h2').text
    
    # Add image and title to dictionary
    hemispheres['img_url'] = img_url
    hemispheres['title'] = title
    
    # Append the dictionary to list
    hemisphere_image_urls.append(hemispheres)

    # To get back to previous page
    browser.back()


# In[16]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[18]:


# 5. Quit the browser
browser.quit()

