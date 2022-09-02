import brickschema
import time
import sys

# gets the filename as command line argument
filename = sys.argv[1]

# loads the last version of brick schema
bldg = brickschema.Graph()
# adds the filename in the graph
bldg.load_file(filename)

# "compile" the graph
print("Compiling graph")
t1 = time.time()
bldg.expand("brick")
print(f"Finished compiling (Took {time.time() - t1} seconds)")

bldg.serialize(f"compiled-{filename}", format="turtle")