import time
import csv
import re
#import pickle use pickle for cookies

from selenium import webdriver as web
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

import numpy as np
import pandas as pd
from datetime import datetime

start = datetime.now()

caps = DesiredCapabilities.FIREFOX
caps["marionette"] = True
caps["binary"] = "/Applications/Firefox.app/Contents/MacOS/firefox-bin"

driver = web.Firefox(capabilities=caps)
driver.get('https://store.steampowered.com/app/413150')

wait = WebDriverWait(driver,30)
wait.until(EC.element_to_be_clickable((By.ID, 'ViewAllReviewssummary'))).click()

len_of_page = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

reviews = []
author = []
author_game_count = []
hours = []

match=False
while(match==False):
    last_count = len_of_page
    time.sleep(3)
    len_of_page = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    review_elements = driver.find_elements_by_class_name('apphub_CardTextContent')
    review_authors = driver.find_elements_by_class_name('apphub_CardContentAuthorBlock.tall')
    hours_on_record = driver.find_elements_by_class_name('hours')
    if last_count==len_of_page or len(review_elements)==1000:
        match=True
        for i in hours_on_record:
            hours.append(i.text)
        for i in review_authors:
            i = i.text.split('\n', 1)
            i[0] = i[0].replace('\n', ' ')
            i[1] = i[1].replace('\n', ' ')
            author.append(i[0])
            author_game_count.append(i[1])
        for i in review_elements:
            i = i.text.split('\n', 1)
            i[0] = i[0].replace('\n', ' ')
            i[1] = i[1].replace('\n', ' ')
            reviews.append(i)

df = pd.DataFrame(reviews)
df['author'] = author
df['author_game_count'] = author_game_count
df['hours_on_record'] = hours
df.to_csv('star1000test.csv', encoding='utf-8')

print datetime.now() - start
