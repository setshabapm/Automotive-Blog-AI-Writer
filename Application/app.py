"""pip install beautifulsoup4
pip install lxml
pip install requests
pip install webdriver_manager
pip install selenium
pip install -q -U google-generativeai"""


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from time import sleep
import pathlib
import textwrap
import pickle
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

# write list to binary file
def write_list(a_list, file_name):
    # store list in binary file so 'wb' mode
    with open(file_name, 'wb') as fp:
        pickle.dump(a_list, fp)
        print('Done writing list into a binary file')

# Read list to memory
def read_list(file_name):
    # for reading also binary mode is important
    with open(file_name, 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list
    


GOOGLE_API_KEY='AIzaSyCM6uvTNlCY3yQOj89VYxeTXSnn-19Tns0'

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

# Login credentials
USERNAME = "setshaba-mashigo"
PASSWORD = "$set-083S"

articles = read_list('article_db')

# Pages of interest
url_login = 'https://motorpress.co.za/'
url_articles = 'https://motorpress.co.za/articles'

# Setup headless web driver
#options = Options()
#options.add_argument('--headless=new')
#options.add_argument('user-agent=fake-useragent')

# Auto-install web driver if not already present
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Login
username_id="email"
password_id="password"

while True:
    if driver.getCurrentUrl() != url_articles:
        driver.get(url_login)
        driver.find_element(By.ID, username_id).send_keys(USERNAME)
        driver.find_element(By.ID, password_id).send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, ("button[type='submit']")).click()

        sleep(1)

    if driver.getCurrentUrl() == url_articles:
        time_release = driver.find_element(By.CSS_SELECTOR,"article .font-bold").text
        article_title = driver.find_element(By.CSS_SELECTOR,"article h2").text

        print(time_release)
        print(article_title)

        print('List is', articles)

        if article_title not in articles:
            article_link = driver.find_element(By.CSS_SELECTOR,"article a").get_attribute('href')

            driver.get(article_link)

            articles.append(article_title)

            write_list(articles, 'article_db')

            sleep(1)

            print(article_link)

            driver.find_element(By.CSS_SELECTOR,"div.text-sm.text-gray-500.flex.items-center.w-full.divide-x.divide-primary div.px-2").text

            category = driver.find_element(By.CSS_SELECTOR,"div.text-sm.text-gray-500.flex.items-center.w-full.divide-x.divide-primary div.px-2").text

            soup = BeautifulSoup(driver.page_source, 'lxml')

            press_release = soup.find(class_="prose max-w-none").get_text()

            Markdown("Category: "+category)
            Markdown(press_release)

            response = model.generate_content("Using as much of your own interpretation and language, write a brief 200 word automotive industry news report of the following press release: "+press_release)

            Markdown(response.text)

            driver.get(url_articles)

            sleep(300)