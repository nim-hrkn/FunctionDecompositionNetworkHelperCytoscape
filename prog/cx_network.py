import os
from graphviz import Digraph
import json
import numpy as np
from copy import deepcopy
from collections import OrderedDict

_CX_DEF1 = """[{"numberVerification":[{"longNumber":281474976710655}]},{"metaData":[{"name":"nodeAttributes","version":"1.0"},{"name":"cyHiddenAttributes","version":"1.0"},{"name":"nodes","version":"1.0"},{"name":"cyNetworkRelations","version":"1.0"},{"name":"cyGroups","version":"1.0"},{"name":"networkAttributes","version":"1.0"},{"name":"cyTableColumn","version":"1.0"},{"name":"cartesianLayout","version":"1.0"},{"name":"edgeAttributes","version":"1.0"},{"name":"edges","version":"1.0"},{"name":"cyVisualProperties","version":"1.0"},{"name":"cySubNetworks","version":"1.0"}]},{"cyTableColumn":[{"applies_to":"node_table","n":"shared name"},{"applies_to":"node_table","n":"name"},{"applies_to":"edge_table","n":"shared name"},{"applies_to":"edge_table","n":"shared interaction"},{"applies_to":"edge_table","n":"name"},{"applies_to":"edge_table","n":"interaction"},{"applies_to":"network_table","n":"shared name"},{"applies_to":"network_table","n":"name"},{"applies_to":"network_table","n":"__Annotations","d":"list_of_string"}]},{"networkAttributes":[{"n":"name","v":"simple1"}]},{"nodes":[{"@id":909,"n":"Node 2"},{"@id":907,"n":"Node 1"}]},{"edges":[{"@id":911,"s":907,"t":909,"i":"interacts with"}]},{"edgeAttributes":[{"po":911,"n":"name","v":"Node 1 (interacts with) Node 2"}]},{"cartesianLayout":[{"node":907,"x":-193.0,"y":-123.0},{"node":909,"x":-209.0,"y":-27.0}]},{"cyVisualProperties":[{"properties_of":"network","properties":{"NETWORK_ANNOTATION_SELECTION":"false","NETWORK_BACKGROUND_PAINT":"#FFFFFF","NETWORK_CENTER_X_LOCATION":"0.0","NETWORK_CENTER_Y_LOCATION":"0.0","NETWORK_CENTER_Z_LOCATION":"0.0","NETWORK_DEPTH":"0.0","NETWORK_EDGE_SELECTION":"true","NETWORK_FORCE_HIGH_DETAIL":"false","NETWORK_HEIGHT":"380.0","NETWORK_NODE_LABEL_SELECTION":"false","NETWORK_NODE_SELECTION":"true","NETWORK_SCALE_FACTOR":"1.0","NETWORK_SIZE":"550.0","NETWORK_WIDTH":"815.0"}},{"properties_of":"nodes:default","properties":{"COMPOUND_NODE_PADDING":"10.0","COMPOUND_NODE_SHAPE":"ROUND_RECTANGLE","NODE_BORDER_PAINT":"#CCCCCC","NODE_BORDER_STROKE":"SOLID","NODE_BORDER_TRANSPARENCY":"255","NODE_BORDER_WIDTH":"0.0","NODE_CUSTOMGRAPHICS_1":"org.cytoscape.ding.customgraphics.NullCustomGraphics,0,[ Remove Graphics ],","NODE_CUSTOMGRAPHICS_2":"org.cytoscape.ding.customgraphics.NullCustomGraphics,0,[ Remove Graphics ],","NODE_CUSTOMGRAPHICS_3":"org.cytoscape.ding.customgraphics.NullCustomGraphics,0,[ Remove Graphics ],","NODE_CUSTOMGRAPHICS_4":"org.cytoscape.ding.customgraphics.NullCustomGraphics,0,[ Remove Graphics ],","NODE_CUSTOMGRAPHICS_5":"org.cytoscape.ding.customgraphics.NullCustomGraphics,0,[ Remove Graphics ],","NODE_CUSTOMGRAPHICS_6":"org.cytoscape.ding.customgraphics.NullCustomGraphics,0,[ Remove Graphics ],","NODE_CUSTOMGRAPHICS_7":"org.cytoscape.ding.customgraphics.NullCustomGraphics,0,[ Remove Graphics ],","NODE_CUSTOMGRAPHICS_8":"org.cytoscape.ding.customgraphics.NullCustomGraphics,0,[ Remove Graphics ],","NODE_CUSTOMGRAPHICS_9":"org.cytoscape.ding.customgraphics.NullCustomGraphics,0,[ Remove Graphics ],","NODE_CUSTOMGRAPHICS_POSITION_1":"C,C,c,0.00,0.00","NODE_CUSTOMGRAPHICS_POSITION_2":"C,C,c,0.00,0.00","NODE_CUSTOMGRAPHICS_POSITION_3":"C,C,c,0.00,0.00","NODE_CUSTOMGRAPHICS_POSITION_4":"C,C,c,0.00,0.00","NODE_CUSTOMGRAPHICS_POSITION_5":"C,C,c,0.00,0.00","NODE_CUSTOMGRAPHICS_POSITION_6":"C,C,c,0.00,0.00","NODE_CUSTOMGRAPHICS_POSITION_7":"C,C,c,0.00,0.00","NODE_CUSTOMGRAPHICS_POSITION_8":"C,C,c,0.00,0.00","NODE_CUSTOMGRAPHICS_POSITION_9":"C,C,c,0.00,0.00","NODE_CUSTOMGRAPHICS_SIZE_1":"50.0","NODE_CUSTOMGRAPHICS_SIZE_2":"50.0","NODE_CUSTOMGRAPHICS_SIZE_3":"50.0","NODE_CUSTOMGRAPHICS_SIZE_4":"50.0","NODE_CUSTOMGRAPHICS_SIZE_5":"50.0","NODE_CUSTOMGRAPHICS_SIZE_6":"50.0","NODE_CUSTOMGRAPHICS_SIZE_7":"50.0","NODE_CUSTOMGRAPHICS_SIZE_8":"50.0","NODE_CUSTOMGRAPHICS_SIZE_9":"50.0","NODE_CUSTOMPAINT_1":"DefaultVisualizableVisualProperty(id=NODE_CUSTOMPAINT_1, name=Node Custom Paint 1)","NODE_CUSTOMPAINT_2":"DefaultVisualizableVisualProperty(id=NODE_CUSTOMPAINT_2, name=Node Custom Paint 2)","NODE_CUSTOMPAINT_3":"DefaultVisualizableVisualProperty(id=NODE_CUSTOMPAINT_3, name=Node Custom Paint 3)","NODE_CUSTOMPAINT_4":"DefaultVisualizableVisualProperty(id=NODE_CUSTOMPAINT_4, name=Node Custom Paint 4)","NODE_CUSTOMPAINT_5":"DefaultVisualizableVisualProperty(id=NODE_CUSTOMPAINT_5, name=Node Custom Paint 5)","NODE_CUSTOMPAINT_6":"DefaultVisualizableVisualProperty(id=NODE_CUSTOMPAINT_6, name=Node Custom Paint 6)","NODE_CUSTOMPAINT_7":"DefaultVisualizableVisualProperty(id=NODE_CUSTOMPAINT_7, name=Node Custom Paint 7)","NODE_CUSTOMPAINT_8":"DefaultVisualizableVisualProperty(id=NODE_CUSTOMPAINT_8, name=Node Custom Paint 8)","NODE_CUSTOMPAINT_9":"DefaultVisualizableVisualProperty(id=NODE_CUSTOMPAINT_9, name=Node Custom Paint 9)","NODE_DEPTH":"0.0","NODE_FILL_COLOR":"#FFFFE0","NODE_HEIGHT":"35.0","NODE_LABEL_COLOR":"#000000","NODE_LABEL_FONT_FACE":"SansSerif.plain,plain,12","NODE_LABEL_FONT_SIZE":"12","NODE_LABEL_POSITION":"C,C,c,0.00,0.00","NODE_LABEL_TRANSPARENCY":"255","NODE_LABEL_WIDTH":"200.0","NODE_NESTED_NETWORK_IMAGE_VISIBLE":"true","NODE_PAINT":"#1E90FF","NODE_SELECTED":"false","NODE_SELECTED_PAINT":"#FFFF00","NODE_SHAPE":"ELLIPSE","NODE_SIZE":"35.0","NODE_TRANSPARENCY":"255","NODE_VISIBLE":"true","NODE_WIDTH":"75.0","NODE_X_LOCATION":"0.0","NODE_Y_LOCATION":"0.0","NODE_Z_LOCATION":"0.0"},"dependencies":{"nodeCustomGraphicsSizeSync":"true","nodeSizeLocked":"false"},"mappings":{"NODE_LABEL":{"type":"PASSTHROUGH","definition":"COL=name,T=string"}}},{"properties_of":"edges:default","properties":{"EDGE_CURVED":"true","EDGE_LABEL_COLOR":"#000000","EDGE_LABEL_FONT_FACE":"Dialog.plain,plain,10","EDGE_LABEL_FONT_SIZE":"10","EDGE_LABEL_TRANSPARENCY":"255","EDGE_LABEL_WIDTH":"200.0","EDGE_LINE_TYPE":"SOLID","EDGE_PAINT":"#323232","EDGE_SELECTED":"false","EDGE_SELECTED_PAINT":"#FF0000","EDGE_SOURCE_ARROW_SELECTED_PAINT":"#FFFF00","EDGE_SOURCE_ARROW_SHAPE":"NONE","EDGE_SOURCE_ARROW_SIZE":"6.0","EDGE_SOURCE_ARROW_UNSELECTED_PAINT":"#000000","EDGE_STROKE_SELECTED_PAINT":"#FF0000","EDGE_STROKE_UNSELECTED_PAINT":"#848484","EDGE_TARGET_ARROW_SELECTED_PAINT":"#FFFF00","EDGE_TARGET_ARROW_SHAPE":"ARROW","EDGE_TARGET_ARROW_SIZE":"6.0","EDGE_TARGET_ARROW_UNSELECTED_PAINT":"#000000","EDGE_TRANSPARENCY":"255","EDGE_UNSELECTED_PAINT":"#404040","EDGE_VISIBLE":"true","EDGE_WIDTH":"2.0"},"dependencies":{"arrowColorMatchesEdge":"false"}}]},{"metaData":[{"name":"nodeAttributes","version":"1.0"},{"name":"cyHiddenAttributes","version":"1.0"},{"name":"nodes","elementCount":2,"idCounter":909,"version":"1.0"},{"name":"cyNetworkRelations","version":"1.0"},{"name":"cyGroups","version":"1.0"},{"name":"networkAttributes","elementCount":1,"version":"1.0"},{"name":"cyTableColumn","elementCount":9,"version":"1.0"},{"name":"cartesianLayout","elementCount":2,"version":"1.0"},{"name":"edgeAttributes","elementCount":1,"version":"1.0"},{"name":"edges","elementCount":1,"idCounter":911,"version":"1.0"},{"name":"cyVisualProperties","elementCount":3,"version":"1.0"},{"name":"cySubNetworks","version":"1.0"}]},{"status":[{"error":"","success":true}]}]
"""

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
            if "NODE_SHAPE" in line["properties"]:
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
        self.calc_id_max()

        self.have_fd_network = False
        self.fd_nodes = []
        self.fd_edges = []

    def calc_id_max(self):
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

    def make_isa_network(self, edges):
        # edges -> io_nodes
        id_list = []
        for edge in edges:
            s = edge["s"]
            t = edge["t"]
            id_list.extend([s,t])
        id_list = list(set(id_list))

        for id_ in id_list:
            node = _find_name(self.io_nodes, id_)
            label = " ".join(["Obtain", node["n"]])
            node = {"@id": node["@id"], "n": label, "shape": "oval"}
            self.fd_nodes.append(node)

        for edge in edges:
            s = edge["s"]
            t = edge["t"]
            source_node = _find_name(self.io_nodes, s)
            newid = self.next_id()
            label = " ".join([source_node["n"], "way"])
            way_node = {"@id": newid, "n": label,
                        "shape": "rectangle", "fillcolor": "#d3d3d3"}
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

    def make_workflow_network(self,edges):
        for edge in edges:
            s = edge["s"]
            t = edge["t"]
            id_ = edge["@id"]
            # change the order between t and s
            self.fd_edges.append({"@id": id_, "s": s, "t": t})

        io_id_list = []
        device_id_list = []
        for edge in edges:
            s = edge["s"]
            t = edge["t"]
            try:
                snode = _find_name(self.io_nodes, s)
                io_id_list.append(s)
            except ValueError:
                snode = _find_name(self.device_nodes, s)
                device_id_list.append(s)
            try:
                tnode = _find_name(self.io_nodes, t)
                io_id_list.append(t)
            except ValueError:
                tnode = _find_name(self.device_nodes, t)
                device_id_list.append(t)

        io_id_list = list(set(io_id_list))
        device_id_list = list(set(device_id_list))

        for id_ in io_id_list:
            node = _find_name(self.io_nodes, id_)
            label = " ".join(["Obtain", node["n"]])
            node = {"@id": node["@id"], "n": label, "shape": "oval"}
            self.fd_nodes.append(node)

        for id_ in device_id_list:
            node = _find_name(self.device_nodes,id_)
            label = " ".join([node["n"], "way"])
            way_node = {"@id": node["@id"], "n": label,
                        "shape": "rectangle", "fillcolor": '#99FFFF'}
            self.fd_nodes.append(way_node)

            source_id = self.find_node_connection(way_node["@id"], "t")
            if source_id is not None:
                apply_node = self.make_apply_node(node)
                self.fd_nodes.append(apply_node)
                id_ = self.next_id()
                node = {"@id": id_, "s": apply_node["@id"], "t": node["@id"] }
                self.fd_edges.append(node)

        self.have_fd_network = True

    if True:
        def make_network(self):
            isa_edge = []
            workflow_edge = []
            for edge in self.edges:
                s = edge["s"]
                t = edge["t"]
                id_ = edge["@id"]
                try:
                    snode = _find_name(self.io_nodes, s)
                    snode_type = "io"
                except ValueError:
                    snode = _find_name(self.device_nodes, s)
                    snode_type = "device"
                try:
                    tnode = _find_name(self.io_nodes, t)
                    tnode_type = "io"
                except ValueError:
                    tnode = _find_name(self.device_nodes, t)
                    tnode_type = "device"

                if snode_type=="io" and tnode_type=="io":
                    isa_edge.append(edge)
                elif snode_type=="io" and tnode_type=="device":
                    workflow_edge.append(edge)
                elif snode_type=="device" and tnode_type=="io":
                    workflow_edge.append(edge)
                else:
                    print("connection error")
                    print(edge)
                    print("source node={}, target node={}".format(snode, tnode))
                    print("source node type={}, target node type={}".format(
                            snode_type, tnode_type))
                    raise ValueError

            self.make_isa_network(isa_edge)
            self.make_workflow_network(workflow_edge)

    else:
        def make_network(self, type_="workflow"):
            if not self.have_fd_network:
                if type_ == "workflow":
                    self.make_fd_network()
                elif type_ == "is-a":
                    self.make_isa_network()

    def graphviz_workflow(self, filename=None, rankdir="TB"):
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
            s = os.path.split(filename)
            # write to the current directory
            outputfilename = s[-1]
            g.render(outputfilename)
            print("save to", outputfilename)
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


