#dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time

#fxn to initialize splinter
def init_browser():
    executable_path = {'executable_path': 'C:/Users/maria/Documents/2020 GT data analytics/chromedriver_win32/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

#begin scrape fxn
def scrape():
    browser = init_browser()
    
    #1) NASA
    #visit NASA mars site, delay 5 seconds before scraping to allow page to load
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    time.sleep(5)

    #create beautifulsoup object
    nasa_html = browser.html
    nasa_soup = bs (nasa_html, 'lxml')

    #scrape top headline & description
    news_h = nasa_soup.find_all("div", class_= "content_title")[1].text.strip()
    news_p = nasa_soup.find("div", class_= "article_teaser_body").text.strip()


    #2) JPL
    #visit JPL mars space image site
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit (jpl_url)

    #create another beautifulsoup object
    jpl_html = browser.html
    jpl_soup = bs (jpl_html, 'lxml')
    
    #scrape link of featured image on JPL site
    jpl_dec = jpl_soup.find ('a', class_='button fancybox')['data-fancybox-href']
    jpl_link = f"https://www.jpl.nasa.gov{jpl_dec}"


    #3) twitter
    #visit mars weather twitter account, delay 10 seconds before scraping to allow page to load
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit (twitter_url)
    time.sleep(10)

    #create another beautifulsoup object
    twitter_html = browser.html
    twitter_soup = bs (twitter_html, 'lxml')

    #scrape most recent weather tweet
    twitter_weather = twitter_soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').\
                                   find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").\
                                   text.strip()


    #4) mars facts
    #define mars fact site
    fact_url = "https://space-facts.com/mars/"

    #scrape w/ pandas, display dataframe
    fact_table = pd.read_html (fact_url)
    fact_df = fact_table[0]

    #label columns, set description as index
    fact_df.columns = ["Description", "Values"]
    fact_df = fact_df.set_index (['Description'])

    #convert to html table string w/ pandas, export
    fact_html = fact_df.to_html()
    fact_html = fact_html.replace('\n', '')


    #5) USGS images
    #visit USGS astrogeology site, delay 5 seconds before scraping to allow page to load
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit (usgs_url)
    time.sleep(5)

    #create another beautifulsoup object
    usgs_html = browser.html
    usgs_soup = bs (usgs_html, 'lxml')

    #create list for mars hemispheres, site titles
    hemi_links = []
    hemi_titles = []

    #search for all link descriptions
    hemi_results = usgs_soup.find_all ('div', class_= "description")

    #loop through results, pull corresponding links & titles
    for result in hemi_results:
        info = result.find ('a', class_= "itemLink product-item")
        link = info['href']
        title = info.find ('h3').text.strip()
        
        hemi_links.append (f"https://astrogeology.usgs.gov/{link}")
        hemi_titles.append (title)

    #create blank list for dict items
    hemi_list = []

    #visit each site, scrape link to full jpgs
    for x in range(len(hemi_links)):
        browser.visit (hemi_links[x])
        hemi_html = browser.html
        hemi_soup = bs (hemi_html, 'lxml')
        
        img_url = hemi_soup.find ('li').find ('a')['href']
        
        #assemble title & url dict entries, append to list
        hemi_item = {'title': hemi_titles[x],
                    'img_url': img_url}
        
        hemi_list.append (hemi_item)

    #close browser after scraping
    browser.quit()

    #list & return results
    mars_data = {"news_headline": news_h,
                 "news_description": news_p,
                 "jpl_link": jpl_link,
                 "table_html": fact_html,
                 "twitter_weather": twitter_weather,
                 "hemispheres": hemi_list}

    return mars_data