# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres" : scrape_hemisphere_data(browser)
    }
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    html = df.to_html()
    marshtml = html.replace('class="dataframe"', 'class="table table-striped table-hover table-responsive"')
    return marshtml

def scrape_hemisphere_data(browser):
    # Add try/except for error handling
    try:

        # 1. Use browser to visit the URL 
        url = 'https://marshemispheres.com/'
        browser.visit(url)

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

    except BaseException:
        return None

        # 4. Print the list that holds the dictionary of each image url and title.
        #hemisphere_image_urls

        # 5. Quit the browser
        # browser.quit()

    return hemisphere_image_urls



if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())