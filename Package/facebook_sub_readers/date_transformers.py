import pandas as pd
from datetime import datetime, date, time

def main_transfo_timestamp_10(df, type_data, label):
    main_df = df.copy()
    main_df['date'] = main_df.date.apply(lambda x : pd.to_datetime(x, unit='s'))
    main_df['Year'] = main_df.date.apply(lambda x: x.year)
    main_df['Month'] = main_df.date.apply(lambda x: x.month)
    main_df['Day'] = main_df.date.apply(lambda x: x.day)
    main_df['Hour'] = main_df.date.apply(lambda x: x.hour)
    
    main_df['type'] = main_df.date.apply(lambda x: type_data)
    main_df['label'] = main_df.date.apply(lambda x: label )
    
    main_df = main_df[['date','type','label','Year','Month','Day','Hour']]
    
    return main_df

def main_transfo_timestamp_13(df, type_data, label):
    main_df = df.copy()
    main_df['date'] = main_df.date.apply(lambda x: datetime.fromtimestamp(int(x/1000)))
    main_df['Year'] = main_df.date.apply(lambda x: x.year)
    main_df['Month'] = main_df.date.apply(lambda x: x.month)
    main_df['Day'] = main_df.date.apply(lambda x: x.day)
    main_df['Hour'] = main_df.date.apply(lambda x: x.hour)
    
    main_df['type'] = main_df.date.apply(lambda x: type_data)
    main_df['label'] = main_df.date.apply(lambda x: label )
    
    main_df = main_df[['date','type','label','Year','Month','Day','Hour']]
    
    return main_df