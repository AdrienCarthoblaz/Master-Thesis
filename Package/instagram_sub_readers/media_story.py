import pandas as pd 
import ast
from dateutil import *
import json
from Package.reader import Reader
from datetime import datetime, date, time

ALL_INDEX = False
ALL_GENERAL = False

class InstagramStoryReader(Reader):
    def get_values(self, path): 
        '''
        1) The json file containing information about pictures on instagram contains all the information for stories,
        photos, profile and direct. This leads to the impossibility to open it with pd.read_json. This function 
        opens the file the "hard way" given the path. From the opened file a dataframe (1x1) is outputed. Values are
        extracted from it and putted in list as str. This str list is split to get a list of words.
        2) As the file contains four types of informations, this function searches where the keys (photos, profile,
        direct) are located and returned an index from it.
        '''
        with open(path, 'r', encoding='utf-8') as f:
            df = pd.DataFrame(f)
        
        data = df.values
        
        for niv1 in data:
            for niv2 in niv1:
                string_data = niv2
        
        list_word = string_data.split()
        index = [list_word.index('"photos":'),list_word.index('"profile":'),list_word.index('"direct":')]
        
        return list_word, index 
    
    def read(self):
        '''
        1) From a the returned list of words, a sub-list of words is created, this one concerns the data linked to 
        stories. Then the list is "reattached" as string list. 
        2) The string list is transformed to be able to read it as a dictionary (ast.literal_eval)
            --> the last coma is dropped and a '}' is added in order to close the "wanna be" dictionary
        3) The dictionary obtained is sorted by useful keys and transformed as "usual" (iso --> datetime/type/label)
        '''
        returned = self.get_values(self.path)
        data = returned[0]
        index = returned[1]
        
        list_stories = []
        for i in data[:index[0]]:
            list_stories.append(i)
            
        string_words = ''
        
        for i in list_stories:
            word = i 
            string_words = str(string_words) + str(word)
        
        string_words = string_words[:-1]
        string_words = str(string_words) + str('}')
        
        dic = ast.literal_eval(string_words)
        values = dic.get("stories")
        
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
        
        main_df['label'] = main_df.date.apply(lambda x: 'story')
        main_df['type'] = main_df.date.apply(lambda x: 'Instagram')
        
        main_df1 = main_df[["date",'type','label','Year','Month','Day','Hour']]
        
        if ALL_INDEX:
            main_df1 = main_df[["date",'type','label','caption','path','Year','Month','Day','Hour']]
        
        if ALL_GENERAL:
            main_df1['name'] = main_df.caption
            main_df1['content'] = main_df.path
            main_df1 = main_df1[['date','type','label','name','content','Year','Month','Day','Hour']]
            
        main_df1.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df1