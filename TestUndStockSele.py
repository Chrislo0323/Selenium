from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def convert_values(data):
    data = str(data).replace('$', '').replace('%', '')
    try:
        if data.endswith('M'):
            return float(data[:-1]) * 1e6
        elif data.endswith('B'):
            return float(data[:-1]) * 1e9
        elif data.endswith('%'):
            return float(data[:-1]) / 100
        else:
            return float(data)
    except ValueError:
       
        pass


def USscrapin(tickers):
    url = 'https://understandstock.com/users/sign_in'
    driver = webdriver.Firefox()
    driver.get(url)

    # Login
    username = "Christopherlopez1013@gmail.com"
    password = "Investor0323$"
    username_field = driver.find_element(By.ID, 'user_email')
    password_field = driver.find_element(By.ID, 'user_password')
    username_field.send_keys(username)
    password_field.send_keys(password)
    
    loginButton = driver.find_element(webdriver.common.by.By.XPATH, '/html/body/div[1]/div[2]/div/div/div/form/div[4]/input')
    loginButton.click()
    time.sleep(5)
    
    dfs =[]
    
    for ticker in tickers:
        # Search for ticker
        tickerSearch = driver.find_element(By.ID, 'query')
        tickerSearch.send_keys(ticker)
        tickerSearch.send_keys(Keys.RETURN)
        time.sleep(10)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'overflow-x-auto')))
    
        # quarterly button
        quarterlyButton = driver.find_element(By.XPATH, '//a[text()="Quarterly"]')
        quarterlyButton.click()
    
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
    
        # table data
        response = driver.page_source
        soup = bs(response, 'html.parser')
        table = soup.find_all('table')[1]  
        df_temp = pd.read_html(str(table))[0]
        df_temp = df_temp.set_index('Concept')
        df_temp = df_temp.applymap(convert_values)
        df_temp['ticker'] = ticker
        dfs.append(df_temp)
         
    driver.quit()
    return dfs 

# example
tickers = ['mcd','bx', 'googl']
dfs = USscrapin(tickers)

plt.figure(figsize=(28, 8))
for df in dfs:
    label_value = str(df.iloc[0]['ticker']) 
    sns.lineplot(x = np.flip(df.columns), y = np.flip(df.loc['Revenue']), label= label_value)
plt.legend(tickers)
plt.xlabel('Date')
plt.ylabel('Total Revenue (Billions)')
plt.xticks(rotation = 90)
plt.title('Total Revenue Over Time for Selected Companies')
plt.show()