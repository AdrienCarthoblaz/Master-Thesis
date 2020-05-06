import pandas as pd
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookLocationReader(Reader):
    def read(self):
        data = pd.read_json(self.path, encoding = 'utf-8')
        df = pd.DataFrame(list(data['location_history']))
        
        outputdict = {}
        for dic in df['coordinate']:
            for key, value in dic.items():
                outputdict[key] = outputdict.get(key, []) + [value]
        
        df['longitude']= outputdict['longitude']
        df['latitude'] = outputdict['latitude']
        df['date'] = df['creation_timestamp']
        df['content'] = df.date.apply(lambda x: 'NaN')
        
        main_df = main_transfo_timestamp_10(df, 'Facebook', 'location')
        
        if ALL_INDEX:
            main_df['name'] = df['name']
            main_df['latitude'] = df['latitude']
            main_df['longitude'] = df['longitude']
            
            main_df = main_df[['date','type','label','name','latitude','longitude','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df.name
            main_df['content'] = df.content
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
            
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
            
                
        self.df = main_df 