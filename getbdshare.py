from bdshare import get_current_trade_data

df = get_current_trade_data()
# print(df.to_string())

from bdshare import get_hist_data
df1 = get_hist_data('2022-03-01','2022-03-02')
print(df1.to_string())



# Get market depth 
from bdshare import get_market_depth_data

df2 = get_market_depth_data('ACI') # get current buy and sell data
print(df2.to_string())



# Get DSE index data 
from bdshare import get_market_inf

df = get_market_inf() # get last 30 days market data
# print(df.to_string())

from bdshare import get_market_inf_more_data
df = get_market_inf_more_data('2022-03-01','2022-03-02') # get historical market data
print(df.to_string())