class FDNPlotterBase:
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

def _multiple_lines(sentence, nlen=30):
    words = sentence.split(" ")
    lines = []
    line = ""
    for word in words:
        if len(line)==0:
            line = word
        else:
            n = len(line)+1+len(word)
            if n>=nlen:
                lines.append(line)
                line = ""
            line += " "+ word
    if len(line)>0:
        lines.append(line)
    return "\n".join(lines)


class FDNGraphvizPlotter(FDNPlotterBase):
    def __init__(self, cxnetwork_list, fix_node_id=True):
        super().__init__(cxnetwork_list, fix_node_id=True)

    def show(self, filename=None, rankdir="BT"):

        g = Digraph(format="png")
        g.attr('graph', rankdir=rankdir)

        for node in self.fd_nodes:
            if "fillcolor" in node:
                g.node(str(node["@id"]), label=_multiple_lines(node["n"]),
                       shape=node["shape"], style="filled",
                       fillcolor=node["fillcolor"])
            else:
                g.node(str(node["@id"]), label=_multiple_lines(node["n"]), 
                        shape=node["shape"])

        for edge in self.fd_edges:
            s = edge["s"]
            t = edge["t"]
            g.edge(str(s), str(t))

        if filename is not None:
            g.render(filename)
            print("save to", filename)
        g.view()


class FDNCXPlotter(FDNPlotterBase):
    def __init__(self, cxnetwork_list, fix_node_id=True):
        super().__init__(cxnetwork_list, fix_node_id=True)

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
        for node in self.fd_nodes:
            element_list = []
            if "shape" in node:
                shape_value = node["shape"].upper()
                if shape_value == "OVAL":
                    shape_value = "ELLIPSE"
                element_list.append(
                    {'NODE_SHAPE': shape_value})
            if "fillcolor" in node:
                fillcolor_value = node["fillcolor"].upper()
                element_list.append(
                    {'NODE_FILL_COLOR': fillcolor_value})
            if len(element_list) > 0:

                element_prop = {}
                for element in element_list:
                    element_prop.update(element)
                element = {'properties_of': 'nodes',
                           'applies_to': node["@id"],
                           'properties': element_prop}
                lines.append(element)
        return lines

    def save(self, network_name="fd_network", filename=None):
        change = True

        if True:
            network = json.loads(_CX_DEF1)
        else:
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
