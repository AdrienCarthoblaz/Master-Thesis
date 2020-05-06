import pandas as pd 
from Package.reader import Reader
from datetime import datetime, date, time
from Package.facebook_sub_readers.date_transformers import main_transfo_timestamp_10
from Package.facebook_sub_readers.own_post_transformers import gen, lists_creator

ALL_GENERAL = False
ALL_INDEX = False

class FacebookPostForSaleItemReader(Reader):
    def read(self):
        '''
        Same process as most of function above but for items saled on Facebook.
        '''
        df = pd.read_json(self.path, convert_dates = False, encoding='utf-8')
        df = df[df['attachments'].notna()]
        
        returned = lists_creator(df,'for_sale_item')
        list_date = returned[0]
        list_att = returned[1]
        
        outputdict = {}
        for lis in list_att:
            for lis_2 in lis:
                for key, value in lis_2.items():
                    for lis_3 in value: 
                        for k2, v2 in lis_3.items():
                            for k3, v3 in v2.items():
                                if isinstance (v3, dict):
                                    for k4, v4 in v3.items():
                                        if isinstance(v4, dict):
                                            for k5, v5 in v4.items():
                                                outputdict[k5] = outputdict.get(k5, []) + [v5]
                                    
                                        else:
                                            outputdict[k4] = outputdict.get(k4, []) + [v4] 
                                else:
                                    outputdict[k3] = outputdict.get(k3, []) + [v3] 
        outputdict.pop('description',None)
        outputdict.pop('title')
    
        df1 = pd.DataFrame.from_dict(outputdict)
        df1['date'] = list_date
        main_df = main_transfo_timestamp_10(df1, 'Facebook', 'for sale item')
    
        if ALL_INDEX:
            main_df['price'] = df1['price']
            main_df['seller']=df1['price']
            main_df['category']=df1['category']
            main_df['marketplace']=df1['marketplace']
            main_df['location']=df1['name']
            main_df['latitude']=df1['latitude']
            main_df['longitude']=df1['longitude']
            main_df['uri']=df1['uri']
            main_df['ip']=df1['upload_ip']
            main_df = main_df[['date','type','label','price','seller','category','marketplace',\
                               'location','latitude','longitude','uri','ip','Year','Month','Day','Hour']]
        if ALL_GENERAL:
            main_df['name'] = df1.marketplace
            main_df['content'] = df1.uri
            main_df = main_df[['date','type','label','name','content','Year','Month','Day','Hour']]
        
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
    
        self.df = main_df