import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookLikePostReader(Reader): 
    def read(self):
        '''
        1) From the "brut"dataframe obtained above, this function list all the different key contained in the column
        reaction and only keep raws where 'attachements' is null (means it's a like on a post without sticker).
        2) Then the standart procedure is implemented (ie. transform the timestamp 10 digits in datetime(ns), split
        the components of date in proper column for further analysis, flag with the type and label)
        3) if all_index = True, the title (ie. xxx a aime le post de yyy) is added to the dataframe 
        '''
    
        data = self.read_json_likes(self.path)
        df = pd.DataFrame(list(data["reactions"]))
        df = df[pd.isnull(df['attachments'])]
    
        df['date']= df['timestamp'].astype(int)
        df['content'] = df.title
        df['name'] = df.title.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df, 'Facebook', 'like post')
    
        if ALL_INDEX: 
            main_df['title'] = df['title']
            main_df = main_df[['date','type','label','title','Year','Month','Day','Hour']]
    
        if ALL_GENERAL:
            main_df['name'] = df['name']
            main_df['content'] = df['content']
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
    
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
    
        self.df=main_df
    
    def read_json_likes(self, path):
        '''
        Simply read json file and return a "brut" dataframe from it 
        '''
        data = pd.read_json(path, encoding='utf-8')
        return data
