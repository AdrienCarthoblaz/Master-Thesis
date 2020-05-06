import pandas as pd 
import json
from datetime import datetime, date, time
from Package.reader import Reader

ALL_INDEX = False
ALL_GENERAL = False

class SnapchatMemoryReader(Reader):
    def read(self):
        '''
        This function returns a dataframe from the snapchat's json file named memory_history.json
        '''
        with open(self.path, encoding = 'utf-8') as json_data:
            data = json.load(json_data)
            
        outputdict = {}
        for key, value in data.items():
            for lis in value:
                for k2, v2 in lis.items():
                    outputdict[k2] = outputdict.get(k2, []) + [v2]
        
        df = pd.DataFrame.from_dict(outputdict)
        df['date'] = df['Date']
        date_format = '%Y-%m-%d %H:%M:%S UTC'
        df['date'] = df.date.apply(lambda t: datetime.strptime(t, date_format))
        df['Year'] = df.date.apply(lambda x: x.year)
        df['Month'] = df.date.apply(lambda x: x.month)
        df['Day'] = df.date.apply(lambda x: x.day)
        df['Hour'] = df.date.apply(lambda x: x.hour)
        
        df['type'] = df.date.apply(lambda x: 'Snapchat')
        df['label'] = df.date.apply(lambda x: 'memory')
        
        df['name'] = df['Media Type']
        df['content'] = df['Download Link']
        
        main_df = df[['date','type','label','Year','Month','Day','Hour']]
        
        if ALL_INDEX:
            main_df['url'] = df['Download Link']
            main_df['media type'] = df['Media Type']
            main_df = main_df[['date','type','label','media type','url','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df = df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df