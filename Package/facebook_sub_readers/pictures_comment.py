import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookPicturesCommentReader(Reader):
    def read(self):
        data = self.read_json_comments(self.path)
        df = pd.DataFrame(list(data['comments']))
        df = df[df['attachments'].notna()]
    
        list_date = []
        for i in df.iterrows():
            list_date.append(i[1][0])
    
        list_attachments = []
        for i in df.iterrows():
            list_attachments.append(i[1][3])

        outputdict = {}
        for lis in list_attachments:
            for dic in lis:
                for key, value in dic.items():
                    if isinstance(value, list):
                        value_dic = value[0]
                        for k2, v2 in value_dic.items(): 
                            for k3, v3 in v2.items():
                                outputdict[k3] = outputdict.get(k3, []) + [v3]
                                
        outputdict.pop('creation_timestamp',None)
        outputdict.pop('media_metadata',None)
        outputdict.pop('title',None)
    
        df = pd.DataFrame.from_dict(outputdict)
        df['date'] = list_date
        df['content'] = df.uri
        df['name'] = df.content.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df, 'Facebook', 'sticker comment')
    
        if ALL_INDEX: 
            main_df['uri'] = df['uri']
            main_df = main_df[['date','type','label','uri','Year','Month','Day','Hour']]
    
        if ALL_GENERAL:
            main_df['name'] = df.name
            main_df['content'] = df.content
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
    
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
    
        self.df = main_df

    def read_json_comments(self, path):
        '''
        Simply read json file and give a 'brut' dataframe (ie: 1x1)
        '''
        data = pd.read_json(path, encoding = 'utf-8')
        return data
