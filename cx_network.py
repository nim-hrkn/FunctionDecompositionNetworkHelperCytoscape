from graphviz import Digraph
import json
import numpy as np
from copy import deepcopy


def _find_name(nodes, id_):
    for node in nodes:
        if node["@id"] == id_:
            return node
    raise ValueError("no id {}".format(id_))
    return None


def _process_cyVisualProperties(nodes, lines):
    key_find_list = [["properties_of", "nodes"], ["applies_to", None]]
    device_nodes = []
    for line in lines:
        flag = np.full(len(key_find_list), False)
        for key, value in line.items():
            for ikey, (key_find, value_find) in enumerate(key_find_list):
                if key == key_find:
                    if value_find is None:
                        flag[ikey] = True
                    elif value_find is not None:
                        if value == value_find:
                            flag[ikey] = True
        if np.all(flag):
            id_ = line["applies_to"]
            shape = line["properties"]["NODE_SHAPE"]
            if shape == "RECTANGLE":
                device = _find_name(nodes, id_)
                device_nodes.append(device)
    return device_nodes


class cxNetwork:
    def __init__(self, filename):
        with open(filename) as f:
            network = json.load(f)
        self.network = network
        self.analyze()

    def analyze(self):
        network = self.network
        for attrib_list in network:
            for key, values in attrib_list.items():
                if True:
                    if key == "nodes":
                        self.nodes = values
                    if key == "edges":
                        self.edges = values
                if key == "cyVisualProperties":
                    self.device_nodes = _process_cyVisualProperties(
                        self.nodes, values)
        self.io_nodes = deepcopy(self.nodes)
        for node in self.device_nodes:
            self.io_nodes.remove(node)

    def graphvis(self, filename=None):
        g = Digraph(format="png")
        for node in cxreader.io_nodes:
            label = deepcopy(node["n"])
            # label = label.replace(" ", "_")
            g.node(str(node["@id"]), label=label, shape="oval")

        for node in cxreader.device_nodes:
            label = deepcopy(node["n"])
            # label = label.replace(" ", "_")
            g.node(str(node["@id"]), label=label, shape="rectangle")

        for edge in cxreader.edges:
            s = edge["s"]
            t = edge["t"]
            g.edge(str(s), str(t))
        if filename is not None:
            g.render(filename)
        g.view()


if __name__ == "__main__":
    filename = "Network_1.cx"

    cxreader = cxNetwork(filename)
    print(cxreader.edges)

    cxreader.graphvis()
