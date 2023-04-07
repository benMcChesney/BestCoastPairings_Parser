import configparser
import pyodbc
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd 
import os 

config = configparser.ConfigParser()
config.read('config.ini')

c = config['output_db']
conn_string = f"mssql+pyodbc://{c['user']}:{c['pwd']}@{c['server']}/{c['database']}?driver={c['driver']}&trusted_connection=Yes"
engine = sqlalchemy.create_engine( conn_string , echo=False) 
engine.connect() ; 
cwd = os.getcwd()

filesToTables = [ 
    #'listParse_factions'
    #, 'listParse_units' 
    #,  'event_army_lists_events' 
    #, 'pairingsData'
    # 'placingsData'
    # 'events_links'
    'event_meta'
    ]

for f in filesToTables : 
    df = pd.read_csv( 
        f"{f}.csv"
        , low_memory=False
    )
    print( f )
    print( 'original shape  ' , df.shape )
    df.dropna( axis=1 , thresh = int(0.01*df.shape[0]), inplace=True)
    print( 'after dropping ' , df.shape  )
    df.to_sql( f , conn_string , if_exists='replace')
    print ( 'written to SQL ')
