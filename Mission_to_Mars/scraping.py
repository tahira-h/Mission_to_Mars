#pip install splinter

#pip install webdriver_manager

#pip install bs4

#pip install pymongo

# Import tools Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
# Import pandas 
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    # Initialize headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    hemisphere_image_url = hemispheres(browser)



    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere_image_url,
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Scrape Mars Data: The News

# Insert code into a function
def mars_news(browser):
    # Visit the mars nasa new site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try: 
        slide_elem = news_soup.select_one('div.list_text')
        
        # Begin scraping
        #slide_elem.find('div', class_='content_title')

        # Let's get just the text, not the HTML tags or elements

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Note:
        # If using '.find_all()' instead of '.find()' when pulling the summary, we would retrieve all of the summaries on the page instead of just the first one. '.find()' is to retrieve the first tags and attributes, or first summary. 

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None 

    # return
    return news_title, news_p

# ### Featured Images

# Scrape Mars Data: Featured Image

def featured_image(browser):
    # Visit URL 
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse to continue and scrape the full-size image URL.

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try: 
        # Use the image tag and class (<img /> and fancybox-img) to build the URL to the full-size image.

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None 

    # When looking at our address bar in the webpage, can see the entire URL up there already; we need to add the first portion to the app.

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

    # NOTE: 
    # f-string print statements as shown above is a cleaner way to create print statements. 

# Scrape Mars Data: Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # Scrape the entire table with .read_html() function
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert the DataFrame back into HTML-ready code using .to_html() function
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

# NOTE:
# Now that everything is gathered, end the automated browsing session by using browser.quit()

# Without browser.quit(), the browser will not know when to shut down. It iwll continue to listen for instructions and use the computer's resources, putting a strain on memory or laptop/computer.

def hemispheres(browser):
    url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
    browser.visit(url)
    
    hemisphere_image_urls = []
    im = browser.find_by_css("a.product-item img")

    for i in range(len(im)):
        hemisphere = {}
        browser.find_by_css("a.product-item img")[i].click()
        sample = browser.find_by_text("Sample")[0]
        hemisphere['link'] = sample["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    return hemisphere_image_urls

# Stop webdriver
    browser.quit()


