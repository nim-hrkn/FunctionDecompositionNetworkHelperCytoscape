from graphviz import Digraph
import json
import numpy as np
from copy import deepcopy
from collections import OrderedDict


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


class cxReader:
    def __init__(self, filename):
        with open(filename) as f:
            network = json.load(f)
        self.network = network
        self.analyze_nodes()
        self.analyze_id()

        self.have_fd_network = False
        self.fd_nodes = []
        self.fd_edges = []

    def analyze_id(self):
        id_max = 0
        for node in self.io_nodes:
            id_max = max(id_max, node["@id"])
        for node in self.device_nodes:
            id_max = max(id_max, node["@id"])
        for node in self.edges:
            id_max = max(id_max, node["@id"])
        self.id_max = id_max

    def next_id(self):
        self.id_max += 1
        return self.id_max

    def analyze_nodes(self):
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

    def make_apply_node(self, device_node):
        label = " ".join(["Apply", device_node["n"]])
        newid = self.next_id()
        node = {"@id": newid, "n": label, "shape": "hexagon"}
        return node

    def make_isa_network(self):

        for node in self.io_nodes:
            label = " ".join(["Obtain", node["n"]])
            node = {"@id": node["@id"], "n": label, "shape": "oval"}
            self.fd_nodes.append(node)

        for edge in self.edges:
            s = edge["s"]
            t = edge["t"]

            target_node = _find_name(self.io_nodes, t)
            newid = self.next_id()
            label = " ".join([target_node["n"], "way"])
            way_node = {"@id": newid, "n": label,
                        "shape": "rectangle", "fillcolor": "gray"}
            self.fd_nodes.append(way_node)

            newid = self.next_id()
            self.fd_edges.append({"@id": newid, "s": s, "t": way_node["@id"]})

            newid = self.next_id()
            self.fd_edges.append({"@id": newid, "s": way_node["@id"], "t": t})

        self.have_fd_network = True

    def find_node_connection(self, id_, s_or_t):
        rev_s_or_t = {"s": "t", "t": "s"}
        for edge in self.edges:
            if edge[s_or_t] == id_:
                return edge[rev_s_or_t[s_or_t]]
        return None

    def make_fd_network(self):

        for edge in self.edges:
            s = edge["s"]
            t = edge["t"]
            id_ = edge["@id"]
            # change the order between t and s
            self.fd_edges.append({"@id": id_, "s": t, "t": s})

        for node in self.io_nodes:
            label = " ".join(["Obtain", node["n"]])
            node = {"@id": node["@id"], "n": label, "shape": "oval"}
            self.fd_nodes.append(node)

        for node in self.device_nodes:
            label = " ".join([node["n"], "way"])
            way_node = {"@id": node["@id"], "n": label, "shape": "rectangle"}

            self.fd_nodes.append(way_node)

            source_id = self.find_node_connection(way_node["@id"], "t")
            if source_id is not None:
                apply_node = self.make_apply_node(node)
                self.fd_nodes.append(apply_node)
                id_ = self.next_id()
                node = {"@id": id_, "s": node["@id"], "t": apply_node["@id"]}
                self.fd_edges.append(node)

        self.have_fd_network = True

    def make_network(self, type_="workflow"):
        if not self.have_fd_network:
            if type_ == "workflow":
                self.make_fd_network()
            elif type_ == "is-a":
                self.make_isa_network()

    def graphviz_workflow(self, filename=None, rankdir="BT"):
        g = Digraph(format="png")
        g.attr('graph', rankdir=rankdir)
        for node in self.io_nodes:
            label = deepcopy(node["n"])
            g.node(str(node["@id"]), label=label, shape="oval")

        for node in self.device_nodes:
            label = deepcopy(node["n"])
            g.node(str(node["@id"]), label=label, shape="rectangle")

        for edge in self.edges:
            s = edge["s"]
            t = edge["t"]
            g.edge(str(s), str(t))
        if filename is not None:
            g.render(filename)
        g.view()


