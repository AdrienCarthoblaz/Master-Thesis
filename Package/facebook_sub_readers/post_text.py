import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10
from Package.facebook_sub_readers.own_post_transformers import gen, lists_creator

ALL_GENERAL = False

class FacebookPostTextReader(Reader):
    def read(self):
        '''
        Return the 'text' created by facebook (ie. friend anniversary on facebook). The json file is quite complex
        and most of the info not so relevant, so this function keep only the date and type and label it
        '''
        df = pd.read_json(self.path, convert_dates = False, encoding='utf-8')
        df = df[df['attachments'].notna()]
    
        returned = lists_creator(df,'text')
        list_date = returned[0]
        list_text = []
        
        for i in list_date:
            list_text.append('post text')
    
        main_df = pd.DataFrame(list(zip(list_date,list_text)), columns=['date','label'])
        main_df['date'] = main_df.date.apply(lambda x : pd.to_datetime(x, unit='s'))
        main_df['Year'] = main_df.date.apply(lambda x: x.year)
        main_df['Month'] = main_df.date.apply(lambda x: x.month)
        main_df['Day'] = main_df.date.apply(lambda x: x.day)
        main_df['Hour'] = main_df.date.apply(lambda x: x.hour)
        
        main_df['type'] = main_df.date.apply(lambda x: 'Facebook')
        main_df['name'] = main_df.date.apply(lambda x: 'NaN')
        main_df['content'] = main_df.name.apply(lambda x: 'NaN')
        
        if ALL_GENERAL:
            main_df = main_df[['date','type','label', 'name', 'content','Year','Month','Day','Hour']]
            
        else: 
            main_df = main_df[['date','type','label','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df
