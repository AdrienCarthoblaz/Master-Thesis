'''
Used and modified with the authorization of C. Viaccoz
https://github.com/cedricviaccoz/WhatsAppDataAnalysis
'''

import os
import pandas as pd
import re
from datetime import datetime, date, time
from dateutil.parser import parse
from Package.reader import Reader

begin_msg_appareance = 'DD.MM.YY à HH:MM - '
begin_msg_reg = r'[0-9][0-9].[0-9][0-9].[0-9][0-9] à [0-9][0-9]:[0-9][0-9] \- '
regex = r'([\w\.]* à [\w\:]*) \- ([\w\+\ ]*): (.*)'
alt_reg = r'([^-]*) \- (.*)?'
date_format = '%d.%m.%y à %H:%M'

ME = 'Enter your WhatsApp pseudo here'
ALL_INDEX = False
ALL_GENERAL = False 

class WhatsappReader(Reader):
    def read(self):
        list_dir_wa = os.listdir(self.path)
        list_dir_tot_wa = []
        for l in list_dir_wa[:]:
            x = self.path + '/' + str(l)
            list_dir_tot_wa.append(x)
            
        self.df = self.datamerger(list_dir_tot_wa, ALL_INDEX, ALL_GENERAL)
        

    def flatten_text(self, lines):
        res = []
        for l in lines:
        #weird unicode character appearing whenever there is an "image absente" string in the text, apparently trigger a newline.
            msg = l.replace('\u200e', '')
            date_zone = msg[:len(begin_msg_appareance)]
            if re.match(begin_msg_reg, date_zone) is None:
                if len(res) > 0:
                    res[-1] = res[-1].strip() + " " + msg 
            
            else:
                res.append(msg)
        return res
        

    def extract_infos(self, text):
        if text is not '': 
            match = re.match(regex, text)
            try:
                result = [x for x in match.groups() if x and x!=text]
                return result
            except AttributeError:
            #in group system message, we need to match otherwise as there is no <name>:<msg>, but <name with action> 
            
                match = re.match(alt_reg, text)
                try:
                    result = [x for x in match.groups() if x and x != text]
                    return [result[0], 'System', '']
                except AttributeError:
                    print('String causing the error : %s'%(text))
                    return ['','','']
            
            
    def wa_data_proc(self, filename, all_index = False, all_general=False):
        '''Parse and clean the whatsapp data (without media files) 
        into a structured panda dataframe
            param : filename => relative file path of the 
                .txt file containing the messages log
        '''
        with open(filename, 'r', encoding='utf-8') as f:
            mainDf = pd.DataFrame([self.extract_infos(x) for x in self.flatten_text(f.readlines())], columns=['date', 'from',\
                                                                                                              'msg'])
            date_format = '%d.%m.%y à %H:%M'
            mainDf['date'] = mainDf.date.apply(lambda t: datetime.strptime(t, date_format))
            mainDf['Year'] = mainDf.date.apply(lambda x: x.year)
            mainDf['Month'] = mainDf.date.apply(lambda x: x.month)
            mainDf['Day'] = mainDf.date.apply(lambda x: x.day)
            mainDf['Hour'] = mainDf.date.apply(lambda x: x.hour)
        
            mainDf['type']=mainDf.date.apply(lambda x: 'WhatsApp')
            mainDf['label']=mainDf['from'].apply(lambda x: 'sent' if x == ME else 'received')
            
            mainDf['name'] = mainDf['from']
            mainDf['content'] = mainDf.msg
        
            if ALL_INDEX:
                mainDf = mainDf[['date','type','label','from','msg','Year','Month','Day','Hour']]
            
            elif ALL_GENERAL:
                mainDf = mainDf[['date','type','label','name','content','Year','Month','Day','Hour']]
        
            else:
                mainDf = mainDf[['date','type','label','Year','Month','Day','Hour']]
            
            return mainDf

    def datamerger(self, path, all_index=False, all_general=False):
        ''' Will give a dataframe with all the messages contain in all whatsapp discussion '''
    
        df = self.wa_data_proc(path[0], all_index, all_general)
    
        for l in path[1:]:
        
            x = self.wa_data_proc(l, all_index, all_general)
            main_df = pd.concat([df,x])
            df = main_df
    
        df.sort_values(["date"], axis=0, ascending=True, inplace=True)
        
        return df
