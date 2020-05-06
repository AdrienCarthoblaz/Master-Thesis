import pandas as pd 
import re
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10

ALL_INDEX = False
FRIENDS_WITH_CONTACTS = False
'''
The first one for the following is only for friends still in the contact (ie not blocked or just a request)
It gives the opportunity to show mail adresses of friends who indicates it on their profile
'''
ALL_GENERAL_FRIENDS = False
ALL_GENERAL_ELSE = False 

class FacebookFriendsReader(Reader):
    def read(self): 
        '''
        This function returns a dataframe containing the date of frienship and (if wanted) the name of the friend
        --> the same structure is used for all 'type of friend interactions' so this function can be used for 
            all of them 
        --> for doing so type_data has to be introduced (name of the columns read by read_json: 'friends','received_requests'
            'rejected_requests','deleted_friends', 'sent_requests') this will also be the type of data in the main 
            dataframe
        --> the 'simple' friends.json add the email address of some friends, can be added with friends_with_contacts
        '''
        text = self.path
        data = pd.read_json(self.path, encoding = 'utf-8')
        if re.search('received_friend_requests.json',text):
            label_data = 'received_requests'
            
        elif re.search('rejected_friend_requests.json',text):
            label_data = 'rejected_requests'
            
        elif re.search('removed_friends',text):
            label_data = 'deleted_friends'
        
        elif re.search('sent_friend_requests.json',text):
            label_data = 'sent_requests'
            
        else:
            label_data = 'friends'
            
        df = pd.DataFrame(list(data[label_data]))
        df['date'] = df['timestamp']
        main_df = main_transfo_timestamp_10(df, 'Facebook', label_data)
        
        if ALL_INDEX:
            main_df['name'] = df['name']
            main_df = main_df[['date','type','label','name','Year','Month','Day','Hour']]
        
        if FRIENDS_WITH_CONTACTS:
            df1 = df[df['contact_info'].notna()]
            main_df = main_transfo_timestamp_10(df1, 'Facebook', 'friend')
            main_df['name'] = df1['name']
            main_df['email'] = df1['contact_info']
            main_df = main_df[['date','type','label','name','email','Year','Month','Day','Hour']]
        
        if ALL_GENERAL_FRIENDS:
            main_df['name'] = df.name
            main_df['content'] = df.contact_info
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        if ALL_GENERAL_ELSE:
            main_df['name'] = df.name
            main_df['content'] = df.name.apply(lambda x: 'NaN')
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df