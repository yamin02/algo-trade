from bdshare import get_current_trade_data

df = get_current_trade_data()
print(df.to_string())