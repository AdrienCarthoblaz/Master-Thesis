import pandas as pd 
from dateutil import *
import json
from Package.reader import Reader
from datetime import datetime, date, time

ALL_INDEX = False
ALL_GENERAL = False
ME = 'Enter your Instagram pseudo here'

class InstagramMessageReader(Reader):
    def read(self):
        '''
        The dataframe given by a "naive" pd.read_json contains two columns: participants (ex: [nrfmf,j.carthoblaz])
        and conversation (ex: [{'sender':'nrfmf', 'created_at':2020-02-17T11:53:23.732921+00:00,'text':'Tien voir'},
        {'sender':......}]), the first column is not at used in this project and can be drop as all relevant informations
        are contained in the second column. 
        --> open the json file the 'hardway'
        --> create dictionaries from dictionaries inside the list
        --> treatment of values contained in the dictionary 
        --> there are multiple kind of messages that can be sent so everything is stored into a column
            nb: sometimes multiple things are sent within the same timestamps, only the first entry is kept(loss of 
            information but forced to keep the arrays the same size)
        --> date is in ISO 8601 format, it's tranformed in a datetime(ns) format
        --> a column label is created in order to know if a message as been sent or received (nb 'me' has to be 
            changed depending of the user)
        '''
        with open(self.path, encoding = 'utf-8') as json_data:
            data = json.load(json_data)
        
        outputdict = {}
        for lis in data:
            for key, value in lis.items():
                outputdict[key] = outputdict.get(key, []) + [value]
        outputdict.pop('participants',None)
        
        condition = ''
        condition_2 = False
        dictionary = {'content':[]}
        for key, value in outputdict.items():
            for lis in value:
                for lis_2 in lis:
                    for k2, v2 in lis_2.items():
                        if condition_2 and k2 != 'sender':
                            continue
                        else:
                            if condition == 'created_at':
                                dictionary.setdefault('content', []).append(v2)
                                condition_2 = True
                            else:
                                dictionary[k2] = dictionary.get(k2, []) + [v2]
                                condition_2 = False
                    
                        condition = k2
        
            
        
        df = pd.DataFrame.from_dict(dictionary)
        df['date']= df['created_at'].apply(lambda t: parser.isoparse(t))
        df['date']= df.date.dt.tz_localize(None)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        date_format = '%Y-%m-%d %H:%M:%S'
        df['date'] = df.date.apply(lambda t: datetime.strptime(t, date_format)) 
        df['Year'] = df.date.apply(lambda x: x.year)
        df['Month'] = df.date.apply(lambda x: x.month)
        df['Day'] = df.date.apply(lambda x: x.day)
        df['Hour'] = df.date.apply(lambda x: x.hour)
        
        df['label'] = df.sender.apply(lambda x: 'msg sent' if x==ME else 'msg received')
        df['type'] = df.sender.apply(lambda x: 'Instagram')
        
        main_df = df[["date",'type','label','Year','Month','Day','Hour']]
        
        if ALL_INDEX:
            main_df = df[["date",'type','label',"sender",'content','Year','Month','Day','Hour']]
        
        
        if ALL_GENERAL:
            main_df['name'] = df.sender
            main_df['content'] = df.content
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df 