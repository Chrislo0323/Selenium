import pandas as pd
import numpy as np
import os
import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
from selenium import webdriver
import seaborn as sns
import time

os.chdir('C:/Users\Chris\OneDrive\School\python club')

tickers = 'AAPL'
url = f'https://finance.yahoo.com/quote/{tickers}/financials'
headers = {'User-Agent': 'Mozilla/5.0'}

# open the puppeteered browser 
driver = webdriver.Edge()
driver.get(url)
# in the url we got, find element of type button that contains text 'Quarterly'
# use selenium method by.By
# we're looking up text using XPATH method
button = driver.find_element(webdriver.common.by.By.XPATH, '//button[text()="Quarterly"]')
button.click()
time.sleep(5)
# get the source code using selenium webdriver
response = driver.page_source
soup = bs(response, 'html.parser')

table = soup.find(class_= 'tableContainer')
rows = table.find_all(class_ = 'row')
columns = rows[0].find_all(class_ = 'column')

rows_list = []
for row in rows:
    values = []
    for cell in row:
        value = cell.text
        values.append(value)
    rows_list.append(values)


df_inc = pd.DataFrame(rows_list)
df_inc.columns = df_inc.loc[0,:]
df_inc.drop('TTM ', axis= 1, inplace = True )
df_inc = df_inc.iloc[1:-2,:]
df_inc['ticker'] =  tickers
#df_inc.set_index('ticker', drop =True, inplace = True)
df_inc.replace(',','', regex = True, inplace = True)
df_inc.replace('--', np.nan, regex = True, inplace = True)
df_inc = df_inc.astype(float, errors = 'ignore')
df_inc.rename(columns = {df_inc.columns[0]:'Income statement entry'}, inplace = True)

y = df_inc.loc[df_inc['Income statement entry'] =='  Total Revenue',
               df_inc.columns[2:-1]].values[0]
y = y/1e6 # convert thousands to billions
y = np.flip(y)
x = df_inc.columns[2:-1]
x = np.flip(x)
plt.plot(x,y)


