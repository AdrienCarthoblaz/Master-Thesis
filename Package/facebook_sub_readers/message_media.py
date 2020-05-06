import os
import json
from Package.reader import Reader
import pandas as pd 
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookMessageMediaReader(Reader):
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
    
    
    def data_fb_pictures_sent_by_msg(self, path):
        '''
        This function permit to refind uris of pictures, videos and files exchanged by msg.
        --> we have to check if in the json file there is such type of files, we use dictionary's key to do this work
        --> if there is an existence all useful informations are transformed into a dataframe
        --> if multiple kind of medias had been exchanged in a conversation, we concatenated them (it's why we have
            to check if a dataframe of a certain type exists or not)
        --> dataframe is cleaned 
        --> if a dataframe exist it is returned, else the function returns 0
        '''
        with open(path, encoding = 'utf-8') as json_data:
            data = json.load(json_data)
            
        outputdict = self.get_adict(data)
            
        for key in outputdict:
            if key == 'photos':
                outputdict_pics = {}
                for i in outputdict['photos']:
                    for dic in i:
                        for key, value in dic.items():
                            outputdict_pics[key] = outputdict_pics.get(key, []) + [value]
                df = pd.DataFrame.from_dict(outputdict_pics)
            else: 
                continue 
        
        for key in outputdict:
            if key == 'files':   
                outputdict_file = {}
                for i in outputdict['files']:
                    for dic in i:
                        for key, value in dic.items():
                            outputdict_file[key] = outputdict_file.get(key, []) + [value]
                df2 = pd.DataFrame.from_dict(outputdict_file)
            else: 
                continue
                
        for key in outputdict:
            if key == 'videos':        
                outputdict_video = {}
                for i in outputdict['videos']:
                    for dic in i:
                        for key, value in dic.items():
                            outputdict_video[key] = outputdict_video.get(key, []) + [value]
                outputdict_video.pop('thumbnail')
                df3 = pd.DataFrame.from_dict(outputdict_video)          
                
            else:
                continue
        
        if 'df' in locals():
            if 'df2' in locals():
                df = pd.concat([df, df2])
            if 'df3' in locals():
                df = pd.concat([df,df3])
        else: 
            if 'df2' in locals():
                df = df2
                if 'df3' in locals():
                    df = pd.concat([df,df3])
            elif 'df3' in locals():
                df = df3
         
        if 'df' in locals():
            df['date'] = df['creation_timestamp'].astype(int)
            df['name'] = df.date.apply(lambda x: 'NaN')
            main_df = main_transfo_timestamp_10(df, 'Facebook', 'msg media')
            main_df = main_df[['date','type','label','Year','Month','Day','Hour']]
            
            
            if ALL_INDEX:
                main_df['uri'] = df['uri']
                main_df = main_df[['date','type','label','uri','Year','Month','Day','Hour']]
            
            if ALL_GENERAL:
                main_df['name'] = df.name
                main_df['content'] = df.uri
                main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
            
            main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
            return main_df, 1
        
        else: 
            return 0, 0
    
    
    def read(self):
        '''
        This function merges all medias contained in the specified file
        --> nb we have to find a file with media in it to begin the concatenation, it's why we check all the json
            files in the first loop until one is found and then break.
        '''
        list_dir = os.listdir(self.path)
        i = 0
        breaking = False
        for l in list_dir:
            for f in os.listdir(self.path+l):
                if f.endswith(".json"):
                    returned = self.data_fb_pictures_sent_by_msg(self.path+l+"/"+f)
                    main_df = returned[0]
                    i = i+1
                    if returned[1] == 1:
                        breaking = True
                        break
            if breaking :
                break
                
        for l in list_dir[1:]:
            for f in os.listdir(self.path+l):
                if f.endswith(".json"):
                    returned = self.data_fb_pictures_sent_by_msg(self.path+l+"/"+f)
                    df = returned[0]
                    if returned[1] == 1:
                        main_df = pd.concat([main_df,df])
                        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
                    else:
                        continue
    
        
        self.df = main_df
    