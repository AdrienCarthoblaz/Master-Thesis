import os
from Package.reader import Reader
import pandas as pd 
from datetime import datetime, date, time

ALL_INDEX = False
ALL_GENERAL = False

class GooglePhotoReader(Reader):
    def read(self):
        ''' Given the path to google_photo (attention has to be renamed manually to avoid the space): 
            will go through all json file containing all data about the picture or the movie.
            
        ---> twice the same loop, the first to get the first entry and then to concatenate (not efficient but
            working)
            1) Startswith : nb: the name of the saved picture depends on the brand of the phone (Ie. samsung 
                                beginning of 2015, sony most of other years) --> DSC, IMG, 2014,2015
                            nb: screenshot to take into account the screenshots saved on google photo
                            nb: MOV to take into account movies, same for endswith .mov
            2) Rename index in order to be able to drop the ones which are not of used + rename timestamp into
                a counter 
            3) Transformation of the timestamp (10 digits) into a datetime (nb new way of doing it)
        
        '''
        i = 2
        list_dir = os.listdir(self.path)
        for l in list_dir[:1]:
            for f in os.listdir(self.path+l):
                if f.endswith(".json") and f.startswith("DSC"):
                    df1 = pd.read_json(self.path+l+"/"+f)
                    df1 = pd.DataFrame(df1, index=['timestamp','formatted','latitude','longitude','altitude',\
                                                   'latitudeSpan','longitudeSpan'])
                    df1 = df1.drop(['formatted','latitude','longitude','altitude','latitudeSpan','longitudeSpan'])
                    df1 = df1.rename(index={'timestamp': '1'})
        for l in list_dir[1:]:
            for f in os.listdir(self.path+l):
                if f.endswith((".json",".mov")) and f.startswith(("DSC","Screenshot","MOV","2014","2015","IMG")):
                    df = pd.read_json(self.path+l+"/"+f)
                    df = pd.DataFrame(df, index=['timestamp','formatted','latitude','longitude','altitude',\
                                                 'latitudeSpan','longitudeSpan'])
                    df = df.drop(['formatted','latitude','longitude','altitude','latitudeSpan','longitudeSpan'])
                    df = df.rename(index={'timestamp': i })
                    
                    df1 = pd.concat([df1,df])
                    i = i+1
                    
        df1['date'] = df1['photoTakenTime'].astype(int)
        df1['date'] = df1.date.apply(lambda x : pd.to_datetime(x, unit='s'))
        df1['Year'] = df1.date.apply(lambda x: x.year)
        df1['Month'] = df1.date.apply(lambda x: x.month)
        df1['Day'] = df1.date.apply(lambda x: x.day)
        df1['Hour'] = df1.date.apply(lambda x: x.hour)
        
        df1['type']= df1.date.apply(lambda x: 'Google')
        df1['label']= df1.date.apply(lambda x: 'picture')
        
        df1['name'] = df1.date.apply(lambda x: 'NaN')
        df1['content'] = df1.title
        
        main_df = df1[["date",'type','label','Year','Month','Day','Hour']]
        
        
        if ALL_INDEX:
            main_df = df1[["date",'type','label',"title",'Year','Month','Day','Hour']]
        if ALL_GENERAL:
            main_df = df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df 
