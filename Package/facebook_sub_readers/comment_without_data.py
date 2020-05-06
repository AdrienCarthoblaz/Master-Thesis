import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookCommentWithoutDataReader(Reader):
    def read(self):
        '''
        The function return a dataframe as above but has to be witten differently as these comments have not a 'data'
        column. 
        nb: the two lists created to form the dataframe are useless as we can just drop columns which are not relevant,
        but this works as well
        '''
    
        data = self.read_json_comments(self.path)
        df = pd.DataFrame(list(data['comments']))
        df = df[pd.isnull(df['attachments'])]
        df = df[pd.isnull(df['data'])]
    
        list_date = []
        for i in df.iterrows():
            list_date.append(i[1][0])
    
        list_title = []
        for i in df.iterrows():
            list_title.append(i[1][2])
    
        df1 = pd.DataFrame(list(zip(list_date, list_title)), columns=['date','title'])
        df1['date']= df1['date'].astype(int)
        df1['name'] = df1.date.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df1, 'Facebook', 'comment')
    
        if ALL_INDEX: 
            main_df['title'] = df1['title']
            main_df = main_df[['date','type','label','title','Year','Month','Day','Hour']]
    
        if ALL_GENERAL:
            main_df['name'] = df1.name
            main_df['content'] = df1.title
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
    
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df

    def read_json_comments(self, path):
        '''
        Simply read json file and give a 'brut' dataframe (ie: 1x1)
        '''
        data = pd.read_json(path, encoding = 'utf-8')
        return data
