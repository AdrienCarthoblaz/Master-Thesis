import pandas as pd
from datetime import datetime, date, time
from Package.reader import Reader

ALL_INDEX = False
ALL_GENERAL = False 

class GoogleBrowserHistoryReader(Reader):
    def read(self):
        '''
        Return a datframe from the json file of the Chrome Browser History: 
        ---> the date is given from a timestamp (16 digits) wich is changed into a datime 
        '''
        
        data = pd.read_json(self.path)
        df = pd.DataFrame(list(data["Browser History"]))
        
        df['date']= df['time_usec'].apply(lambda x : datetime.fromtimestamp(int(x/1000000)))
        df['Year'] = df.date.apply(lambda x: x.year)
        df['Month'] = df.date.apply(lambda x: x.month)
        df['Day'] = df.date.apply(lambda x: x.day)
        df['Hour'] = df.date.apply(lambda x: x.hour)
        
        df['type']= df.date.apply(lambda x: 'Google')
        df['label']= df.date.apply(lambda x: 'search')
        
        df['name'] = df.title
        df['content'] = df.url
        
        main_df = df[["date",'type','label',"Year","Month","Day","Hour"]]
        
        if ALL_INDEX:
            main_df = df[["date",'type','label',"title","url","Year","Month","Day","Hour"]]
        
        if ALL_GENERAL: 
            main_df = df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df
