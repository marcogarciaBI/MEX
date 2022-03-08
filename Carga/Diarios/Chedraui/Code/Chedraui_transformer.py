#!/usr/bin/env python
# coding: utf-8

#%%
from fileinput import filename
import jupyternotify
import requests
import pandas as pd
import calendar
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from datetime import datetime
from datetime import timedelta
from time import sleep
import json
import os
import pyodbc

# %%
path = r'\\NASPRO.infovisiontv.com\Respaldo_Operacion_Cargas\Chedraui\2022'
files = [f for f in os.listdir(path) if f.endswith('.txt')]
#%%
%%time
'''
for week in range(24, 31):
    path = r'\\NASPRO.infovisiontv.com\Respaldo_Operacion_Cargas\Chedraui\2022'
    filename_import = 'Chedraui_{0}012022.txt'
    filename_import = filename_import.format(week)
    '''
for filename_import in files:
    df = pd.read_csv(path + '\\' + filename_import,sep='|',encoding='ANSI')
    df.drop(['OmnicanalUni','OmnicanalVta'],axis=1,inplace=True)

    to_remove = ['03-21','11-16','10-14','10-17','11-18','07-18','11-17','09-18','04-18','10-18','12-18','11-12','09-20','10-20','08-19','02-20','11-20','12-20','04-21','10-21']
    for numeros in to_remove:
        df['tienda_nombre'] = df['tienda_nombre'].apply(lambda x: x.replace(numeros,''))

    fix_tienda_nombre = {'PERCITO VERACRUZ GRACIANO SANCHEZ BOCA DEL RIO': 'PERCITO VERACRUZ GRACIANO SANCHEZ',
                         'PERCITO VERACRUZ GRACIANO SANCHEZ BOCA DEL RIO ':'PERCITO VERACRUZ GRACIANO SANCHEZ',
                         'PERCITO VERACRUZ GRACIANO SANCHEZ BOCA DEL RIO 06-20':'PERCITO VERACRUZ GRACIANO SANCHEZ',
                        'PER CHEDRAUI TUXTLA GUTIÉRREZ CENTRAL CAMIONERA':'PER CHEDRAUI TUXTLA GUTIÉRREZ CENTRAL',
                        'PER CHEDRAUI TUXTLA GUTIÉRREZ CENTRAL CAMIONERA ':'PER CHEDRAUI TUXTLA GUTIÉRREZ CENTRAL',
                        'PER CHEDRAUI TUXTLA GUTIÉRREZ CENTRAL CAMIONERA  ':'PER CHEDRAUI TUXTLA GUTIÉRREZ CENTRAL'}

    df['tienda_nombre'] = df['tienda_nombre'].replace(fix_tienda_nombre)

    filename_export = 'Chedraui_' + ''.join(list(str(df['dia'].unique()[0]))[6:]) + ''.join(list(str(df['dia'].unique()[0]))[4:6]) + ''.join(list(str(df['dia'].unique()[0]))[0:4]) + '.txt'
    df.to_csv(path + '\\' + filename_export, sep='|',encoding='ANSI',index=False)
# %%
