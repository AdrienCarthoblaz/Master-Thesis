import os
import json
from Package.reader import Reader
import pandas as pd 
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_13

ME = 'Enter your facebook pseudo here'
ALL_INDEX = False
ALL_GENERAL = False


class FacebookMessageStandardReader(Reader):
    def get_adict(self, data):
        '''
        Transform the nested dictionary into a dictionary with data rearranged
        --> all raws have a timestamp but when a there is a picture shared, there is no 'content', so when there is 
            a picture, a file shared, a video or a gif we add the mention media into content (forced to do that to 
            have arrays of the same size, avoid to lose the content). We also add the dictionary in the denested 
            dictionary in order to be able to find the uri associated with the media
        --> same for sticker, 'lost msg' and audio but we do not keep their uris (it's a choice as there are few 
            numbers of them)
        '''
        outputdict = {'content':[]}
        condition = ''
        for key, value in data.items():
            if isinstance (value, list):
                for lis in value: 
                    for k2, v2 in lis.items():
                        if condition == 'timestamp_ms' and k2 != 'content':
                            if k2 == 'photos' or k2=='files' or k2=='videos' or k2=='gifs' :
                                outputdict.setdefault('content', []).append('media')
                                outputdict[k2] = outputdict.get(k2, []) + [v2]
                            elif k2 == 'sticker':
                                outputdict.setdefault('content', []).append('sticker')
                            elif k2 == 'type':
                                outputdict.setdefault('content', []).append('NaN')
                            elif k2 == 'audio_files':
                                outputdict.setdefault('content', []).append('audio')
                    
                        else:
                            outputdict[k2] = outputdict.get(k2, []) + [v2]
                            
                        condition = k2
            else: 
                outputdict[key] = outputdict.get(key, []) + [value]
        return outputdict 
    
    
    def proc_fb_messages_standard(self, path):
        '''
        From the denested and rearranged dictionary this function give a 'clean' dataframe.
        --> nb: it's a new type of timestamp used (ie. 13 digits)
        --> all index give the possibility to keep the content exchanged 
        '''
        with open(path, encoding = 'utf-8') as json_data:
            data = json.load(json_data)
            
        outputdict = self.get_adict(data)
        outputdict.pop('name',None)
        outputdict.pop('type',None)
        outputdict.pop('title',None)
        outputdict.pop('thread_type',None)
        outputdict.pop('thread_path',None)
        outputdict.pop('photos',None)
        outputdict.pop('files',None)
        outputdict.pop('is_still_participant',None)
        outputdict.pop('share',None)
        outputdict.pop('videos',None)
        outputdict.pop('gifs',None)
        outputdict.pop('call_duration', None)
        outputdict.pop('missed', None)
        outputdict.pop('share', None)
        outputdict.pop('users', None)
        outputdict.pop('reactions', None)
        
        df = pd.DataFrame.from_dict(outputdict)
        df['date'] = df['timestamp_ms']
        
        main_df = main_transfo_timestamp_13(df, 'Facebook' , 'msg')
        main_df['label'] = df['sender_name']
        main_df['label']=main_df['label'].apply(lambda x: 'msg sent' if x == ME else 'msg received')
        
        if ALL_INDEX: 
            main_df['name'] = df['sender_name']
            main_df['content'] = df['content']
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df.sender_name
            main_df['content'] = df.content
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        return main_df
    
    
    
    def read(self):
        '''
        This function merges all dicussion contained in the specified files 
        '''
        list_dir = os.listdir(self.path)
        for l in list_dir[:1]:
            for f in os.listdir(self.path+l):
                if f.endswith(".json"):
                    main_df = self.proc_fb_messages_standard(self.path+l+"/"+f)
    
    
        for l in list_dir[1:]:
            for f in os.listdir(self.path+l):
                if f.endswith(".json"):
                    df = self.proc_fb_messages_standard(self.path+l+"/"+f)
                    main_df = pd.concat([main_df,df])
    
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df