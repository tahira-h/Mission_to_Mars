# pip install splinter

# pip install webdriver_manager

# pip install bs4

# pip install pymongo

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)

# Scrape Mars Data: The News

# Visit the mars nasa new site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# Begin scraping
slide_elem.find('div', class_='content_title')

# Let's get just the text, not the HTML tags or elements

# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Note:
# If using '.find_all()' instead of '.find()' when pulling the summary, we would retrieve all of the summaries on the page instead of just the first one. '.find()' is to retrieve the first tags and attributes, or first summary. 

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# Featured Images

# Scrape Mars Data: Featured Image

# Visit URL 
url = 'https://spaceimages-mars.com/'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse to continue and scrape the full-size image URL.

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Use the image tag and class (<img /> and fancybox-img) to build the URL to the full-size image.

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# When looking at our address bar in the webpage, can see the entire URL up there already; we need to add the first portion to the app.

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# NOTE: 
# f-string print statements as shown above is a cleaner way to create print statements. 

# Scrape Mars Data: Mars Facts

# Scrape the entire table with .read_html() function
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
# Convert the DataFrame back into HTML-ready code using .to_html() function
df.to_html()

#browser.quit() 


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### JPL Space Images Featured Image

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

# ### Mars Facts

df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.head()

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'

browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles 'for' each hemisphere.
im = browser.find_by_css("a.product-item img")

for i in range(len(im)):
    hemisphere = {}

    browser.find_by_css("a.product-item img")[i].click()
    sample = browser.find_by_text("Sample")[0]
    hemisphere['link'] = sample["href"]
    hemisphere["title"] = browser.find_by_css("h2.title").text
    hemisphere_image_urls.append(hemisphere)
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()

