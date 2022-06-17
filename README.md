# Linkedin Crawler
Web Crawler to scrap profile data from Linkedin

About

The objective is to systematically visit one's connections linkedin profiles and extract data points from these pages. 
These extraced datapoints are then populated in a csv file and stored. This crawler is designed to be used for personal use. But it can be scaled up to pull large amounts of data.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Strategies

Every website has policies against bots and Linkedin has poclicies as well. This scrapper uses some ethical strategies to make sure that it does not overload the server. Each request is sent after a significant cooldown period.  

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Technicalities

The scraper make use of libraries such as selenium, regular expressions, BeautifulSoup, parsel.
Selenium helps to automate the process of scrapping. The webdriver associated with selenium runs a headless browser in the background. Selenium is also capable of running javascript in the webpages sychronously.

Dealing with lazy pagination.

This crawler first pulls the web links of connections after logging in and stores them. The connections page has a lazy pagination and hence it has to be scrapped first in order to avoid dealing with the infinite scroll every time.
Each profile is then visted sequentially with random wait period, random clicks, refresh, previous page visits in between.

Extracting html elements.

Data points in these webpges are pulled using a combination of Paresl, BeautifulSoup and regular expressions.
Parsel is a library to extract and remove data from HTML and XML using XPath and CSS selectors.


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Conclusion

This crawler 

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Disclaimer

This scrapper is to be used only for educatiional purposes and should not be used in a commercial scale as it violates Linkedin policy. Use the crawler respecting all the ethical aspects of crawling else it can get your account banned.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Bibliography

1. https://www.crummy.com/software/BeautifulSoup/bs4/doc/
2. https://www.selenium.dev/documentation/
3. https://parsel.readthedocs.io/en/latest/usage.html
4. https://docs.python.org/3/library/re.html
