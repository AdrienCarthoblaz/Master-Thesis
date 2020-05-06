import pandas as pd 
import json
from datetime import datetime, date, time
from Package.reader import Reader

ALL_INDEX = False
ALL_GENERAL = False

class SnapchatLocationLastTwoYears(Reader):
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
        This function returns a dataframe from the column 'Areas you may have visited in the last two years' in the
        brut dictionary:
        --> note the location is imprecise but the postal code lead to the right place 
        '''
        
        dic = self.get_adict_local_history(self.path)
        
        data_2 = dic['Areas you may have visited in the last two years']
        outputdict_2 = {}
        for lis in data_2:
            for dic in lis:
                for k2, v2 in dic.items():
                    outputdict_2[k2] = outputdict_2.get(k2, []) + [v2]
        
        df = pd.DataFrame.from_dict(outputdict_2)
        
        df['date'] = df['Time']
        date_format = '%Y/%m/%d %H:%M:%S UTC'
        df['date'] = df.date.apply(lambda t: datetime.strptime(t, date_format))
        df['Year'] = df.date.apply(lambda x: x.year)
        df['Month'] = df.date.apply(lambda x: x.month)
        df['Day'] = df.date.apply(lambda x: x.day)
        df['Hour'] = df.date.apply(lambda x: x.hour)
        
        df['type'] = df.date.apply(lambda x: 'Snapchat')
        df['label'] = df.date.apply(lambda x: 'location')
        
        df['name'] = df.City
        df['content'] = df['Postal Code']
        
        main_df = df[['date','type','label','Year','Month','Day','Hour']]
        
        if ALL_INDEX:
            main_df['city'] = df['City']
            main_df['region'] = df['Region']
            main_df['postal code'] = df['Postal Code']
            main_df = main_df[['date','type','label','city','region','postal code','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df = df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df
        