from selenium import webdriver
import time
import re
import parameters


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
    link_final = link_final.split(',')
    link_final_1 = []
    url_final = 'https://www.linkedin.com'
    for k in range(len(link_final)):
        link_final[k] = link_final[k].strip()
        link_final[k] = url_final + link_final[k]
        if link_final[k] not in link_final_1:
            link_final_1.append(link_final[k])

    return link_final_1

def run_driver():
    print('Starting web driver.\n')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(parameters.driver_location, options=chrome_options)
    #driver.maximize_window()
    print('Webdriver ready\n')
    return driver

def run_scrapper():
    driver = run_driver()

    # Setting Implicit wait.
    driver.implicitly_wait(3600)

    driver.get('https://www.linkedin.com')

    print('Logging in.\n')
    # login
    username = driver.find_element_by_name('session_key')
    username.send_keys(parameters.linkedin_username)
    password = driver.find_element_by_name('session_password')
    password.send_keys(parameters.linkedin_password)
    log_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')
    log_in_button.click()
    print('Logged in.\n')

    #go to lazy load connections page
    driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')

    #code snippet to scroll till the end

    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False

    print('scrolling started\n')

    j = 1
    for i in range(3):
        print('try ' + str(i+1) + '\n')
        while(match==False):
            try:
                print('scrolling ' + str(j) + ' time...\n')
                lastCount = lenOfPage
                time.sleep(5)
                lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount == lenOfPage:
                    match = True
                j += 1

            except Exception as e:

                print(e)  # Printing the reason for the error in try part.
                print('sleeping for 30s')
                time.sleep(30)

            # Saving the current connections if j is a multiple of 10
            if j % 10 == 1:

                print('Saving current connections.\n')
                # code snippet to get connection link from the list of connections

                page1 = driver.page_source

                # Finding all connection links in the page source

                connection_link = re.compile('<a data-control-name="connection_profile".*?>')
                links = href_link_filter_from_page_source(page1, connection_link)

                # saving list of links to txt file

                print('No.of links = ' + str(len(links)))
                with open('connection_links profile 3.txt', 'w') as txt_file:
                    for k in links:
                        txt_file.write(k + '\n')

                txt_file.close()

                print('Current connections saved.\n')

        time.sleep(60)

        print('scrolling completed -- trial ' + str(i+1) + '\n')

    #code snippet to get connection link from the list of connections

    page1 = driver.page_source

    #saving page source to txt file

    with open('page source profile 3.txt', 'w', encoding='utf-8') as txt:
        txt.write(page1)
    txt.close()
    print('page source saved\n')

    # Finding all connection links in the page source

    connection_link = re.compile('<a data-control-name="connection_profile".*?>')
    links = href_link_filter_from_page_source(page1, connection_link)

    #saving list of links to txt file

    print('No.of links = ' + str(len(links)))
    with open('connection_links profile 3.txt', 'w') as txt_file:
        for i in links:
            txt_file.write(i + '\n')

    txt_file.close()
    print('connections links saved\n')

    # logging out

    print('Logging out.\n')

    driver.get('https://www.linkedin.com/m/logout/')
    driver.quit()


if __name__ == '__main__':
    run_scrapper()
