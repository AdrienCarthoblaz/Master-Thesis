import pandas as pd 
import re
import json
from datetime import datetime, date, time
from Package.reader import Reader

ALL_INDEX = False
ALL_GENERAL = False

class SnapchatLocationHistoryReader(Reader):
    def get_adict_local_history(self, path):
        '''
        The json file containing location history conained multiple kinds of information, this function returned 
        a 'brut' dictionary from the json file
        '''
        with open(path, encoding = 'utf-8') as json_data:
            data = json.load(json_data)
        
        outputdict = {}
        for key, value in data.items():
            outputdict[key] = outputdict.get(key, []) + [value]
        
        return outputdict
    
    def read(self):
        '''
        This function returns a dataframe from the column 'Locations History' in the brut dictionary:
        --> snapchat stocks the latitude and the longitude in the same value of the dictionary, a regex is used 
            to find propers latitude and longitude and create two lists from them. These lists are used as columns
            in the dataframe 
        --> the rest is quite the same "as usual" but it's worth noticing the change of format date (ie: / instead 
            of - )
        '''
        
        dic = self.get_adict_local_history(self.path)
        
        data_2 = dic['Locations History']
        outputdict_2 = {}
        for lis in data_2:
            for dic in lis:
                for k2, v2 in dic.items():
                    outputdict_2[k2] = outputdict_2.get(k2, []) + [v2]
        
        regex = r'([\d]*[\.][\d]{3})'
        latitude = []
        longitude = []
        for i in outputdict_2['Latitude, Longitude']:
            match = re.findall(regex, i)
            latitude.append(match[0])
            longitude.append(match[1])
        
        df = pd.DataFrame.from_dict(outputdict_2)
        
        df['latitude'] = latitude
        df['longitude'] = longitude
        
        df['date'] = df['Time']
        date_format = '%Y/%m/%d %H:%M:%S UTC'
        df['date'] = df.date.apply(lambda t: datetime.strptime(t, date_format))
        df['Year'] = df.date.apply(lambda x: x.year)
        df['Month'] = df.date.apply(lambda x: x.month)
        df['Day'] = df.date.apply(lambda x: x.day)
        df['Hour'] = df.date.apply(lambda x: x.hour)
        
        df['type'] = df.date.apply(lambda x: 'Snapchat')
        df['label'] = df.date.apply(lambda x: 'location')
        
        df['name']=df.latitude
        df['content']=df.longitude
        
        main_df = df[['date','type','label','Year','Month','Day','Hour']]
        
        if ALL_INDEX:
            main_df = df[['date','type','label','latitude','longitude','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df = df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df
            