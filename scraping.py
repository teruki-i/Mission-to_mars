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

    # Run all scraping functions and store results in dictionary 
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
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


## JPL Space Images - Featured Images

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

    # add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'{url}/{img_url_rel}'
    
    return(img_url)


## Mars Facts

def mars_facts():
    
    try:
        # Create DataFrame of Mars and Earth facts 
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # format DataFrame
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert DataFrame into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemispheres(browser):

    #Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # create list of links to hemisphere pages
    html = browser.html
    hemi_soup = soup(html,'html.parser')

    path_list = []
    hemi_tag = hemi_soup.find_all('div', class_='item')

    for i in range(len(hemi_tag)):
        hemi = hemi_tag[i].find('a')['href']
        new_url = f'{url}{hemi}'
        path_list.append(new_url)

    # loop through list of hemisphere page links to get image urls and titles
    for link in path_list:
        try:
            # selects link for hemisphere
            browser.visit(link)
            
            # create empty dictionary to store image url and title
            hemi_dict = {}
            
            # find image url on hemisphere page
            img_url= browser.find_by_text('Sample')['href']
            #print(img_url)
            hemi_dict.update({'img_url':img_url})
            
            # find title on hemisphere page
            title = browser.find_by_css('h2.title').text
            hemi_dict.update({'title':title})
            
            # append to list of image urls and titles as a dictionary
            hemisphere_image_urls.append(hemi_dict)
        except:
            return None
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())