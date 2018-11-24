import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests

# Use Chrome driver and pass the string chrome when creating the Browser instance:
def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Define a scrape funtion with url as a parameter
def scrape(url):
    browser = init_browser()

    # Visit the specified url website
    browser.visit(url)

    # Introduce an intentional delay or lag in the scraper to wait 5 second before making the next request
    time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph

browser = init_browser()

# Visit www.mars.nasa.gov/news
url_mars = "https://mars.nasa.gov/news/"
browser.visit(url_mars)

# Introduce an intentional delay or lag in the scraper to wait 5 second before making the next request
time.sleep(5)

# Scrape page into Soup
html = browser.html
soup = bs(html, "html.parser")

# Create a dictionary to store scrape data
articles = {}

# Get the news title
news_title = soup.find('div', class_='content_title').text

# Get the news paragraph
news_p = soup.find('div', class_='article_teaser_body').text

# Store data in a dictionary
articles = {
     "news title": news_title,
     "news paragraph": news_p
 }


 # JPL Mars Space Images - Featured Mars Image

# Visit www.mars.nasa.gov/news
url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url_jpl)

time.sleep(5)

# Scrape page into Soup
html = browser.html
soup_jpl = bs(html, "html.parser")

# Get full image for the current featured Mars image and assign it to a variable
base_url = "https://www.jpl.nasa.gov" # get the base url
image = soup_jpl.find('a', {'id':'full_image','data-fancybox-href': True}).get('data-fancybox-href')
featured_image_url = base_url+image
print(featured_image_url)

# Mars Weather

# Visit the Mars Weather twitter account
url_tweet = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_tweet)

time.sleep(5)

# Scrape page into Soup
html = browser.html
soup_tweet = bs(html, "html.parser")

# Get the news title
mars_weather = soup_tweet.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

print(mars_weather)

# Mars Facts

# Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet
url_facts = "http://space-facts.com/mars/"
browser.visit(url_facts)

time.sleep(5)

# Use Pandas to scrape the table
facts_df = pd.read_html(url_facts)

# Convert the data into a dataframe
mars_facts_df = pd.DataFrame(facts_df[0])

# Rename column and set index
mars_facts_df.columns = ['Description','Data']
mars_facts_new = mars_facts_df.set_index("Description")
print(mars_facts_new)

# Convert the data to a HTML table string
mars_facts_html = mars_facts_new.to_html(classes='marsdata')
mars_facts_table = mars_facts_html.replace('\n', ' ')
print(mars_facts_table)

# Mars Hemispheres

# Visit the USGS Astrogeology to get high resolution images of Mars hemisphere
url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url_hemisphere)

# Scrape page into Soup
html = browser.html
soup_hemisphere = bs(html, "html.parser")

# Get the div element that holds the images and titles.
img_title = soup_hemisphere.find('div', class_='collapsible results')

# Initialize a list to contain dictionary storing image and hemisphere title
hemisphere_image_urls = []

# Loop through tags and load the data to the dictionary
for i in range(len(img_title.find_all("div", class_="item"))):
        time.sleep(5)
        img = browser.find_by_tag('h3')
        img[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find("h2", class_="title").text
        div = soup.find("div", class_="downloads")
        for li in div:
            link = div.find('a')
        url = link.attrs['href']
        hemisphere_dict = {
                'title' : title,
                'img_url' : url
            }
        hemisphere_image_urls.append(hemisphere_dict)
        browser.back()

print(hemisphere_image_urls)

# Close the browser after scraping
browser.quit()



print(articles)
