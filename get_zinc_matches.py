import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re
import pandas as pd
import numpy as np
from urllib.parse import quote


df = pd.read_excel('BDP_Smiles_500.xlsx')
df_id = df.iloc[:,16]

driver = webdriver.Chrome('/Users/mariaclaraotani/chromedriver')
def lookup(link):
    if pd.isnull(link):
        return []
    t = quote(link)
    URL="https://zinc.docking.org/substances/subsets/for-sale/?q="+t
    driver.get(URL)
    driver.find_element_by_xpath('/html/body/div/div/div/nav[1]/div/div/div[4]/div[3]/form/button').click()
    elems = driver.find_elements_by_partial_link_text('ZINC')
    results = []
    for elem in elems:
        link = elem.get_attribute("href")
        if "substance" in str(link):
            results.insert(0,link)
    return results

result = pd.Series([lookup(df_id[i]) for i in range (len(df_id))])
results = pd.DataFrame({'ZINC': result.values.tolist()})
df = pd.merge(df, results, right_index=True, left_index=True)
exploded = df.explode('ZINC')
exploded.to_excel('BDP_500_ZINC_MATCHES.xlsx')