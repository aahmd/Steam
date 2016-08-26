import time
import csv
import re
import pickle

from selenium import webdriver as web
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import numpy as np
import pandas as pd


# NMS:  275850, RUST:  252490, STARDEW 413150, N:  230270, DEUS EX:  337000
# note that games like Deus Ex will need to go through age verification 
chrome = web.Chrome()
chrome.get('https://store.steampowered.com/app/275850/')

# why use a wait?
wait = WebDriverWait(chrome,30)
wait.until(EC.element_to_be_clickable((By.ID, 'ViewAllReviewsall'))).click()

lenOfPage = chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

match=False
reviews = []
while(match==False):
	lastCount = lenOfPage
	time.sleep(3)
	lenOfPage = chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	review_elements = chrome.find_elements_by_class_name('apphub_CardTextContent')


	for i in review_elements:
		reviews.append(i.text.split('\n', 1))

	if lastCount==lenOfPage or len(reviews)==1000:
		match=True

# dates = []
# revs = []

# for i in reviews:
# 	dates.append(i[0])
# 	revs.append(i[1])


# print revs
# dates = [item for item in reviews]
# revs = [item[1:] for item in reviews]

df = pd.DataFrame(reviews)

# df = pd.DataFrame({  "Date"  : dates,
                     # "Reviews" : revs})

df.to_csv('nms_cl.csv', encoding='utf-8')