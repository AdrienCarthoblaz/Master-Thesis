import pandas as pd 
import ast
from dateutil import *
import json
from Package.reader import Reader
from datetime import datetime, date, time

ALL_INDEX = False
ALL_GENERAL = False

class InstagramLikeReader(Reader):
    def list_date(self, data):
        '''
        From the "raw" data sent this function return a list containing all the date related to a "like":
            --> data at the right level are put in a list (list of dictionaries)
            --> from this str(dictionries) ast.literal_eval recognise a dictionary 
            --> values related to 'media_likes' (ie the one of the dictionary's key) are stocked 
            --> all dates contain in values are putted in a list 
        '''
        list_dict = []
        list_date = []
        
        for niv1 in data : 
            for niv2 in niv1 : 
                list_dict.append(niv2)
                
        string_dict = list_dict[0]
        dictionary = ast.literal_eval(string_dict)
        values = dictionary.get("media_likes")
        
        for i in range(len(values)):
            list_date.append(values[i][0])
            
        return list_date 
    
    def list_like(self, data):
        '''
        Same as above but for user_pseudos 
        '''
        list_dict = []
        list_like = []
        
        for niv1 in data : 
            for niv2 in niv1 : 
                list_dict.append(niv2)
                
        string_dict = list_dict[0]
        dictionary = ast.literal_eval(string_dict)
        values = dictionary.get("media_likes")
        
        for i in range(len(values)):
            list_like.append(values[i][1])
            
        return list_like
    
    def read(self): 
        '''
        The json file about Instagram likes can't be open with the pd.read_json and has to be opened the hard way.
        Then it's tranformed into a dataframe, only one cell with all the informations contained in the json file.
        We collect all the values in data and send this to the two function above in order to get two lists (date 
        and the user behind the liked post). From the two lists a dataframe is created and the following operations
        are performed: 
            --> the format ISO 8601 is transformed into a datetime(ns)
            --> creation of two columns type and label(like) for further analysis 
        '''
        with open(self.path, 'r', encoding='utf-8') as f:
            df = pd.DataFrame(f)
        data = df.values
        
        df = pd.DataFrame(list(zip(self.list_date(data),self.list_like(data))), columns=['date','like'])
        df['date']= df.date.apply(lambda t: parser.isoparse(t))
        df['date']= df.date.dt.tz_localize(None)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        date_format = '%Y-%m-%d %H:%M:%S'
        df['date'] = df.date.apply(lambda t: datetime.strptime(t, date_format)) 
        df['Year'] = df.date.apply(lambda x: x.year)
        df['Month'] = df.date.apply(lambda x: x.month)
        df['Day'] = df.date.apply(lambda x: x.day)
        df['Hour'] = df.date.apply(lambda x: x.hour)
        
        df['label'] = df.like.apply(lambda x: 'like')
        df['type'] = df.like.apply(lambda x: 'Instagram')
        df['content'] = df.like.apply(lambda x: 'NaN')
        
        main_df = df[["date",'type','label','Year','Month','Day','Hour']]
        
        if ALL_INDEX:
            main_df = df[["date",'type','label','like','Year','Month','Day','Hour']]
            
        if ALL_GENERAL: 
            main_df['name'] = df.like
            main_df['content'] = df.content
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        
        self.df = main_df 