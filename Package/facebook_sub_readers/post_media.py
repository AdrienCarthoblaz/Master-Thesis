import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10
from Package.facebook_sub_readers.own_post_transformers import gen, lists_creator

ALL_INDEX = False
ALL_GENERAL = False

class FacebookPostMediaReader(Reader):
    def read(self):
        '''
        Return a dataframe prom the pictures post on facebook, with the path to the picture in the Facebook file
        and the IP address used when uploading the picture.
        Nothing revolutionary, a new kind of nested dictionaries with multiple layer f list inside(see outputdict).
        NB: the ip address was inside a dictionnary and is taken out and added as 'main' column
        '''
        df = pd.read_json(self.path, convert_dates = False, encoding='utf-8')
        df = df[df['attachments'].notna()]
    
        returned = lists_creator(df, 'media')
        list_att = returned[1]
    
        outputdict = {}
        for i in list_att:
            for j in i:
                for key, value in j.items(): 
                    for k in value: 
                        for k2, v2 in k.items():
                            if k2 == 'media':
                                for k3, v3 in v2.items():
                                    outputdict[k3] = outputdict.get(k3, []) + [v3]
                            
        outputdict.pop('description',None)
    
        dict_ip = {}
        for i in outputdict['media_metadata']:
            for key, value in i.items():
                if isinstance(value, dict):
                    for k2, v2 in value.items():
                        dict_ip[k2] = dict_ip.get(k2, []) + [v2]
            
                else:
                    dict_ip[key] = dict_ip.get(key, []) + [value]
        dict_ip.pop('orientation',None)
    
        list_ip = list(dict_ip.values())
    
        df1 = pd.DataFrame.from_dict(outputdict)
        df1['ip'] = list_ip[0]
        df1['date'] = df1['creation_timestamp'].astype(int)
        main_df = main_transfo_timestamp_10(df1, 'Facebook', 'post picture')
    
        if ALL_INDEX: 
            main_df['uri'] = df1['uri']
            main_df['ip'] = df1['ip']
            main_df = main_df[['date','type','label','uri','ip','Year','Month','Day','Hour']]
    
        if ALL_GENERAL:
            main_df['name'] = df1.ip
            main_df['content'] = df1.uri
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
    
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
    
        self.df = main_df
    