# Author:       Roberto Chiosa
# Copyright:    Roberto Chiosa, © 2023
# Email:        roberto.chiosa@polito.it
#
# Created:      01/02/23
# Script Name:  main.py
# Path:         
#
# Script Description:
#
#
# Notes:

import os

import matplotlib.pyplot as plt
import pandas as pd
import psycopg2

from config import Config
from utils import *

if __name__ == '__main__':

    ttl_compiled_file = "ttl/compiled-bldg2.ttl"

    # Compile ttl if needed
    if not os.path.exists(ttl_compiled_file):
        compile_ttl(input_filepath="ttl/bldg2.ttl", output_filepath=ttl_compiled_file)

    g = brickschema.Graph().load_file(ttl_compiled_file)

    q = """
    SELECT DISTINCT ?ahu ?sat ?sp ?sat_uuid ?sp_uuid WHERE {
       ?ahu  a  brick:AHU .
       ?ahu  brick:hasPoint  ?sat, ?sp .
       ?sat  a  brick:Supply_Air_Temperature_Sensor ;
             brick:timeseries [ brick:hasTimeseriesId ?sat_uuid ] .
       ?sp   a  brick:Supply_Air_Temperature_Setpoint ;
             brick:timeseries [ brick:hasTimeseriesId ?sp_uuid ]
    }
    """
    # transform query into dataframe
    # md = sparql_to_df(g, q)
    res = g.query(q)  # performs the query on the model
    df = pd.DataFrame.from_records(list(res))  # transforms the results into dataframe
    df = df.applymap(str)  # transforms all to string
    df.drop_duplicates(inplace=True)  # drops duplicates
    df.columns = ['ahu', "sat", "sp", "sat_uuid", "sp_uuid"]
    df.head()

    ahu, sat, sp, sat_uuid, sp_uuid = df.values[1]
    # df = get_data([sat_uuid, sp_uuid], ['sat', 'sp'])

    # creates connection
    dbRemote = psycopg2.connect(
        user=Config.TIMESCALEDB_USER,
        password=Config.TIMESCALEDB_PSW,
        host=Config.TIMESCALEDB_HOST,
        port=Config.TIMESCALEDB_PORT)
    uuids = [sat_uuid, sp_uuid]
    names = ['sat', 'sp']
    # perform query on the timescale db
    query = "SELECT time, value, uuid FROM data WHERE uuid = ANY(%s)"
    df = pd.read_sql(query, dbRemote, params=(uuids,))  # reads from db remote
    df = df.pivot(columns='uuid', values='value', index='time')  # explicit column structure
    df = df.resample('15T').mean()  # synchronize the timestamp to 15 minutes
    df.columns = names

    print(df.head())

    # fig = plt.figure()  # an empty figure with no Axes
    fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')  # a figure with a single Axes
    ax.plot(df['2012-06-01':'2012-06-5']['sp'], linestyle='-', label='Supply Air Temperature')
    ax.plot(df['2012-06-01':'2012-06-5']['sat'], linestyle=':', label='Set Point Air Temperature')
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature [°F]')
    ax.set_title("AHU Air temperature")  # Add a title to the axes.
    ax.legend()  # Add a legend.
    fig.show()
