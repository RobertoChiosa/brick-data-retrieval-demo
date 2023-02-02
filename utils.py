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
