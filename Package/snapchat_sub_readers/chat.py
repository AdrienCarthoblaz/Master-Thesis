import pandas as pd
import json
from datetime import datetime, date, time
from Package.reader import Reader

ALL_INDEX = False
ALL_GENERAL = False 

class SnapchatChatReader(Reader):
    def read(self):
        '''
        This function returns a dataframe from snapchat's json file named 'chathistory.json':
        --> chat can be from the user (ie sent) or from friends (ie received), this is taken into account in the
            label section
        --> name of friend sending the chat is stocked and can be accessed with the all_index argument
        --> the date is a string in no particular format (no format seen until now in this project), it's cleaned and
            returned into a datetime format
        '''
        with open(self.path, encoding = 'utf-8') as json_data:
            data = json.load(json_data)
        
        outputdict = {'label':[],'name':[]}
        for key, value in data.items():
            for lis in value:
                for k2, v2 in lis.items():
                    if k2 == 'From':
                        outputdict.setdefault('label', []).append('received chat')
                        outputdict.setdefault('name', []).append(v2)
                    elif k2 == 'To':
                        outputdict.setdefault('label', []).append('sent chat')
                        outputdict.setdefault('name', []).append(v2)
                    else:
                        outputdict[k2] = outputdict.get(k2, []) + [v2]
                        
        df = pd.DataFrame.from_dict(outputdict)
        date_format = '%Y-%m-%d %H:%M:%S UTC'
        df['date'] = df['Created']
        df['date'] = df.date.apply(lambda t: datetime.strptime(t, date_format))
        df['Year'] = df.date.apply(lambda x: x.year)
        df['Month'] = df.date.apply(lambda x: x.month)
        df['Day'] = df.date.apply(lambda x: x.day)
        df['Hour'] = df.date.apply(lambda x: x.hour)
        
        df['type'] = df.date.apply(lambda x: 'Snapchat')
        
        df['content'] = df['Media Type']
        
        main_df = df[['date','type','label','Year','Month','Day','Hour']]
        
        if ALL_INDEX:
            main_df = df[['date','type','label','name','media type','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df = df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df