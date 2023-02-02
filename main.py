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

    # path to ttl file
    ttl_compiled_file = "ttl/compiled-bldg2.ttl"

    # Compile ttl if needed
    if not os.path.exists(ttl_compiled_file):
        compile_ttl(input_filepath="ttl/bldg2.ttl", output_filepath=ttl_compiled_file)

    # load ttl in brick graph
    g = brickschema.Graph().load_file(ttl_compiled_file)

    # query supply air temperature and setpoint and relative uuid
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

    # performs the query on the model
    res = g.query(q)
    # transform query into dataframe
    df_brick = pd.DataFrame.from_records(
        data=list(res), columns=['ahu', "sat", "sp", "sat_uuid", "sp_uuid"])
    # transforms all to string
    df_brick = df_brick.applymap(str)
    # drops duplicates
    df_brick.drop_duplicates(inplace=True)
    # let say that i want to analyze the first
    ahu, sat, sp, sat_uuid, sp_uuid = df_brick.values[1]

    # connect to local TimescaleDB
    try:
        dbRemote = psycopg2.connect(
            user=Config.TIMESCALEDB_USER,
            password=Config.TIMESCALEDB_PSW,
            host=Config.TIMESCALEDB_HOST,
            port=Config.TIMESCALEDB_PORT)

        # opens connection and perform query
        with dbRemote.cursor() as cursorRemote:
            cursorRemote.execute("""SELECT time, value, uuid 
                                    FROM data 
                                    WHERE uuid in {}
                                    """.format(tuple([sat_uuid, sp_uuid])))
            result_list = cursorRemote.fetchall()

        # convert query result to dataframe
        df1 = pd.DataFrame(result_list, columns=['time', 'value', 'uuid'])
        # explicit column structure
        df1 = df1.pivot(columns='uuid', values='value', index='time')
        # synchronize the timestamp to 15 minutes
        df1 = df1.resample('15T').mean()
        # rename
        df1.columns = ["sat", "sp"]

        # fig = plt.figure()  # an empty figure with no Axes
        fig, ax = plt.subplots(figsize=(8, 3), layout='constrained')  # a figure with a single Axes
        ax.plot(df1['2012-06-04':'2012-06-08']['sp'], linestyle='-', label='Supply Air Temperature')
        ax.plot(df1['2012-06-04':'2012-06-08']['sat'], linestyle=':', label='Set Point Air Temperature')
        ax.set_ylabel('Temperature [°F]')
        ax.set_title("AHU02 Air temperature")  # Add a title to the axes.
        ax.legend()  # Add a legend.
        # fig.show()
        plt.savefig("img/download.png")

    except Exception as e:
        logger.error(f"Error when connecting to database: {e}")
