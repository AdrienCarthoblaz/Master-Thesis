import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookStickerCommentReader(Reader):
    def read(self): 
        '''
        'Attachment' contains the path to the sticker used on the comment, it can be useful for some usages. This 
        function keep only raws where there is an attachment. Then collect the timestamp in a list. And nested
        dictionaries containing the path we described above are also put in a list. Nested dictionaries are 'denested'
        to keep only the path in a dictionary. From this last dictionary, a dataframe is created and the date is added
        to it. Then the same operation on date, type and label are performed.
        nb if all_index = True, path to the sticker used is added 
        '''
    
        data = self.read_json_likes(self.path)
        df = pd.DataFrame(list(data['reactions']))
        df = df[df['attachments'].notna()]
    
        list_date = []
        for i in df.iterrows():
            list_date.append(i[1][0])
    
        list_link = []
        for i in df.iterrows():
            list_link.append(i[1][3][0])
    
        outputdict = {}
        for dic in list_link: 
            for key, value in dic.items():
                if isinstance(value, list):
                    value_dic = value[0]
                    for k2, v2 in value_dic.items():
                        if isinstance(v2, dict):
                            for k3, v3 in v2.items():
                                outputdict[k3] = outputdict.get(k3, []) + [v3]
    
        df = pd.DataFrame.from_dict(outputdict)
        df['date'] = list_date
        df['name'] = df.date.apply(lambda x: 'NaN')
        df['content'] = df.uri
        main_df = main_transfo_timestamp_10(df, 'Facebook', 'sticker comment')
    
        if ALL_INDEX:
            main_df['uri'] = df['uri']
            main_df = main_df[['date','type','label','uri','Year','Month','Day','Hour']]
    
        if ALL_GENERAL:
            main_df['name'] = df['name']
            main_df['content'] = df['content']
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
    
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
       
    
        self.df = main_df 
        
    def read_json_likes(self, path):
        '''
        Simply read json file and return a "brut" dataframe from it 
        '''
        data = pd.read_json(path, encoding='utf-8')
        return data