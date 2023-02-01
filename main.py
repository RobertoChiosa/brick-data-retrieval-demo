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
import matplotlib.pyplot as plt
from utils import *

if __name__ == '__main__':
    # Compile ttl if needed
    # compile_ttl("ttl/bldg2.ttl")

    g = brickschema.Graph().load_file("ttl/compiled-bldg2.ttl")

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
    md = sparql_to_df(g, q)
    md.head()

    ahu, sat, sp, sat_uuid, sp_uuid = md.values[1]
    df = get_data([sat_uuid, sp_uuid], ['sat', 'sp'])
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
