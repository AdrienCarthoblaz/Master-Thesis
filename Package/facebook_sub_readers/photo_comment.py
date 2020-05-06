import pandas as pd
import json
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10
from Package.reader import Reader

ALL_INDEX = False
ALL_GENERAL = False
ME = 'Enter your facebook pseudo'

class FacebookPhotoCommentReader(Reader):
    def open_photo_file(self, path):
        with open(path, encoding = 'utf-8') as json_data:
            data = json.load(json_data)
        return data
    
    def give_a_photo_dict(self, data):
        outputdict = {'author':[]}
        condition = ''
        for key, value in data.items():
            if isinstance(value, list):
                for lis in value: 
                    for k2, v2 in lis.items():
                        if isinstance(v2, list):
                            for lis_2 in v2:
                                for k3, v3 in lis_2.items():
                                    if condition == 'comment' and k3 != 'author':
                                        outputdict.setdefault('author', []).append('unknown')
                                        outputdict[k3] = outputdict.get(k3, []) + [v3]
                                    else:
                                        outputdict[k3] = outputdict.get(k3, []) + [v3]
                                    
                                    condition = k3
                    
                        else: 
                            outputdict[k2] = outputdict.get(k2, []) + [v2]
            
        
            elif isinstance(value, dict):
                continue
            
            else:
                outputdict[key] = outputdict.get(key, []) + [value]
                
        return outputdict
    
    def read(self):
        data = self.open_photo_file(self.path)
        outputdict = self.give_a_photo_dict(data)
        
        outputdict.pop('name',None)
        outputdict.pop('uri',None)
        outputdict.pop('creation_timestamp',None)
        outputdict.pop('title',None)
        outputdict.pop('description',None)
        outputdict.pop('last_modified_timestamp',None)
        outputdict.pop('media_metadata',None)
        
        df = pd.DataFrame.from_dict(outputdict)
        df['date'] = df['timestamp']
        main_df = main_transfo_timestamp_10(df, 'Facebook', 'photo comment')
        main_df['label'] = df['author']
        main_df['label']=main_df['label'].apply(lambda x: 'own comment photo' if x == ME else 'other comment photo')
        
        if ALL_INDEX: 
            main_df['comment'] = df['comment']
            main_df['author'] = df['author']
            main_df = main_df[['date','type','label','author','comment','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df.author
            main_df['content'] = df.comment
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df