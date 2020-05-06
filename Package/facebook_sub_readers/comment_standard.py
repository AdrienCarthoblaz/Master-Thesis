import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookCommentStandardReader(Reader):
    def read(self):
        '''
        This function return a dataframe with all relevant informations about Facebook comments: 
        1) list all main dictionaries from the 'brut' dataframe and keep only raws where there is no attachment (
        ie without path to a picture) and with 'data' ('data' contains timestamp, the comment and the author (and 
        for a few of them the group where the comment was written))
        2) a list containing all 'data' (dictionary of dictionaries) is created 
        3) from these nested dictionaries the sub-dictionaries are extracted and 'merged' under a dictionary with 
        three 'super keys' (timestamp, comment, author) --> nb: 'group' it's not relevant and 'can't be transform 
        into a dataframe' 
        4) Timestamp is transformed into a datetime(ns), type and label are added 
        5) If all_index = True, the comment is added in the dataframe 
        '''
    
        data = self.read_json_comments(self.path)
        df = pd.DataFrame(list(data['comments']))
        df = df[pd.isnull(df['attachments'])]
        df = df[df['data'].notna()]
    
        list_data = []
        for i in df.iterrows():
            list_data.append(i[1][1])
        
        outputdict = self.drop_nesteddictionary_fb_comment(list_data)
    
    
        df1 = pd.DataFrame.from_dict(outputdict)
        df1['date']= df1['timestamp'].astype(int)
        main_df = main_transfo_timestamp_10(df1, 'Facebook', 'comment')
    
        if ALL_INDEX:
            main_df['comment'] = df1['comment']
            main_df['author'] = df1['author']
            main_df = main_df[['date','type','label','author','comment','Year','Month','Day','Hour']]
    
        if ALL_GENERAL:
            main_df['name'] = df1.author
            main_df['content'] = df1.comment
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
    
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
    
        self.df = main_df
        
    def read_json_comments(self, path):
        '''
        Simply read json file and give a 'brut' dataframe (ie: 1x1)
        '''
        data = pd.read_json(path, encoding = 'utf-8')
        return data

    def drop_nesteddictionary_fb_comment(self, alist):
        outputdict = {}
        for lis in alist:
            for dic in lis:
                for key, value in dic.items():
                    if isinstance(value,dict):
                        for k2, v2 in value.items():
                            outputdict[k2] = outputdict.get(k2, []) + [v2]
        outputdict.pop('group',None)
        return outputdict