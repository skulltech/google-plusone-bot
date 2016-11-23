import csv
import os
import sys
import time
from configparser import ConfigParser

import selenium.common.exceptions as SE
from wdstart import start_webdriver
from selenium import webdriver

BASEHTML = r'''
<html>
  <head>
    <title>Google +1 Bot</title>
    <link rel="canonical" href="{url}" />
    <script src="https://apis.google.com/js/platform.js" async defer>
    </script>
    <script>
      {{"parsetags": "explicit"}}
    </script>
  </head>
  <body>
    <div id="content">
      <div class="g-plusone"></div>
    </div>
    <script>
      gapi.plusone.go("content");
    </script>
  </body>
</html>
'''

PROFILE = os.getenv('LOCALAPPDATA') + '\\Google\\Chrome\\User Data'
sleep_time = 6


def save_webpage(url):
    html = BASEHTML.format(url=url)

    with open('plusone.html', mode='w') as f:
        f.write(html)

def login_google(driver, email, password):
    driver.get('https://accounts.google.com/login')

    input_email = driver.find_element_by_name('Email')
    input_email.send_keys(email)
    input_email.submit()
    time.sleep(sleep_time)
    
    input_passwd = driver.find_element_by_name('Passwd')
    input_passwd.send_keys(password)
    input_passwd.submit()

def main():
    config = ConfigParser()
    config.read('config.ini')

    if not bool(len(config) - 1):
        print('config.ini file not present or correctly configured!')

    driver = start_webdriver(driver_name=config['SETTINGS']['BrowserName'])
    login_google(driver, email=config['SETTINGS']['Email'], password=config['SETTINGS']['Password'])
    file_url = 'file:///' + os.getcwd() + '\\plusone.html'

    with open('url.csv', mode='r') as f:
        url_csv = csv.reader(f)

        for row in url_csv:
            print('+1-ing {url} ... '.format(url=row[0]), end='')
            
            save_webpage(row[0])
            driver.get(file_url)
            time.sleep(sleep_time)

            button_frame = driver.find_elements_by_tag_name('iframe')[0]
            driver.switch_to.frame(button_frame)

            button = driver.find_element_by_id('button')
            state = button.get_attribute('aria-pressed')

            button.click()
            time.sleep(sleep_time)
            print('Done!')
                      

    driver.quit()
    print('\nAll Tasks Done!')


if __name__ == '__main__':
    main()