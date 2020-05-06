import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookLikePageReader(Reader):
    def read(self):
        data = self.read_json_likes(self.path)
        df = pd.DataFrame(list(data['page_likes']))
        df['date'] = df['timestamp']
        df['content'] = df.date.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df, 'Facebook', 'like page')
    
        if ALL_INDEX: 
            main_df['page'] = df['name']
            main_df = main_df[['date','type','label','page','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df.name
            main_df['content'] = df.content
            main_df = main_df [['date','type','label','name','content','Year','Month','Day','Hour']]
        
    
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df
    
    def read_json_likes(self, path):
        '''
        Simply read json file and return a "brut" dataframe from it 
        '''
        data = pd.read_json(path, encoding='utf-8')
        return data