import os
import pandas as pd
from datetime import *
from dateutil import *
from Package.reader import Reader

COMBOX = '0000000000000'
ALL_INDEX = False
ALL_GENERAL = False

class SwisscomReader(Reader):
    def read(self):
        list_dir_swisscom = os.listdir(self.path)
        list_dir_tot_swisscom = []
        for l in list_dir_swisscom[:]:
            x = self.path + '/' + str(l)
            list_dir_tot_swisscom.append(x)

        self.df = self.datamerger(list_dir_tot_swisscom, False, False)

    def proc_data(self, data, all_index=False, all_general=False):
        ''' read Swisscom excel file and return a panda dataframe
        --> drop NaN value in the "Vers" column (Swisscom does a statistic of the number of KB used per day everyday
            at midnight, these statistics are not usefull in this project, dropping these missing value solve these
            issues)
        --> concatenate date column and hour column into one
        --> create dedicated columns where date is split, more convenient for futher statistics
        --> type and label( call, sms, combox): will be useful for visualization 
            --> .apply(lambda x: 'sms' if x==1 else 'call') in 'Durée/Quantité/KB' if theres is a 1 it means that a 
                sms has been sent 
            --> mask = (main_df['Vers'] == '0860799034915') & (main_df['label'] == 'call'): boolean mask to flag
                recieved combox call, relabelled 'combox'
        '''
    
        df = pd.read_excel(data, converters={'Vers':str})
        df = df[df['Vers'].notna()]
        
        df['date']=df['Date'].astype(str)+' à '+df['Heure'].astype(str)
        date_format = '%Y-%m-%d à %H:%M:%S'
        df['date'] = df.date.apply(lambda t: datetime.strptime(t, date_format))
        df['Year'] = df.date.apply(lambda x: x.year)
        df['Month'] = df.date.apply(lambda x: x.month)
        df['Day'] = df.date.apply(lambda x: x.day)
        df['Hour'] = df.date.apply(lambda x: x.hour)
        
        df['type']= df.date.apply(lambda x: 'Swisscom')
        df['label']= df['Durée/Quantité/KB'].apply(lambda x: 'sms' if x==1 else 'call')
        
        mask = (df['Vers'] == COMBOX) & (df['label'] == 'call')
        df['label'][mask] = 'combox'
        
        df['name']=df.Vers
        df['content']=df['Durée/Quantité/KB']
        
        main_df = df[["date",'type','label',"Year","Month","Day","Hour"]]
        
        if ALL_INDEX:
            main_df['Vers'] = df['Vers']
            main_df['Durée/Quantité'] = df['Durée/Quantité/KB']
            main_df = main_df[["date",'type','label',"Vers","Durée/Quantité","Year","Month","Day","Hour"]]
            
        if ALL_GENERAL:
            main_df = df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        return main_df

    def datamerger(self, path, all_index=False, all_general=False):
        ''' Merge all files into one dataframe (ie read all files in the given file and concatenate them)
        --> sort values in chronological order 
        '''
        df = self.proc_data(path[0], all_index, all_general)
        for l in path[1:]:
            x = self.proc_data(l, all_index, all_general)
            main_df = pd.concat([df,x])
            df = main_df
        df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        return df
