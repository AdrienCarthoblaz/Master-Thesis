import pandas as pd
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookSearchHistoryReader(Reader):
    def read(self):
        data = pd.read_json(self.path)
        df = pd.DataFrame(list(data['searches']))
        
        outputdict = {}
        for lis in df['attachments']:
            for dic in lis:
                for key, value in dic.items():
                    for dic_2 in value:
                        for k2, v2 in dic_2.items():
                            outputdict[k2] = outputdict.get(k2, []) + [v2]
                            
        df['search'] = outputdict['text']
        df['date'] = df['timestamp']
        df['name'] = df.date.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df, 'Facebook', 'search_history')
        
        if ALL_INDEX: 
            main_df['search'] = df['search']
            main_df = main_df[['date','type','label','search','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df.name
            main_df['content'] = df.search
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
            
        self.df = main_df 