def _fix_nodes_edges_id(cxnetwork):
    # fix edges
    for edge in cxnetwork.fd_edges:
        source_node = _find_name(cxnetwork.fd_nodes, edge["s"])
        target_node = _find_name(cxnetwork.fd_nodes, edge["t"])
        edge["s"] = source_node["n"].replace(" ", "_")
        edge["t"] = target_node["n"].replace(" ", "_")
    for node in cxnetwork.fd_nodes:
        node["@id"] = node["n"].replace(" ", "_")

    return cxnetwork


def _calc_elementCount(data, key):
    n = 0
    for datum in data:
        for datum_key, datum_value in datum.items():
            if datum_key == key:
                n = len(datum_value)
                return n
    return n


def _calc_idCounter(data, key):
    id_list = []
    for datum in data:
        for datum_key, datum_value in datum.items():
            if datum_key == key:
                for value in datum_value:
                    id_list.append(value["@id"])
    id_array = np.array(id_list)
    return int(id_array.max())


class FDNPlotter:
    def __init__(self, cxnetwork_list, fix_node_id=True):
        if fix_node_id:
            cxnetwork_fix_list = []
            for cxnetwork in cxnetwork_list:
                cxnetwork_fix = _fix_nodes_edges_id(cxnetwork)
                cxnetwork_fix_list.append(cxnetwork_fix)
        else:
            cxnetwork_fix_list = cxnetwork_list

        self.fd_nodes = []
        self.fd_edges = []
        for cxnetwork in cxnetwork_fix_list:
            self.fd_nodes.extend(cxnetwork.fd_nodes)
            self.fd_edges.extend(cxnetwork.fd_edges)

        if fix_node_id:
            self.reindex_fd_nodes_edges()

    def print(self):
        for node in self.fd_nodes:
            print("FD_NODE", node)
        for edge in self.fd_edges:
            print("FD_EDGE", edge)

    def reindex_fd_nodes_edges(self):
        fd_nodes = self.fd_nodes
        fd_edges = self.fd_edges
        id_ = 1
        id_dic = {}
        # node["@oid"] is str
        for node in fd_nodes:
            id_dic[node["@id"]] = id_
            id_ += 1
        # node["@id"] is int
        for edge in fd_edges:
            edge["@id"] = id_+1
            id_ += 1

        for node in fd_nodes:
            id_ = id_dic[node["@id"]]
            node["@id"] = id_
        for edge in fd_edges:
            for st in ["s", "t"]:
                id_ = id_dic[edge[st]]
                edge[st] = id_

    def graphviz_fd_network(self, filename=None, type_="workflow"):

        g = Digraph(format="png")
        for node in self.fd_nodes:
            if "fillcolor" in node:
                g.node(str(node["@id"]), label=node["n"],
                       shape=node["shape"], style="filled", fillcolor=node["fillcolor"])
            else:
                g.node(str(node["@id"]), label=node["n"], shape=node["shape"])

        for edge in self.fd_edges:
            s = edge["s"]
            t = edge["t"]
            g.edge(str(s), str(t))

        if filename is not None:
            g.render(filename)
        g.view()

    def fix_metaData(self, metaData, data):
        data_fix = []
        for line in metaData:
            key = "elementCount"
            if key in line.keys():
                n = _calc_elementCount(data, line["name"])
                if n > 0:
                    line[key] = n
                else:
                    del line[key]
            key = "idCounter"
            if key in line.keys():
                n = _calc_idCounter(data, line["name"])
                line[key] = n
            data_fix.append(line)
        return data_fix

    def fix_edgeAttributes(self):
        element_list = []
        for edge in self.fd_edges:
            source_node = _find_name(self.fd_nodes, edge["s"])
            target_node = _find_name(self.fd_nodes, edge["t"])

            label = "{} (interacts with) {}".format(
                source_node["n"], target_node["n"])
            element = {"po": edge["@id"], "n": "name", "v": label}
            element_list.append(element)
        return element_list

    def fix_cyVisualProperties(self, lines):
        print("len(line)", len(lines))
        for node in self.fd_nodes:
            if "shape" in node:
                shape_value = node["shape"].upper()
                if shape_value == "OVAL":
                    shape_value = "ELLIPSE"
                element = {'properties_of': 'nodes',
                           'applies_to': node["@id"],
                           'properties': {'NODE_SHAPE': shape_value}}

                lines.append(element)
        return lines

    def cx_fd_network(self, network_name, filename):
        change = True

        _filename = "simple1.cx"
        with open(_filename) as f:
            network = json.load(f)
            print("load from", _filename)
        data = []
        for line in network:
            for key, line in line.items():
                if key == "numberVerification":
                    datum = {key: line}
                    data.append(datum)
                elif key == "metaData":
                    if change:
                        value = self.fix_metaData(line, data)
                        datum = {key: value}

                        data.append(datum)
                    else:
                        datum = {key: line}
                        data.append(datum)
                elif key == "cyTableColumn":
                    datum = {key: line}
                    data.append(datum)
                elif key == "networkAttributes":
                    if change:
                        line = [{'n': 'name', 'v': network_name}]
                        datum = {key: line}
                        data.append(datum)
                    else:
                        datum = {key: line}
                        data.append(datum)
                elif key == "nodes":
                    if change:
                        elements = []
                        for node in self.fd_nodes:
                            elements.append(
                                {"@id": node["@id"], "n": node["n"]})
                        data.append({key: elements})
                    else:
                        datum = {key: line}
                        data.append(datum)
                elif key == "edges":
                    if change:
                        elements = []
                        for edge in self.fd_edges:
                            elements.append(
                                {"@id": edge["@id"], "s": edge["s"], "t": edge["t"]})
                        data.append({key: elements})
                    else:
                        datum = {key: line}
                        data.append(datum)
                elif key == "edgeAttributes":
                    if change:
                        line = self.fix_edgeAttributes()
                        datum = {key: line}
                        data.append(datum)
                    else:
                        datum = {key: line}
                        data.append(datum)
                elif key == "cartesianLayout":
                    pass
                elif key == "cyVisualProperties":
                    if change:
                        line = self.fix_cyVisualProperties(line)
                        datum = {key: line}
                        data.append(datum)
                    else:
                        datum = {key: line}
                        data.append(datum)
                elif key == "status":
                    datum = {key: line}
                    data.append(datum)
                else:
                    print("key error", key)
                    raise ValueError
        if filename is not None:
            with open(filename, "w") as f:
                json.dump(data, f)
            print("save to", filename)


if __name__ == "__main__":
    import argparse
    if True:
        parser = argparse.ArgumentParser()
        parser.add_argument("--show_workflow",
                            help="show workflows", action="store_true")
        parser.add_argument(
            "--show_is_a", help="show is-a relation", action="store_true")
        parser.add_argument("--output_filename", help="output name",
                            default="output.cx")
        parser.add_argument("--name", help="Network name",
                            default="fd_network")
        parser.add_argument("file", nargs="+")
        args = parser.parse_args()

        filename_list = args.file

    cxreader_list = []
    for filename in filename_list:
        if "is-a" in filename:
            type_ = "is-a"
        else:
            type_ = "workflow"
        cxreader = cxReader(filename)
        cxreader.make_network(type_)
        if type_ == "workflow" and args.show_workflow:
            cxreader.graphviz_workflow(filename+".png")
        if type_ == "is-a" and args.show_is_a:
            cxreader.graphviz_workflow(filename+".png", rankdir="TB")

        cxreader_list.append(cxreader)

    plotter = FDNPlotter(cxreader_list)

    # plotter.graphviz_fd_network("df_network")
    plotter.cx_fd_network(args.name, args.output_filename)
