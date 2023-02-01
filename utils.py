# Author:       Roberto Chiosa
# Copyright:    Roberto Chiosa, © 2023
# Email:        roberto.chiosa@polito.it
#
# Created:      01/02/23
# Script Name:  utils.py
# Path:         
#
# Script Description:
#
#
# Notes:

import time

import brickschema
import pandas as pd
import psycopg2
from config import Config, logger


def compile_ttl(filepath):
    """

    :param filepath:
    :return:
    """
    # loads the last version of brick schema
    bldg = brickschema.Graph()
    # adds the filename in the graph
    bldg.load_file(filepath)

    # "compile" the graph
    logger.info("Compiling graph")
    t1 = time.time()
    bldg.expand("brick")
    logger.info(f"Finished compiling (Took {time.time() - t1} seconds)")

    bldg.serialize(f"{filepath}-compiled.ttl", format="turtle")


def sparql_to_df(g, q):
    """

    :param g:
    :param q:
    :return:
    """
    res = g.query(q)  # performs the query on the model
    df = pd.DataFrame.from_records(list(res))  # transforms the results into dataframe
    df = df.applymap(str)  # transforms all to string
    df.drop_duplicates(inplace=True)  # drops duplicates
    return df


def get_data(uuids, names):
    """
    
    :param uuids:
    :param names:
    :return:
    """
    # creates connection
    dbRemote = psycopg2.connect(
        user=Config.TIMESCALEDB_USER,
        password=Config.TIMESCALEDB_PSW,
        host=Config.TIMESCALEDB_HOST,
        port=Config.TIMESCALEDB_PORT)

    # perform query on the timescale db
    query = "SELECT time, value, uuid FROM data WHERE uuid = ANY(%s)"
    df = pd.read_sql(query, dbRemote, params=(uuids,))  # reads from db remote
    df = df.pivot(columns='uuid', values='value', index='time')  # explicit column structure
    df = df.resample('15T').mean()  # syncronize the timestamp to 15 minutes
    df.columns = names

    return df
