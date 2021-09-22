import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import numpy as np

df = pd.read_excel('BDP_500_ZINC_MATCHES.xlsx')
df_id = df.iloc[:,18]
def consult(link):
    print("this is the link")
    print(link)
    if pd.isnull(link):
        return "", 0, 0
    r = requests.get(link)
    soup = bs(r.content, features='lxml')
    counter = 0
    formula = ""
    mwt = 0
    for table_row in soup.select("table tr"):
        cells = table_row.findAll("td")
        if len(cells) > 0:
            if counter == 0:
                mwt = float(cells[3].text.strip())
                counter+=1
            elif counter == 1:
                formula = cells[0].text.strip()
                counter+=1
            else:
                break
    mydivs = soup.find("div", {"class": "panel-heading clearfix"})
    h3 = mydivs.find("h3", recursive=False)
    a = h3.find("a",recursive=False)
    item = a.text.strip()
    vendors = int(item.replace(' Total', ''))
    return formula, mwt, vendors

result = pd.Series([consult(df_id[i]) for i in range (len(df_id))])
results = pd.DataFrame(result.values.tolist(), index = result.index, columns = ['formula', 'mwt','vendors'])
df = pd.merge(df, results, right_index=True, left_index=True)

df.to_excel('BDP_ZINC_FINALIZADO.xlsx')