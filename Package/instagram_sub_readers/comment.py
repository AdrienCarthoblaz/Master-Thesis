import pandas as pd 
from dateutil import *
import json
from Package.reader import Reader
from datetime import datetime, date, time

ME = 'Enter your Instagram pseudo here'
ALL_INDEX = False
ALL_GENERAL = False

class InstagramCommentReader(Reader):
    def read(self):
        with open(self.path, encoding = 'utf-8') as json_data:
            data = json.load(json_data)
        
        outputdict = {}
        for key, value in data.items():
            outputdict[key] = outputdict.get(key, []) + [value] 
    
        outputdict.pop('live_comments',None)
        outputdict.pop('story_comments',None)
        
        df = pd.DataFrame.from_dict(outputdict)
        
        list_date = []
        list_msg = []
        list_name = []
    
        for i in df.iterrows():
            for lis in i[1][0]:
                list_date.append(lis[0])
                list_msg.append(lis[1])
                list_name.append(lis[2])
        
        df1 = pd.DataFrame(list(zip(list_date,list_name)), columns=['date','name'])
        df1['msg'] = list_msg
        df1['date'] = df1.date.apply(lambda t: parser.isoparse(t))
        df1['date']= df1.date.dt.tz_localize(None)
        df1['date'] = pd.to_datetime(df1['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        date_format = '%Y-%m-%d %H:%M:%S'
        df1['date'] = df1.date.apply(lambda t: datetime.strptime(t, date_format)) 
        df1['Year'] = df1.date.apply(lambda x: x.year)
        df1['Month'] = df1.date.apply(lambda x: x.month)
        df1['Day'] = df1.date.apply(lambda x: x.day)
        df1['Hour'] = df1.date.apply(lambda x: x.hour)
        
        df1['label'] = df1.name.apply(lambda x: 'own comment' if x==ME else 'friend comment')
        df1['type'] = df1.name.apply(lambda x: 'Instagram')
        
        main_df = df1[["date",'type','label','Year','Month','Day','Hour']]
        
        if ALL_INDEX:
            main_df = df1[["date",'type','label','name','msg','Year','Month','Day','Hour']]
        if ALL_GENERAL:
            main_df['name'] = df1.name
            main_df['content'] = df1.msg
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df 