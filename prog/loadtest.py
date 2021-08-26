import json
from copy import deepcopy
import sys

# filename = "heat_exchanger.cx"
# filename = "simple1.cx"
# filename = "output.cx"

filename = sys.argv[1]

with open(filename) as f:
    network = json.load(f)

def show_dic(dic):
    if isinstance(dic,dict):
        for key,value in dic.items():
            print("{}> {}".format(key,value))

prop = []

cx = []
dlen = []
for line in network:
    print("===========================")
    for line_key, line_value in line.items():
        print("KEY", line_key)
        print("NODE", line_value)

        if line_key == "cyVisualProperties":
            cyVisualProp = deepcopy(line_value)
            print("----------")
            # print(len(line_value))
            for aline in line_value:
                print(">>>", aline)
                flag = False
                for key, value in aline.items():
                    print("<{}>".format(key) )
                    show_dic(value)
            d = {"cyVisualProperties": line_value}
            # cx.append(d)
        elif line_key == "cartesianLayout":
            print(len(line_value))
            d = None
        elif line_key == "nodeAttributes":
            print(len(line_value))
            d = None
            cx.append(d)
        elif line_key == "edgeAttributes":
            print(len(line_value))
            d = None
            cx.append(d)
        else:
            print(len(line_value))
            d = {line_key: line_value}
            cx.append(d)
        if d is not None:

            if len(d[line_key]) > 1:
                dlen.append({"name": line_key, "elementCount": len(
                    d[line_key]), "version": 1.0})
            else:
                dlen.append({"name": line_key, "version": 1.0})


print("DLEN", {"metaData": dlen})
filename = "m.cx"
with open(filename, "w") as f:
    json.dump(cx, f)
print("save to",filename)

if False:
    filename = "cyVisualProperties.json"
    datum = {"cyVisualProperties": cyVisualProp}
    with open(filename,"w") as f:
        json.dump(datum, f)
    print("save to", filename)
