import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10
from Package.facebook_sub_readers.own_post_transformers import gen, lists_creator

ALL_GENERAL = False
ALL_INDEX = False

class FacebookPostPlaceReader(Reader):
    def read(self):
        df = pd.read_json(self.path, convert_dates = False, encoding='utf-8')
        df = df[df['attachments'].notna()]
        
        returned = lists_creator(df,'place')
        list_date = returned[0]
        list_att = returned[1]
        
        outputdict = {}
        for lis in list_att:
            for lis_2 in lis:
                for key, value in lis_2.items():
                    for lis_3 in value: 
                        for k2, v2 in lis_3.items():
                            for k3, v3 in v2.items():
                                outputdict[k3] = outputdict.get(k3, []) + [v3] 
        outputdict.pop('url',None)
        
        new_outputdict = {a: list(set(b)) for a, b in outputdict.items()}
        
        df1 = pd.DataFrame.from_dict(new_outputdict)
        df1['date'] = list_date
        df1['content'] = df1.date.apply(lambda x: 'NaN')
        main_df =  main_transfo_timestamp_10(df1, 'Facebook', 'place')
        
        if ALL_INDEX:
            main_df['name'] = df1['name']
            main_df = main_df[['date','type','label','name','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df1.name
            main_df['content'] = df1.content
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df   