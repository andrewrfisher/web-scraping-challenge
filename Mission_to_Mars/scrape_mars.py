#exicutable path
#/Users/andrewfisher/.wdm/drivers/chromedriver/mac64/89.0.4389.23/chromedriver

#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd

#site navigation
executable_path = {'executable_path': '/Users/andrewfisher/.wdm/drivers/chromedriver/mac64/89.0.4389.23/chromedriver'}
browser = Browser("chrome", **executable_path, headless=False)

#create a dictionary that can be imported into Mongo
mars_info={}

#def function from first part of HW for Mars News Title and Text
#MARS NEWS

def srape_mars_news ():
    try:

        # URL of page to be scraped
        url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

        # visit URL
        browser.visit(url)

        #HTML object
        html = browser.html

        #parse HTML with BS
        soup= BeautifulSoup(html, "html.parser")

        # Retrieve the parent tags for all articles
        results = soup.find_all('article')

        # loop over results to get article data
        for article in results:
    
            # scrape the article title 
            title = article.find('div', class_='content_title').text
    
            # scrape the article text
            teaser_text = article.find('div', class_='article_teaser_body').text
    
            # Dictionary entry from MARS NEWS
            mars_info['news_title'] = title
            mars_info['news_paragraph'] = teaser_text

        return mars_info
    
    finally:

        browser.quit()  

#MARS IMAGE

def scrape_mars_image ():

    try:

        #URL of image page
        image_url ='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

        #visit URL
        browser.visit(image_url)

        #HTML Object
        html_image = browser.html

        #Parse HTML with BS
        soup = BeautifulSoup(html_image, 'html.parser')

        #Retrieve parent tag for all images
        image_url = soup.find('img', class_='headerimage')['src']

        #add image_url to link from HW assignment to get jpg img and featured_image_url
        featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + image_url

        # Display full link to featured image
        featured_image_url 

        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url 

        return mars_info
    
    finally:

        browser.quit()

def scrap_mars_facts ():

    try:

        #URL of facts
        facts_url = 'https://space-facts.com/mars/'

        #visit URL
        browser.visit(facts_url)   
        
        #pandas read_html
        mars_data = pd.read_html(facts_url)

        #convert to DataFrame so we can see the data clearly
        mars_df= pd.DataFrame(mars_data[0])
        mars_df     

        #assign columns to df
        mars_df.columns = ['Description', 'Value']

        #set index to description
        mars_df.set_index('Description', inplace=True)      

        # Save html code to folder Assets
        data = mars_df.to_html()

        # Dictionary entry from MARS FACTS
        mars_info['mars_facts'] = data

        return mars_info

#MARS HEMISPHERE

def scrape_mars_hemisphere ():
    
    try:

        #URL of image page
        hemisphere_url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

        #visit URL
        browser.visit(hemisphere_url)

        #HTML Object
        html_hemisphere = browser.html

        #Parse HTML with BS
        soup = BeautifulSoup(html_hemisphere, 'html.parser')

        #mars hemisphere empty list to contain all images
        mars_hem = []

        #set up variables
        products = soup.find('div', class_='result-list')
        hemispheres = products.find_all('div', class_='item')

        #for loop so it runs through all hems and allows us to define more variables
        for hemisphere in hemispheres:
            title = hemisphere.find('h3').text
            #get rid of "enhanced in each title"
            title = title.replace("Enhanced", "")
            hem_link = hemisphere.find('a')['href']
            image_link = 'https://astrogeology.usgs.gov/' + hem_link
    
                #go into this link using browser
            browser.visit(image_link)
            hem_html = browser.html
            soup=BeautifulSoup(hem_html, "html.parser")
            #now that we're on the page we want, let's find the sample link
            sample_img = soup.find('div', class_='downloads')
            sample_img_url = sample_img.find('a')['href']
    
            #create dictionary with the above and append it to empty list mars_hem
            mars_hem.append({'Title': title, 'Image URL': sample_img_url})

        #add to dictionary
        mars_info["mars_hemisphere_urls"] = mars_hem

        #return mars_info dict
        return mars_info
    
    finally:
        browser.quit()




