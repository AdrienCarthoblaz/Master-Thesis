def gen(alist, name):
    '''
    Return a booleen if the key of the dictionary of interest is equivalent to a certain name(ie: type of data
    in the attachments) 
    '''
    for dic in alist:
        for key, value in dic.items():
            if isinstance(value, list):
                list_dict = value[0]
                for k2, v2 in list_dict.items():
                    if k2 == name:
                        return True
                    else:
                        return False


def lists_creator(df, name):
    '''
    Return two lists:
    1) list of timestamp when it's not contained directly in the attachments columns (ie. not all type are 
    constructed the same --> lead to some nightmares)
    2) list of nested dictionaries 
    '''
    list_date = []
    list_attachments = []

    for i in df.iterrows():
        main_list = i[1][3]
        condition = gen(main_list, name)
        
        if condition :
            list_date.append(i[1][0])
            list_attachments.append(i[1][3])
            
    return list_date, list_attachments
