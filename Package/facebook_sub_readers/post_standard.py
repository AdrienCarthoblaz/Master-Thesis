import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookPostStandardReader(Reader):
    def read(self): 
        '''
        This function convert the json file given by facebook about posts (they do not differenciate post on your 
        wall, on others wall, statut update or 'mood' --> it was not important in my analysis but could be for other
        usage so take note)
        1) Tansform timestampe (10 digits) in a datetime(ns) format, add a type and a label 
        '''
        df = pd.read_json(self.path, convert_dates = False, encoding = 'utf-8')
        df = df[pd.isnull(df['attachments'])]
        df['date']= df['timestamp'].astype(int)
        df['name'] = df.date.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df, 'Facebook', 'post')
    
        if ALL_INDEX:
            main_df['title'] = df['title']
            main_df = main_df[['date','type','label','title','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name']=df.name
            main_df['content'] = df.title
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
    
        self.df = main_df