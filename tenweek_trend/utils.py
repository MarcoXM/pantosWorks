import pandas as pd
import numpy as np
import os
from datetime import datetime

def get_selected_cols_df(df, cols):
    '''
    cols : list of str 
    '''
    return df[cols]


def get_selected_values_df(df, values_in_cols, col_name):
    '''
    values_in_cols : list of str
    col : str
    '''
    df = df[df[col_name].isin(values_in_cols)]
    return df


def get_selected_values_over_df(df, values_in_cols, col_name):
    '''
    values_in_cols : digit
    col : str
    '''
    df = df[df[col_name] >= values_in_cols]
    return df


def joinStr(words):
    return "".join(words.split())


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_daily_report_df(df_iod,df_tm):
    operation_dict = pd.Series( df_tm['Operational Status'].values,df_tm['Load ID'].values).to_dict()
    df_iod['Stop Seq'] = df_iod.apply(lambda x : operation_dict.get(x['Load ID'],"In Transit"), axis=1)
    return df_iod


def getDate_in_month():
    return int(str(datetime.now())[8:10])


def greeting():
    h = datetime.now().hour
    if 0 < h < 12:
        return "Morning "
    
    elif 12 <= h <= 17:
        return 'Afternoon'
    
    else:
        return 'Evening'
