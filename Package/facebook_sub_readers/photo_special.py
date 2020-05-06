import pandas as pd
import json
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10
from Package.reader import Reader

ALL_INDEX = False
ALL_GENERAL = False

class FacebookPhotoSpecialReader(Reader):
    def open_photo_file(self, path):
        with open(path, encoding = 'utf-8') as json_data:
            data = json.load(json_data)
        return data
    
    def read(self):
        data = self.open_photo_file(self.path)
        
        outputdict = {}
        for key, value in data.items():
            if isinstance(value, dict):
                for k2, v2 in value.items():
                    outputdict[k2] = outputdict.get(k2, []) + [v2]
            
            else: 
                outputdict[key] = outputdict.get(key, []) + [value]
        outputdict.pop('name', None)
        outputdict.pop('photos',None)
        outputdict.pop('comments',None)
        outputdict.pop('description',None)
        
        df = pd.DataFrame.from_dict(outputdict)
        df['date'] = df['last_modified_timestamp']
        df['name'] = df.date.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df, 'Facebook', 'photo')
        
        if ALL_INDEX: 
            main_df['uri'] = df['uri']
            main_df = main_df[['date','type','label','uri','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df.name
            main_df['content'] = df.uri
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df 

