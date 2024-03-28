import pandas as pd

def parsedata(year,ticker,start_date,end_date):
    df = pd.read_csv('./yearwise/Dhaka-Stock-Exchange-DSE-'+year+'.csv')
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')      
    # Set the 'date' column as the index
    df.set_index('date', inplace=True)
    stock_data = df[(df['name'] == ticker) & (df.index >= start_date) & (df.index <= end_date)]
    return stock_data