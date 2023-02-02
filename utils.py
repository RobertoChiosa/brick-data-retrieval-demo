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

from config import logger


def compile_ttl(input_filepath, output_filepath):
    """ Used to compile the ttl file with reasoner
    :param output_filepath: path to ttl file
    :param input_filepath: path to compiled ttl file
    """
    # loads the last version of brick schema
    bldg = brickschema.Graph()
    # adds the filename in the graph
    bldg.load_file(input_filepath)

    # "compile" the graph
    logger.info("Compiling graph")
    t1 = time.time()
    try:
        bldg.expand("brick")
        bldg.serialize(output_filepath, format="turtle")
        logger.info(f"Finished compiling (Took {time.time() - t1} seconds)")
    except Exception as e:
        logger.error(f"Error expanding {e}")

# def sparql_to_df(g, q):
#     """ Converts sparql query to pandas dataframe
#
#     :param g: brock graph
#     :param str q: sparql query
#     :return df : pandas dataframe of query
#     """
#     res = g.query(q)  # performs the query on the model
#     df = pd.DataFrame.from_records(list(res))  # transforms the results into dataframe
#     df = df.applymap(str)  # transforms all to string
#     df.drop_duplicates(inplace=True)  # drops duplicates
#     return df


# def get_data(uuids, names):
#     """ Retrieves data from timescaledb
#
#     :param str uuids: unique identifiers of timeseries
#     :param names:
#     :return:
#     """
#     # creates connection
#     dbRemote = psycopg2.connect(
#         user=Config.TIMESCALEDB_USER,
#         password=Config.TIMESCALEDB_PSW,
#         host=Config.TIMESCALEDB_HOST,
#         port=Config.TIMESCALEDB_PORT)
#
#     # perform query on the timescale db
#     query = "SELECT time, value, uuid FROM data WHERE uuid = ANY(%s)"
#     df = pd.read_sql(query, dbRemote, params=(uuids,))  # reads from db remote
#     df = df.pivot(columns='uuid', values='value', index='time')  # explicit column structure
#     df = df.resample('15T').mean()  # synchronize the timestamp to 15 minutes
#     df.columns = names
#
#     return df
