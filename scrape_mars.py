from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Get the latest News title and paragraph
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(.25)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")


    title = soup.find("div", class_="content_title").get_text()
    news_p = soup.find("div", class_="rollover_description_inner").get_text()

    # Get the latest featured image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    
    time.sleep(.25)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    a = soup.find("footer").find("a")
    if a.has_attr('data-fancybox-href'):
       relative_url = a['data-fancybox-href'] 
    
    featured_image_url = "https://www.jpl.nasa.gov" + relative_url
    
    # Get the Mars Weather report 
    url = "https://twitter.com/MarsWxReport"
    browser.visit(url)
    
    time.sleep(.25)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    weather_rs = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    
    tweets = []
    for w in weather_rs:
        tweet = w.get_text()
        if "InSight" in tweet:
            tweets.append(tweet)
    mw = tweets[0].replace('\n', ' ').replace('Insight s', 'S')
    mars_weather = mw.split('pic', 1)[0]
    
    # Get Mars Facts
    
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    
    time.sleep(.25)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    
    t = soup.find("table") 
    mars_stuff = t.find_all("span", class_="mars-s")
    
    mars_dict = {"Diameter": mars_stuff[0].get_text(),
                 "Mass" : mars_stuff[1].get_text(),
                 "Moons" : mars_stuff[2].get_text(),
                 "DistancefromSun" : mars_stuff[3].get_text(),
                 "LengthofYear" : mars_stuff[4].get_text(),
                 "Temperature" : mars_stuff[5].get_text()}
                 
    # Store Hemisphere images
    
    hemisphere_image_urls = [
        {"title" : "Cerberus Hemisphere", "img_url" : "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title" : "Schiaparelli Hemisphere", "img_url" : "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title" : "Syrtis Major Hemisphere", "img_url" : "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
        {"title" : "Valles Marineris Hemisphere", "img_url" : "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"}    
    ]
    
    # Store Mars data in a dictionary
    # Store data in a dictionary
    mars_data = {
        "newstitle": title,
        "news_p": news_p,
        "featured_img": featured_image_url,
        "mars_weather": mars_weather,
        "mars_dimensions" : mars_dict,
        "hemisphere_images" : hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
