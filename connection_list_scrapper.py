from selenium import webdriver
import parameters
from parsel import Selector
import re
import csv
from bs4 import BeautifulSoup as bs

# Filename to store connections links
file_name = ''

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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(parameters.driver_location, options=chrome_options)

    return driver

def create_csv_file():
    with open('result.csv', 'w') as csv_file:
        filewriter = csv.writer(csv_file, delimiter=',')
        filewriter.writerow(
            ['Name', 'Job Position', 'Company name', 'Location', 'Linkedin Profile URL', 'Phone', 'Email address'])
    csv_file.close()

def save_file(final_connections):
    with open(file_name, 'w') as text_file:
        for x in final_connections:
            text_file.write(x + '\n')

def run_scrapper():

    driver = start_driver()

    driver.get('https://www.linkedin.com')

    # login
    username = driver.find_element_by_name('session_key')
    username.send_keys(parameters.linkedin_username)
    password = driver.find_element_by_name('session_password')
    password.send_keys(parameters.linkedin_password)
    log_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')
    log_in_button.click()

    # go to admin's profile page
    page = driver.page_source
    profile_pic_tag = re.compile('<a data-control-name="identity_profile_photo".*?>')
    profile_url = href_link_filter_from_page_source(page, profile_pic_tag)

    driver.get(profile_url)

    # go to connections page
    page_profile = driver.page_source
    filter_connections = re.compile('<a data-control-name="topcard_view_all_connections".*?>')
    connections_url = href_link_filter_from_page_source(page_profile, filter_connections)
    connections_url_unchanged = connections_url

    driver.get(connections_url)
    connections_list_page = driver.page_source
    connection_link_filter = re.compile('<a data-control-id.*? data-control-name="search_srp_resul'
                                                                 't" .*? class="search-result__result-link ember-view">')
    connections_links = re.findall(connection_link_filter, connections_list_page)

    j = 2

    create_csv_file()

    final_connections = []

    while len(connections_links) is not 0:

        for i in range(len(connections_links)):
            href = re.compile('href=".*?"')
            tag_filtered = str(re.findall(href, connections_links[i]))
            quotes = re.compile('".*?"')
            link = str(re.findall(quotes, tag_filtered))
            link = link.replace('[', '')
            link = link.replace(']', '')
            link = link.replace('"', '')
            link = link.replace("'", "")
            url = 'https://www.linkedin.com'
            connections_links[i] = url + link
            if connections_links[i] not in final_connections:
                final_connections.append(connections_links[i])

        print(final_connections)
        print(len(final_connections))

        connections_url = connections_url_unchanged
        connections_url = connections_url + '&page=' + str(j)
        print(j)

        j += 1
        driver.get(connections_url)
        connections_list_page = driver.page_source
        connection_link_filter = connection_link_filter = re.compile('<a data-control-id.*? data-control-name="search_srp_resul'
                                                                     't" .*? class="search-result__result-link ember-view">')
        connections_links = re.findall(connection_link_filter, connections_list_page)

    save_file(final_connections)

    driver.quit()


if __name__ == '__main__':
    run_scrapper()