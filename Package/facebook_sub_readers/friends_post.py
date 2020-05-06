import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
ALL_GENERAL = False

class FacebookFriendsPostReader(Reader):
    def read(self):
        '''
        Concatenate the four dataframe created in order to have a unified dataframe 
        '''
        
        df1 = self.proc_fb_others_post_standard(self.path)
        df2 = self.proc_fb_others_post_without_title(self.path)
        df3 = pd.concat([df1,df2])
        df4 = self.proc_fb_others_post_without_posts(self.path)
        df5 = pd.concat([df3,df4])
        df6 = self.proc_fb_others_post_where_everything_is_missing(self.path)
        main_df = pd.concat([df5,df6])
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True) 
        
        self.df = main_df 
    
    
    def gen_1(self, adict):
        '''
        The json file containing friend's posts is quite messy with timestamp for all entries (464 in my case) but 
        not all enties have a title or the posts associated.
        --> this function return true if the nested dictionary sent contains a dictionnary with a key == 'post',
        meaning this entry has the associated post in the data
        '''
        for key, value in adict.items():
            if isinstance(value, list):
                for lis_2 in value:
                    if isinstance (lis_2, str):
                        continue
                
                    else:
                        for k2, v2 in lis_2.items():
                            if k2 == 'post':
                                return True
                            else:
                                continue
            else:
                continue
    def gen_2(self, adict):
        '''
        Same as above but for dictionnary with a key == 'title'
        '''
        for key, value in adict.items():
            if key == 'title':
                return True
            else: 
                continue 
    
    def others_post_post(self, path):
        '''
        This function return a dataframe of other's post where the post is explicitely written
        '''
        data = pd.read_json(path, encoding = 'utf-8')
        df = pd.DataFrame(list(data["wall_posts_sent_to_you"])).T
        
        list_data = []
        for i in df.iterrows():
            list_data.append(i[1][0])
        
        outputdict = {}
        for lis in list_data:
            if self.gen_1(lis):
                for key, value in lis.items():
                    if isinstance(value, list):
                        for lis_2 in value:
                            if isinstance (lis_2, str):
                                continue
                
                            else:
                                for k2, v2 in lis_2.items():
                                    outputdict[k2] = outputdict.get(k2, []) + [v2]
            
                    else: 
                        outputdict[key] = outputdict.get(key, []) + [value]
    
        outputdict.pop('title',None)
        outputdict.pop('update_timestamp',None)
        outputdict.pop('data',None)
        
        df1 = pd.DataFrame.from_dict(outputdict)
        df1['timestamp'].astype(str)
        
        return df1
    
    def others_post_title(self, path):
        '''
        This function return a dataframe of other's post where the title of the post (ie. xxx a ecrit sur votre
        journal) is explicitely written
        '''
        data = pd.read_json(path, encoding = 'utf-8')
        df = pd.DataFrame(list(data["wall_posts_sent_to_you"])).T
        
        list_data = []
        for i in df.iterrows():
            list_data.append(i[1][0])
        
        outputdict = {}
        for lis in list_data:
            if self.gen_2(lis):
                for key, value in lis.items():
                    if isinstance(value, list):
                        for lis_2 in value:
                            if isinstance (lis_2, str):
                                continue
                
                            else:
                                for k2, v2 in lis_2.items():
                                    outputdict[k2] = outputdict.get(k2, []) + [v2]
            
                    else: 
                        outputdict[key] = outputdict.get(key, []) + [value]
    
        outputdict.pop('post',None)
        outputdict.pop('update_timestamp',None)
        outputdict.pop('data',None)
        
        df2 = pd.DataFrame.from_dict(outputdict)
        df2['timestamp'].astype(str)
           
        return df2 
    
    def proc_fb_others_post_standard(self, path):
        '''
        This function merge (where the timestamp is equivaent) the two function above into one dataframe 
        containing all informations
        '''
        df1 = self.others_post_post(path)
        df2 = self.others_post_title(path)
        
        df3 = pd.merge(df1, df2, on='timestamp')
        df3['date'] = df3['timestamp']
        main_df = main_transfo_timestamp_10(df3, 'Facebook', 'others post')
        
        if ALL_INDEX: 
            main_df['post'] = df3['post']
            main_df['title']= df3['title']
            main_df = main_df[['date','type','label','title','post','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df3.title
            main_df['content'] = df3.post
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        
        return main_df
    
    def proc_fb_others_post_without_title(self, path):
        '''
        Some posts have no title (links for exemple) this function compare the dataframe returned from others_post_post
        and the main dataframe containing all infos (ie. title and posts)
        --> this is done by a left joining on the date, the merge column says if the date is in both dataframe or
            only in the left one, all which are in both are abandonned and only posts without title are returned
        '''
        df1 = self.others_post_post(path)
        df1['date'] = df1['timestamp']
        df1['date'] = df1.date.apply(lambda x : pd.to_datetime(x, unit='s'))
        
        df2 = self.proc_fb_others_post_standard(path)
        
        df_all = df1.merge(df2.drop_duplicates(), on='date', how='left', indicator=True)
        df_all = df_all[df_all['_merge']== 'left_only']
        df_all['date'] = df_all['timestamp'].astype(str)
        df_all['name'] = df_all.date.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df_all, 'Facebook', 'others post')
        
        
        if ALL_INDEX:
            main_df['post'] = df_all['post_x']
            main_df = main_df[['date','type','label','post','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df_all.name
            main_df['content'] = df_all.post_x
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
            
        return main_df
    
    def proc_fb_others_post_without_posts(self, path):
        '''
        Same as above but for post "with no post" (meaning a picture or a link for example --> xxx a poste une 
        photo sur votre journal)
        '''
        
        df1 = self.others_post_title(path)
        df1['date'] = df1['timestamp']
        df1['date'] = df1.date.apply(lambda x : pd.to_datetime(x, unit='s'))
        
        df2 = self.proc_fb_others_post_standard(path)
        
        df_all = df1.merge(df2.drop_duplicates(), on='date', how='left', indicator=True)
        df_all = df_all[df_all['_merge']== 'left_only']
        df_all['date'] = df_all['timestamp'].astype(str)
        df_all['content'] = df_all.date.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df_all, 'Facebook', 'others post')
        
        
        if ALL_INDEX:
            main_df['title'] = df_all['title_x']
            main_df = main_df[['date','type','label','title','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df_all.title_x
            main_df['content'] = df_all.content
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        return main_df
    
    '''
    Following functions are all used for the same purpose, finding and create a dataframe with post with no title
    and no posts (in my data this means one occurence)
    '''
    
    def concat_all_for_a_list(self, path):
        '''
        Concatenate dataframe with a title and with a post, to obtain a list of the timestamp
        --> drop duplicated timestamps
        '''
        df1 = self.others_post_post(path)
        df2 = self.others_post_title(path)
        df_all = pd.concat([df1,df2])
        df_all.drop_duplicates(subset='timestamp', keep='first')
        
        list_timestamp = []
        
        for i in df_all.iterrows():
            list_timestamp.append(i[1][0])
        
        return list_timestamp
    
    def gen_3(self, adict):
        '''
        If the dictionary given has a key called 'attchments' return True (it's the only "personal"characteristic 
        I found for the only post without title and post)
        '''
        for key, value in adict.items():
            if key == 'attachments':
                return True
            else: 
                continue
    
    def gen_4(self, adict, alist):
        '''
        From a dictionary and a list given this function returns true if the value of the timestamp == timestamp 
        contained in the list given
        '''
        for key, value in adict.items():
            for i in alist:
                if value == i:
                    return True
                else: 
                    continue
    
    def proc_fb_others_post_where_everything_is_missing(self, path):
        '''
        Return a dataframe of the row still untreated (ie without title and post):
        1) list_timestamp_rebels collect timestamp of rows with 'attachments', some posts with post have also
        attachments inside 
        2) concat_all_for_a_list return all the timestamps 'already treated', main_list keeps only timestamp which
        haven't been treated yet 
        3) with all conditions implemented, nested dictionaries are 'denested' and an ordonated dictionary is
        created
        --> nb: due to only one observation, the dictionary may be subjected to problem for other users (may lead 
        to some changes)
        4) a dataframe is produced from the dictionary and treated as usual 
        '''
        
        data = pd.read_json(path, encoding = 'utf-8')
        df = pd.DataFrame(list(data["wall_posts_sent_to_you"])).T
        
        list_data = []
        for i in df.iterrows():
            list_data.append(i[1][0])
        
        list_timestamp_rebels = []
        for lis in list_data:
            if self.gen_3(lis):
                for key, value in lis.items():
                    if key == 'timestamp':
                        list_timestamp_rebels.append(value)
                             
        list_timestamp = self.concat_all_for_a_list(path)
                             
        main_list = list(set(list_timestamp_rebels)-set(list_timestamp))
        
        outputdict = {}
        for lis in list_data:
            if self.gen_3(lis):
                if self.gen_4(lis, main_list):
                    for key, value in lis.items():
                        if isinstance (value, list):
                            for lis_2 in value:
                                for k2, v2 in lis_2.items(): 
                                    if isinstance (v2, list):
                                        for lis_3 in v2:
                                            for k3, v3 in lis_3.items():
                                                for k4, v4, in v3.items():
                                                    outputdict[k4] = outputdict.get(k4, []) + [v4]
                                                
                                    else:
                                        outputdict[k2] = outputdict.get(k2, []) + [v2]
                                    
                        else:
                            outputdict[key] = outputdict.get(key, []) + [value]
        
        df1 = pd.DataFrame.from_dict(outputdict)
        df1['date'] = df1['timestamp']
        df1['name'] =df1.date.apply(lambda x: 'NaN')
        main_df = main_transfo_timestamp_10(df1, 'Facebook', 'others post')
        
        if ALL_INDEX: 
            main_df['url'] = df1['url']
            main_df = main_df[['date','type','label','url','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df['name'] = df1.name
            main_df['content'] = df1.url
            main_df = main_df[['date','type','label','name','content','Year','Month','Day']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        return main_df             