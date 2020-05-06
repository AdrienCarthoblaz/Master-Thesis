import pandas as pd 
import ast
from dateutil import *
import json
from Package.reader import Reader
from datetime import datetime, date, time

ALL_INDEX = False
ALL_GENERAL = False

class InstagramConnectionReader(Reader):
    def get_and_concat_dataframe(self, data):
        '''
        This function perform the following operations in order to transform data into a dataframe:
            --> data are ordrered by str(dictionaries) (ie following, blocked_users etc...) into a list
            --> ast.litteral_eval recognise the list as a dictionnary 
            --> from this dictionnary with collect keys, these one will be labels in our dataframe 
            --> for each dictionnaries we collect the date and the user and put them in a list 
            --> from the two lists obtained, we create a Dataframe (creation of the column type and label)
            --> Finally we concatenate all dataframe obtained 
        '''
        list_dict = []
        for niv1 in data : 
            for niv2 in niv1 : 
                list_dict.append(niv2)
        
        string_dict = list_dict[0]
        dictionary = ast.literal_eval(string_dict)
        
        list_index = []
        for key, value in dictionary.items():
            list_index.append(key)
        
        j = -1
    
        for i in list_index:
            j = j+1
            label = str(i)
            values = dictionary.get(i)
            if bool(values) == True: 
                list_name = []
                list_date = []
            
                for key, value in values.items():
                    list_name.append(key)
                    list_date.append(value)
                
                df = pd.DataFrame(list(zip(list_date,list_name)),columns=['date','name'])
                df['type']=df.name.apply(lambda x: 'Instagram')
                df['label']=df.name.apply(lambda x: label )
    
                if j == 0 :
                    main_df = df
                
                else :
                    main_df = pd.concat([main_df,df])
                    
        return main_df 
    
    
    
    def read(self):
        '''
        The command pd.read_json give a dataframe which is not operable and need tranformation, so the json file as
        to be open 'the hard way' and transform into a dataframe. This dataframe contains all the informations from 
        the json file into one cell. To perform operations on it, datas are sent to get_and_concat_dataframe. 
        From the received dataframe: 
            --> date format ISO 8601 is transformed into a datetime(ns)
            --> date is split in other columns to simplify further analysis 
        '''
        
        with open(self.path, 'r', encoding='utf-8') as f:
            df = pd.DataFrame(f)
        data = df.values
        
        main_df = self.get_and_concat_dataframe(data)
        main_df['date']=main_df.date.apply(lambda t: parser.isoparse(t))
        main_df['date']= main_df.date.dt.tz_localize(None)
        main_df['date'] = pd.to_datetime(main_df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        date_format = '%Y-%m-%d %H:%M:%S'
        main_df['date'] = main_df.date.apply(lambda t: datetime.strptime(t, date_format)) 
        main_df['Year'] = main_df.date.apply(lambda x: x.year)
        main_df['Month'] = main_df.date.apply(lambda x: x.month)
        main_df['Day'] = main_df.date.apply(lambda x: x.day)
        main_df['Hour'] = main_df.date.apply(lambda x: x.hour)
        
        main_df['content'] = main_df.date.apply(lambda x : 'NaN')
        
        
        main_df1 = main_df[["date",'type','label','Year','Month','Day','Hour']]
        
        
        if ALL_INDEX:
            main_df1 = main_df[["date",'type','label','name','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df1['name'] = main_df.name
            main_df1['content'] = main_df.content
            main_df1 = main_df1[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df1.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df1 