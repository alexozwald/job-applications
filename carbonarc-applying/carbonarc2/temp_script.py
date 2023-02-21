import json
import pandas as pd

"""PRETTY PRINT OLD GEOJSON
PLUTO_GEOJSON = "./maps/pluto_sm.geojson"
PLUTO_GEOJSON_PP = "./maps/pluto_sm_pp.geojson"

with open(PLUTO_GEOJSON, 'r') as f:
	data = json.load(f)
	
with open(PLUTO_GEOJSON_PP, 'w') as f:
	json.dump(data, f, indent='\t')
	print(f"prettier json dump success!")
"""

PLUTO_GEOJSON22_big = "./maps/MapPLUTO22v2_big.json"
PLUTO_GEOJSON22 = "./maps/MapPLUTO22v2_bbl.geojson"
 
"""PANDAS JSON SAVEME ATTEMPT
#data = pd.read_json(PLUTO_GEOJSON22_big)

#data.to_json(PLUTO_GEOJSON22, lines=True)

#print(data.columns, '\n\n')
#print(data.head(), '\n\n')
#print(data.info(), '\n\n')

#data.
	
#with open(PLUTO_GEOJSON22, 'w') as f:
#	json.dump(data, f, indent=2)
#	print(f"thicc geojson removal success!")
"""

"""JSON SAVEME LEARNING
test = open("./studyherjson.geojson", 'w+')
with open(PLUTO_GEOJSON22_big, 'r') as f:
	i = 0
	for line in f:
		test.write(line)
		if i == 5000:
			test.write("...")
			break
		i += 1
test.close()
"""

"""JSON REWRITING THE WORLD
tstPLUTO_GEOJSON22_og = "./studyherjson.geojson"
tstPLUTO_GEOJSON22_bbl = "./studyherBBL.geojson"

og = open(tstPLUTO_GEOJSON22_og, 'rt')
nw = open(tstPLUTO_GEOJSON22_bbl, 'wt')

s0 = 'properties":{'
s1 = '"BBL":'
s2 = '}},\n'

nw.write('{"type":"FeatureCollection", "features": [\n')
ogiter = iter(og)
next(ogiter)
i = 0
for line in ogiter:

	#print(line)
	print(i)
	line0, lineX = line.split(s0)   # start + shape
	_, line2 = lineX.split(s1)  # unused (props) + bbl# + unused
	lineA = line0 + s0 + s1 + line2[:10] + s2
	nw.write(lineA)
	i += 1
	
	#try:
	#	line0, lineX = line.split(s0)   # start + shape
	#	_, lineX = lineX.split(s1)  # unused (props)
	#	line2, lineX = lineX.split(s2)  # BBL # + unused (props)

	#	lineA = line0 + s0 + s1 + line2[:10] + s2 
	#	nw.write(lineA)
	#finally:
	#	continue
	

nw.write("}}")  # last line

og.close()
nw.close()

print("test complete!")
"""

"""TEST VALUE OF LAST LINE
PLUTO_GEOJSON22_big = "./maps/MapPLUTO22v2_big.json"
with open(PLUTO_GEOJSON22_big, 'r') as f:
    for line in f:
        pass
    last_line = line
print(last_line)

with open(PLUTO_GEOJSON22_big, 'r') as f:
    for line in f:
        pass
        line1 = line
    lst2_line = line1
    last_line = line
print(f"lst2_line = {lst2_line}")
print(f"last_line = {last_line}")
"""

# FINAL CODE TO REDO IT
og = open(PLUTO_GEOJSON22_big, 'rt')
nw = open(PLUTO_GEOJSON22, 'wt')

s0 = 'properties":{'
s1 = '"BBL":'
s2 = '}},\n'

nw.write('{"type":"FeatureCollection", "features": [\n')
ogiter = iter(og)
next(ogiter)
i = 0
for line in ogiter:
	try:
		line0, lineX = line.split(s0)   # start + shape
		_, line2 = lineX.split(s1)  # unused (props) + bbl# + unused
		lineA = line0 + s0 + s1 + line2[:10] + s2
		nw.write(lineA)
		i += 1
	except ValueError:
		nw.write("]}")

og.close()
nw.close()

print("test complete!")