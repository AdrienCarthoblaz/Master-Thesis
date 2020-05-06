from Package.reader import Reader
from datetime import datetime, date, time
from dateutil import *
import pandas as pd

ALL_INDEX = False
ALL_GENERAL = False

class GoogleAppsReader(Reader):
    def read(self):
        ''' Read json file and give a panda dataframe cleaned 
        ---> encoding utf-8 to avoid special character not readable (é, ü etc...)
        ---> all nested dictionnaries (ie. each app) is put in a list 
        ---> the dataframe is constructed from the returned dictionnary from dropnested
        ---> parser.isoparse transform ISO 8601 in a datetime
        ---> tz_localize erase the time zone returned by isoparse 
        ---> strftime return a date in string which is transform into the datetime format we want to use '''
        list_dict = []
        data = pd.read_json(self.path, encoding='utf-8')
        
        for t in data.iterrows():
            d = dict(t[1])
            list_dict.append(d)
        df = pd.DataFrame.from_dict(self.dropnested(list_dict))
        
        df['date']=df['acquisitionTime'].apply(lambda t: parser.isoparse(t))
        df['date']= df.date.dt.tz_localize(None)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        date_format = '%Y-%m-%d %H:%M:%S'
        df['date'] = df.date.apply(lambda t: datetime.strptime(t, date_format)) 
        df['Year'] = df.date.apply(lambda x: x.year)
        df['Month'] = df.date.apply(lambda x: x.month)
        df['Day'] = df.date.apply(lambda x: x.day)
        df['Hour'] = df.date.apply(lambda x: x.hour)
        
        df['type']= df.date.apply(lambda x: 'Google')
        df['label']= df.date.apply(lambda x: 'app installed')
        
        df['name'] = df.title
        df['content'] = df.title.apply(lambda x: 'NaN')
        
        main_df = df[["date",'type','label','Year','Month','Day','Hour']]
        
        if ALL_INDEX:
            main_df = df[["date",'type','label',"title",'Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df = df[['date','type','label','name','content','Year','Month','Day','Hour']]
            
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df


    def dropnested(self, alist):
        ''' Library.json which is given when you download your Google data is presented as a nested dictionnary
        ---> this function give a dictionnary of all nested dictionnaries contained in a list
        ---> the idea is the following if the value of a dictionnary is still a dictionnary go one step further in
            order to "break" all nested dictionnaries
        '''
        outputdict = {}
        for dic in alist:
            for key, value in dic.items():
                if isinstance(value, dict):
                    for k2, v2 in value.items():
                        if isinstance(v2, dict):
                            for k3, v3, in v2.items():
                                outputdict[k3] = outputdict.get(k3, []) + [v3]
                        else: 
                            outputdict[k2] = outputdict.get(k2, []) + [v2]
                else:
                    outputdict[key] = outputdict.get(key, []) + [value]
        return outputdict  
