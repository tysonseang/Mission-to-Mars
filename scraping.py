# Import Splinter, BeautifulSoup, Pandas, and datetime dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

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
        "last_modified": dt.datetime.now(),
        "hemisphere_data": hemisphere_data(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# Featured Articles

def mars_news(browser):

    # Visit the Mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
            return None, None

    return news_title, news_p


# Featured Images

def featured_image(browser):

    # Visit Space Images URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


# Featured Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # Create a dataFrame from Galaxy Facts table using 'read_html'
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
       return None

    # Assign columns and set description as table index
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert df to html format, add bootstrap
    return df.to_html(classes="table table-striped")



# Hemisphere Images

def hemisphere_data(browser):
    
    #  Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    #  Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.

    # Find the hemisphere image link and click on it 
    hemisphere_img = browser.find_by_css('a.product-item img')
    print(len(hemisphere_img))
    
    for i in range(len(hemisphere_img)):
        hemispheres = {}
        browser.find_by_css('a.product-item img')[i].click()

        # Parse the image title
        hemisphere_img_title = browser.find_by_css('h2.title').text
        hemispheres['title'] = hemisphere_img_title
        
        
        # Use "Sample" link to access url add-on and add it to homepage root url
        sample = browser.find_by_css('li a')[0]['href']
        hemispheres['img_url'] = sample

        hemisphere_image_urls.append(hemispheres)

        # Use browser back to return to homepage to access next image link
        browser.back()

    return hemisphere_image_urls



if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())