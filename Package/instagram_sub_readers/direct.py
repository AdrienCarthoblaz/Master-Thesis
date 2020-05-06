import pandas as pd 
import ast
from dateutil import *
import json
from Package.reader import Reader
from datetime import datetime, date, time

ALL_INDEX = False
ALL_GENERAL = False

class InstagramDirectReader(Reader):
    def read(self):
        '''
        As the data concerning direct pictures was cut in half during downloading (3 zip files), the json files 
        containing only direct pictures has to be treated separately (the main def was built to find the key words,
        these ones won't be found as they don't exist in the file --> may be concerning if used in other context,
        i.e. if the user has more files and everything has to be treated separetely)
        
        '''
        with open(self.path, 'r', encoding='utf-8') as f:
            df = pd.DataFrame(f)
        
        data = df.values
        
        for niv1 in data:
            for niv2 in niv1:
                string_data = niv2
        
        dic = ast.literal_eval(string_data)
        values = dic.get("direct")
        
        outputdict = {}
        for dic in values:
            for key, value in dic.items():
                outputdict[key] = outputdict.get(key, []) + [value]
        
        main_df = pd.DataFrame.from_dict(outputdict)
        main_df['date']=main_df['taken_at'].apply(lambda t: parser.isoparse(t))
        main_df['date']= main_df.date.dt.tz_localize(None)
        main_df['date'] = pd.to_datetime(main_df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        date_format = '%Y-%m-%d %H:%M:%S'
        main_df['date'] = main_df.date.apply(lambda t: datetime.strptime(t, date_format)) 
        main_df['Year'] = main_df.date.apply(lambda x: x.year)
        main_df['Month'] = main_df.date.apply(lambda x: x.month)
        main_df['Day'] = main_df.date.apply(lambda x: x.day)
        main_df['Hour'] = main_df.date.apply(lambda x: x.hour)
        
        main_df['label'] = main_df.date.apply(lambda x: 'direct')
        main_df['type'] = main_df.date.apply(lambda x: 'Instagram')
        
        main_df['name'] = main_df.date.apply(lambda x: 'NaN')
        
        main_df1 = main_df[["date",'type','label','Year','Month','Day','Hour']]
        
        if ALL_INDEX:
            main_df1 = main_df[["date",'type','label','path','Year','Month','Day','Hour']]
        
        if ALL_GENERAL: 
            main_df1['name'] = main_df.name
            main_df1['content'] = main_df.path
            main_df1 = main_df1[['date','type','label','name','content','Year','Month','Day','Hour']]
            
        main_df1.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df1