from selenium import webdriver
import parameters
from parsel import Selector
import re
import csv
from bs4 import BeautifulSoup as bs
import time
import os
import random
import connection_list_scrapper

#Results Filename
results_filename = 'results.csv'

def tag_remover(raw_html):
    if raw_html is not None:
        cleaner = re.compile('<.*?>')
        return re.sub(cleaner, '', raw_html)
    else:
        return raw_html


def href_link_filter_from_page_source(page_source, filter_re):
    tag = str(re.findall(filter_re, page_source))
    href_filter = re.compile('href=".*?"')
    tag_filtered = str(re.findall(href_filter, tag))
    quotes_filter = re.compile('".*?"')
    link_final = str(re.findall(quotes_filter, tag_filtered))
    link_final = link_final.replace('[', '')
    link_final = link_final.replace(']', '')
    link_final = link_final.replace('"', '')
    link_final = link_final.replace("'", "")
    url_final = 'https://www.linkedin.com'
    url_final = url_final + link_final

    return url_final

def start_driver():
    print('Starting web driver.\n')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(parameters.driver_location)

    return driver

def create_csv_file():
    # Creating csv file
    with open(results_filename, 'w') as csv_file:
        filewriter = csv.writer(csv_file, delimiter=',')
        filewriter.writerow(
            ['Name', 'Job Position', 'Company name', 'Location', 'Linkedin Profile URL', 'Phone', 'Email address'])
    csv_file.close()

def load_links():
    # loading connections links from text file

    file = open('connections.txt', 'r')
    contents = file.readlines()
    for i in range(len(contents)):
        contents[i] = contents[i].strip()
    print('Connection list loaded\n')

    return contents

def run_crawler(driver, contents):

    for i in range(len(contents)):
        try:
            print(i + 1)

            driver.get(contents[i])

            # NAME EXTRACT

            page = driver.page_source
            soup = bs(page, features='lxml')
            name = str(soup.find_all('h1', class_="top-card-layout__title")[0])
            name = tag_remover(name)
            if name is not None:
                name = name.strip()

            # JOB POSITION EXTRACT

            job_position = str(soup.find_all('h2', class_="top-card-layout__headline")[0])
            job_position = tag_remover(job_position)
            if job_position is not None:
                job_position = job_position.strip()

            # COMPANY

            try:
                company = str(soup.find_all('span', class_="top-card-link__description")[0])
                company = tag_remover(company)
                if company is not None:
                    company = company.strip()
            except:
                company = 'not available'

            # Location
            try:
                location = str(soup.find_all('span', class_="top-card__subline-item")[0])
                location = tag_remover(location)
                if location is not None:
                    location = location.strip()
            except:
                location = 'not available'

            print(name, job_position, location, company, contents[i], sep='\n')
            print('\n')

            with open(results_filename, 'a+', newline='', encoding='utf-8') as csv_file:
                filewriter = csv.writer(csv_file, delimiter=',')
                filewriter.writerow([name, job_position, company, location, contents[i]])
            csv_file.close()


        except Exception as e:

            print(e)  # printing the error in the try part.
            print('network slow\n')

            try:
                driver.refresh()
                print('page refreshed\n')
            except Exception as f:
                print('Unable to refresh the page.\n')
                print(f)
            i -= 1

        time.sleep(random.uniform(7, 13))

    driver.quit()

if __name__ == '__main__':

    connection_list_scrapper.run_scrapper()

    driver = start_driver()

    contents = load_links()

    run_crawler(contents, driver)
