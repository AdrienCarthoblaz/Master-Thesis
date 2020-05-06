import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10
from Package.facebook_sub_readers.own_post_transformers import gen, lists_creator

ALL_INDEX = False
ALL_GENERAL = False

class FacebookPostExternalContent(Reader):
    def read(self):
        '''
        Same procedure as 'above' (posts) but for external content (url) post on facebook. 
        Nb: it could be the same function as above but nested dictionaries are encoded in other way 
        Idea: is it possible to create a 'big' function in order to destructured nested dictionary 
        '''
        df = pd.read_json(self.path, convert_dates = False, encoding='utf-8')
        df = df[df['attachments'].notna()]
        
        returned = lists_creator(df,'external_context')
        list_date = returned[0]
        list_att = returned[1]
        
        outputdict = {}
        for lis in list_att:
            for dic in lis:
                for key, value in dic.items():
                    for list_dic in value: 
                        for k2, v2 in list_dic.items():
                            for k3, v3 in v2.items():
                                outputdict[k3] = outputdict.get(k3, []) + [v3]
        outputdict.pop('name', None)
        outputdict.pop('source',None)
    
        df1 = pd.DataFrame.from_dict(outputdict)
        df1['date'] = list_date
        df1['name'] = df1.date.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df1, 'Facebook', 'post external content')
    
        if ALL_INDEX: 
            main_df['url'] = df1['url']
            main_df = main_df[['date','type','label','url','Year','Month','Day','Hour']]
    
        if ALL_GENERAL:
            main_df['name'] = df1.name
            main_df['content'] = df1.url
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
    
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
    
        self.df = main_df