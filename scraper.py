import time
import csv
import re
#import pickle use pickle for cookies

from selenium import webdriver as web
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import numpy as np
import pandas as pd
from datetime import datetime

start = datetime.now()

# NMS:  275850, RUST:  252490, STARDEW 413150, N:  230270, DEUS EX:  337000
# the next 3 lines are to get rid of the ignore-certificate-warnings
options = web.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
chrome = web.Chrome(chrome_options=options)
chrome.get('https://store.steampowered.com/app/413150/')

wait = WebDriverWait(chrome,30)
wait.until(EC.element_to_be_clickable((By.ID, 'ViewAllReviewsall'))).click()

lenOfPage = chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

reviews = []
match=False

while(match==False):
	lastCount = lenOfPage
	time.sleep(3)
	lenOfPage = chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	review_elements = chrome.find_elements_by_class_name('apphub_CardTextContent')
	if lastCount==lenOfPage or len(review_elements)==8000:
		match=True
		for i in review_elements:
			try:
				i = i.text.split('\n', 1)
				i[0] = i[0].replace('\n', ' ')
				i[1] = i[1].replace('\n', ' ')
			except IndexError:
				pass
			reviews.append(i)

df = pd.DataFrame(reviews)

df.to_csv('stardew_8k.csv', encoding='utf-8')

print datetime.now() - start

