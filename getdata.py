import pandas as pd
# from bdshare import get_hist_data
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from getshare import get_hist_data

def get_hist_data(start=None, end=None, code='All Instrument'):
    try:
        # r = requests.get(url=vs.DSE_URL+vs.DSE_DEA_URL, params=data)
        pageUrl = f"https://dsebd.org/day_end_archive.php?startDate={start}&endDate={end}&inst={code}&archive=data"
        pageUrl2 = f"https://dse.com.bd/day_end_archive.php?startDate={start}&endDate={end}&inst={code}&archive=data"
        r = requests.get(url=pageUrl)
        if r.status_code != 200:
            r = requests.get(url=pageUrl2)
    except Exception as e:
            print(e)
    #soup = BeautifulSoup(r.text, 'html.parser')
    soup = BeautifulSoup(r.content, 'html5lib')
    quotes = []  # a list to store quotes
    table = soup.find('table', attrs={
                      'class': 'shares-table'
                      })
    # print(table)
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        quotes.append({'date': cols[1].text.strip().replace(",", ""),
                       'symbol': cols[2].text.strip().replace(",", ""),
                       'ltp': cols[3].text.strip().replace(",", ""),
                       'high': cols[4].text.strip().replace(",", ""),
                       'low': cols[5].text.strip().replace(",", ""),
                       'open': cols[6].text.strip().replace(",", ""),
                       'close': cols[7].text.strip().replace(",", ""),
                       'ycp': cols[8].text.strip().replace(",", ""),
                       'trade': cols[9].text.strip().replace(",", ""),
                       'value': cols[10].text.strip().replace(",", ""),
                       'volume': cols[11].text.strip().replace(",", "")
                       })
    df = pd.DataFrame(data=quotes,index= None)
    # print(df['close'])
    return df

def parsedata(ticker,start_date,end_date):
    # df = pd.read_csv('./yearwise/Dhaka-Stock-Exchange-DSE-'+year+'.csv')
    df=pd.read_csv('./yearwise/Dhaka-Stock-Exchange-DSE-2018.csv')
    # print(df)
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')      
    # Set the 'date' column as the index
    df.set_index('date', inplace=True)
    stock_data = df[(df['symbol'] == ticker) & (df.index >= start_date) & (df.index <= end_date)]
    return stock_data


def parsedata2(ticker,start_date,end_date):
    # df = pd.read_csv('./yearwise/Dhaka-Stock-Exchange-DSE-'+year+'.csv')
    df = get_hist_data(start_date,end_date,ticker)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')      
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    df = df[(df['symbol'] == ticker) & (df.index >= start_date) & (df.index <= end_date)]
    return df

