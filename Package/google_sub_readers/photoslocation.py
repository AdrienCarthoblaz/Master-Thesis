import os
from Package.reader import Reader
import pandas as pd 
from datetime import datetime, date, time

class GooglePhotoLocationReader(Reader):
    def read(self):
        '''Return a dataframe of pictures/movies which have geolocalisation coordinates
        '''
        list_dir = os.listdir(self.path)
        for l in list_dir[:1]:
            for f in os.listdir(self.path+l):
                if f.endswith(".json") and f.startswith("DSC"):
                    main_df = pd.read_json(self.path+l+"/"+f)
                    main_df = pd.DataFrame(main_df, index=['timestamp','formatted','latitude','longitude','altitude',\
                                                       'latitudeSpan','longitudeSpan'])
                    main_df = main_df.drop(['timestamp','formatted','altitude','latitudeSpan','longitudeSpan'])
        for l in list_dir[1:]:
            for f in os.listdir(self.path+l):
                if f.endswith((".json",".mov")) and f.startswith(("DSC","Screenshot","MOV","2014","2015","IMG")):
                    df = pd.read_json(self.path+l+"/"+f)
                    df = pd.DataFrame(df, index=['timestamp','formatted','latitude','longitude','altitude',\
                                             'latitudeSpan','longitudeSpan'])
                    df = df.drop(['timestamp','formatted','altitude','latitudeSpan','longitudeSpan'])
                
                    main_df = pd.concat([main_df,df])
                    main_df = main_df[["title","geoData"]]
                
        main_df = main_df[main_df.geoData.values != 0]
    
        ''' At this point the returned dataframe is not really convenient, so has to be transformed into a dataframe
            with the name of the file, latitude and longitude: 
        
            1) get values contains in geodata (operate a sort between latitude and longitude, if > 40 it's a
               latitude, all my pictures were taken in the northern hemisphere it has to be changed if user is 
               elsewhere) and put them into a list, same for file name
            2) list of filename contains duplicate (ie in the "raw" dataframe returned above the same file appears two 
               times once for latitude once for longitude), transform it into a dict will not allow twice the same key
            3) create a new dataframe from the 3 dictionnaries
        
        '''
    
        list_latitude = []
        list_longitude = []
        list_name = []
    
        for i in main_df.iterrows(): 
            if i[1][1] > 40:
                list_latitude.append(i[1][1])
            else:
                list_longitude.append(i[1][1])

        for i in main_df.iterrows(): 
            list_name.append(i[1][0])
        
        list_name = list(dict.fromkeys(list_name))

        d = {'title':list_name,'latitude':list_latitude,'longitude':list_longitude}
        new_df = pd.DataFrame(d)
        
        main_dataframe = self.main_dataframe_creator(self.path)
        geo_location_dataframe = self.add_date(main_dataframe, new_df)
        
        self.df = geo_location_dataframe 
    
    def add_date(self, main_dataframe,geo_dataframe):
        ''' Add the date and "clean it" to the geodataframe by comparing file name (title) from the main dataframe and the
        geodataframe.
        --> nb: here the loop begin at row 35 because some files had the same names
        --> nb: maybe was it feasible to do it directly in geodatamerger, but this solution works
        
        '''
        list_date = []
        new_geodataframe = geo_dataframe.copy()
        for i in main_dataframe.astype(str).iloc[35:].iterrows():
            for j in geo_dataframe.astype(str).iterrows(): 
                if i[1][3] ==  j[1][0]:
                    list_date.append(i[1][0])
    
        new_geodataframe['date'] = list_date
        date_format = '%Y-%m-%d %H:%M:%S'
        new_geodataframe['date'] = new_geodataframe.date.apply(lambda t: datetime.strptime(t, date_format)) 
        new_geodataframe['Year'] = new_geodataframe.date.apply(lambda x: x.year)
        new_geodataframe['Month'] = new_geodataframe.date.apply(lambda x: x.month)
        new_geodataframe['Day'] = new_geodataframe.date.apply(lambda x: x.day)
        new_geodataframe['Hour'] = new_geodataframe.date.apply(lambda x: x.hour)
    
        new_geodataframe['type']= new_geodataframe.date.apply(lambda x: 'Google')
        new_geodataframe['label']= new_geodataframe.date.apply(lambda x: 'picture loc')
    
        new_geodataframe = new_geodataframe[["date",'type','label',"title",'latitude','longitude','Year','Month','Day','Hour']]
        new_geodataframe.sort_values(["date"],axis=0,ascending=True,inplace=True)
    
        return new_geodataframe
    
    def main_dataframe_creator(self, path):
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
        list_dir = os.listdir(path)
        for l in list_dir[:1]:
            for f in os.listdir(path+l):
                if f.endswith(".json") and f.startswith("DSC"):
                    df1 = pd.read_json(path+l+"/"+f)
                    df1 = pd.DataFrame(df1, index=['timestamp','formatted','latitude','longitude','altitude',\
                                                   'latitudeSpan','longitudeSpan'])
                    df1 = df1.drop(['formatted','latitude','longitude','altitude','latitudeSpan','longitudeSpan'])
                    df1 = df1.rename(index={'timestamp': '1'})
        for l in list_dir[1:]:
            for f in os.listdir(path+l):
                if f.endswith((".json",".mov")) and f.startswith(("DSC","Screenshot","MOV","2014","2015","IMG")):
                    df = pd.read_json(path+l+"/"+f)
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
        
        main_df = df1[["date",'type','label',"title",'Year','Month','Day','Hour']]
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        return main_df 