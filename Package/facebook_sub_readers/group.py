import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookGroupReader(Reader):
    def read(self):
        data = pd.read_json(self.path, encoding='utf-8')
        df = pd.DataFrame(list(data['groups_joined']))
        df['date'] = df['timestamp']
        df['name'] = df.date.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df, 'Facebook', 'group')
        
        title_begin_appareance = 'Vous avez arrÃªtÃ© dâÃªtre membre de '
        list_type = []
        for i in df['title']:
            if i[:len(title_begin_appareance)] == title_begin_appareance:
                list_type.append('group leaved')
            else: 
                list_type.append('group joined')
        
        main_df['label'] = list_type
        
        if ALL_INDEX: 
            main_df['title'] = df['title']
            main_df = main_df[['date','type','label','title','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df.name
            main_df['content'] = df.title
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df