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


# NMS:  275850, RUST:  252490, STARDEW 413150, N:  230270, DEUS EX:  337000
# note that games like Deus Ex will need to go through age verification (require cookies) 
chrome = web.Chrome()
chrome.get('https://store.steampowered.com/app/275850/')

wait = WebDriverWait(chrome,30)
wait.until(EC.element_to_be_clickable((By.ID, 'ViewAllReviewsall'))).click()

lenOfPage = chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

reviews = []
match=False
n = 0
review_page_number = 1
while(match==False):
	lastCount = lenOfPage
	time.sleep(3)
	lenOfPage = chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")	
	review_elements = chrome.find_elements_by_class_name('apphub_CardTextContent')
	if lastCount==lenOfPage or review_page_number==10:
		match=True
		for i in review_elements:
			review_page_number += 1
			i = i.text.split('\n', 1)
			i[0] = i[0].replace('\n', ' ')
			i[1] = i[1].replace('\n', ' ')
			reviews.append(i)
	# n += 1

df = pd.DataFrame(reviews)

df.to_csv('nms_clean.csv', encoding='utf-8')


'''
Things to fix:
-when people use the 'spoiler' blackout over their text-we are not caputring that text, just what is around it
the javascript element that holds this text will need to be targeted
-there seems to be a max text length in the actual dataframe (the long reviews get 'cut off')
-issues w/ page/review number

Things to add:
-we can add recommendation, hrs on record, name of user, games in user acct, how many people found the review
helpful or funny, etc..
lets target some of these and add them as well, this *should* be fairly straightforward

...? 


'''
