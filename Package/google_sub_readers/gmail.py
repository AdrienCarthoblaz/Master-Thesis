'''
Most of this code is inspired by Justin Ellis and can be found at this address :
https://jellis18.github.io/post/2018-01-17-mail-analysis/

Note before running this code use the proc_gmail_csv in order to get a csv file from the mbox file 
'''
import os
import re
import pandas as pd 
import mailbox 
import csv
from datetime import datetime, date, time
from Package.reader import Reader

ALL_INDEX = False
ALL_GENERAL = False 
ME = 'Enter your gmail address here'

def proc_gmail_csv(path):
    '''
    Create a csv file from the mbox file provided by google, it's easier to manipulate later  
    '''
    mbox = mailbox.mbox(path)
    
    with open("mbox.csv","w",encoding='utf-8') as outfile: 
        writer = csv.writer(outfile)
        for messages in mbox: 
            writer.writerow([messages['subject'],messages['from'],messages['date'],messages['to'],\
                             messages['X-Gmail-Labels'],messages['X-GM-THRID']])

class GmailReader(Reader):
    def read(self):
        '''
        Read csv file from google mapbox and clean it : 
        ---> transform the date (ex: Fri, 07 Feb 2020 08:45:35-0800) into a regular datetime64(ns)
        ---> transform the from column only keeping the mail address 
        ---> create a label column saying if the mail was sent or received
        
        ??? Not important in this project but how is it possible to avoid the subject name from "crashing"
        '''
        df = pd.read_csv(self.path, names=['subject','from','date','to','label','thread'])
        df['date'] = df.date.apply(lambda x: pd.to_datetime(x, errors='coerce', utc=True))
        df = df[df['date'].notna()]
        date_format= '%Y-%m-%d %H:%M:%S+00:00'
        df['date']=df.date.astype(str).apply(lambda t: datetime.strptime(t, date_format))
        df['Year'] = df.date.apply(lambda x: x.year)
        df['Month'] = df.date.apply(lambda x: x.month)
        df['Day'] = df.date.apply(lambda x: x.day)
        df['Hour'] = df.date.apply(lambda x: x.hour)
    
        
        df['type'] = df.date.apply(lambda x: 'Google')
        df['from'] = df['from'].apply(lambda x: self.get_email_address(x))
        df['name'] = df['from']
        df['label'] = df['from'].apply(lambda x: 'mail sent' if x==ME else 'mail inbox')
        df['content'] = df.subject
        
        main_df = df[['date','type','label','Year','Month','Day','Hour']]
        
        if ALL_INDEX:
            main_df = df[['date','type','label','from','subject','to','Year','Month','Day','Hour']]
        if ALL_GENERAL:
            main_df = df[['date','type','label','name','content','Year','Month','Day','Hour']]
            
        main_df.sort_values(["date"],axis=0,ascending=True,inplace=True)
        
        self.df = main_df
            
    def get_email_address(self, string):
        '''
        find email addresses between < > typically used in mail, usefull to label mail 
        '''
    
        email = re.findall(r'<(.+?)>', string)
        if not email:
            email = list(filter(lambda y: '@' in y, string.split()))
        return email[0] if email else np.NAN
