"""
Standard and reliable module for starting up Selenium Webdriver, with custom user-agent and custom profiles.
"""

import os
import subprocess
import urllib
import sys

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

##    Starts the Java Standalone Selenium Server. Uses find_file to search for the server .jar file.. 

def start_selenium_server():
    seleniumserver_path = find_file(name='selenium-server-standalone-2.50.1.jar', path=os.getcwd())
    cmd = ['java', '-jar', seleniumserver_path]
    server = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)


##    Starts the Selenium Webdriver.
##    Uses broswer driver_name. Custom user-agent and profile can be passed as user_agent and profile_path, respectively.

def start_webdriver(driver_name, user_agent=None, profile_path=None):
    driver_name = driver_name.lower()
    driver = None

    if driver_name == 'htmlunit':
        while True:
            try:
                urllib.request.urlopen('http://localhost:4444/wd/hub/status')
            except urllib.error.URLError:
                start_selenium_server()
            else:
                break

        if user_agent:
            pass
        dcap = webdriver.DesiredCapabilities.HTMLUNITWITHJS
        driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                  desired_capabilities=dcap)

    if driver_name == 'firefox':
        if profile_path:
            fp = webdriver.FirefoxProfile(profile_path)
        else:
            fp = webdriver.FirefoxProfile()

        if user_agent:
            fp.set_preference('general.useragent.override', user_agent)

        driver = webdriver.Firefox(fp)

    if driver_name == 'chrome':
        opt = webdriver.chrome.options.Options()
        if user_agent:
            opt.add_argument('user-agent={user_agent}'.format(user_agent=user_agent))
        if profile_path:
            opt.add_argument('user-data-dir={profile_path}'.format(profile_path=profile_path))

        if sys.platform.startswith('win'):
            chromedriver_path = find_file(name='chromedriver.exe', path=os.getcwd())
        elif sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
            chromedriver_path = find_file(name='chromedriver', path=os.getcwd())
            
        driver = webdriver.Chrome(chromedriver_path, chrome_options=opt)

    if driver_name == 'phantomjs':
        dcap = DesiredCapabilities.PHANTOMJS
        if user_agent:
            dcap["phantomjs.page.settings.userAgent"] = user_agent

        phantomjs_path = find_file(name='phantomjs.exe', path=os.getcwd())
        driver = webdriver.PhantomJS(phantomjs_path, desired_capabilities=dcap)

    return driver
