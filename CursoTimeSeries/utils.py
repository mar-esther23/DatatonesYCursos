from re import sub
from unidecode import unidecode
import pandas as pd

def clean_string(s):
    if type(s)==str:
        s = unidecode(s)
        s = sub('[^A-Za-z0-9 ]+', '', s)
        s = sub('\s+', ' ', s)
        s = s.strip().title()
    else: s=''
    return s

def pivot_datetime(df, filas, columnas, values, 
                   formato='dia', aggfunc='sum', 
                   normalizar=False, ignore=None,
                   mostrar_total=False, mostrar_columnas=15):
    if formato=='dia':          f = '%Y-%m-%d'
    if formato=='semana':       f = '%Y-%U'
    if formato=='mes':          f = '%Y-%m'
    if formato=='año':          f = '%Y'
    if formato=='dia_del_mes':  f = '%d'
    if formato=='dia_semana':   f = '%w'
    if formato=='hora':         f = '%H'
    if formato=='dia_sem_hora': f = '%w-%H'
        
    df_time = pd.pivot_table(df, aggfunc=aggfunc, index=filas, 
                                 columns=df[columnas].dt.strftime(f),
                                 values=values, fill_value=0)
    if ignore!=None:
        df_time.drop(ignore, errors='ignore', inplace=True)
    
    df_time = df_time.reindex(df_time.sum(axis=1).sort_values(ascending=False).index)
    df_time = df_time.reindex(df_time.sum(axis=1).sort_values(ascending=False).index)
    df_time = df_time.iloc[0:mostrar_columnas,:]
    
    if mostrar_total:
        i_row = [(i,s) for i,s in zip(df_time.index,df_time.sum(axis=1))]
        i_row = [str(i)+'   ('+str(int(s))+')' for i,s in i_row]
        df_time.index=i_row
    
    if normalizar: 
        df_time = df_time.div(df_time.sum(axis=1), axis=0)
        
    return df_time