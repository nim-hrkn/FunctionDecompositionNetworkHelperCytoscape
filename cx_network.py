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


class cxNetwork:
    def __init__(self, filename):
        with open(filename) as f:
            network = json.load(f)
        self.network = network
        self.analyze_nodes()
        self.analyze_id()
        
        self.have_fd_network = False
        
    def analyze_id(self):
        id_max = 0
        for node in self.io_nodes:
            id_max = max(id_max,node["@id"])
        for node in self.device_nodes:
            id_max = max(id_max,node["@id"])            
        for node in self.edges:
            id_max = max(id_max,node["@id"])  
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

    def graphviz_workflow(self, filename=None):
        g = Digraph(format="png")
        g.attr('graph', rankdir="BT")
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
        
    def make_apply_node(self, device_node):
        label = " ".join(["apply", device_node["n"]])
        newid = self.next_id()
        node = {"@id": newid, "n":label, "shape":"hexagon"}
        return node
        
    def make_fd_network(self):
        self.fd_nodes = []
        self.fd_edges = []
        
        for edge in self.edges:
            s = edge["s"]
            t = edge["t"]
            id_ = edge["@id"]
            self.fd_edges.append({"@id":id_, "s": t, "t":s})
            
        for node in self.io_nodes:
            label = " ".join(["obtain",node["n"]])
            node = {"@id": node["@id"], "n": node["n"], "shape":"oval"}
            self.fd_nodes.append(node)
            
        for node in self.device_nodes:
            label = " ".join([node["n"],"way"])
            way_node = {"@id": node["@id"], "n": label, "shape":"rectangle"}

            self.fd_nodes.append(way_node)
            
            apply_node = self.make_apply_node(node)

            self.fd_nodes.append(apply_node)
            
            id_ = self.next_id()
            node = {"@id":id_, "s": node["@id"], "t":apply_node["@id"]}
            self.fd_edges.append(node)
            
        self.have_fd_network = True
            
    def graphviz_fd_network(self, filename=None):
        
        if not self.have_fd_network:
            self.make_fd_network()
            
        g = Digraph(format="png")
        for node in self.fd_nodes:

            g.node(str(node["@id"]), label=node["n"], shape=node["shape"])

        for edge in self.fd_edges:
            s = edge["s"]
            t = edge["t"]
            g.edge(str(s), str(t))
            
        if filename is not None:
            g.render(filename)
        g.view()        
        
    def cx_fd_network(self, name, filename):
        if not self.have_fd_network:
            self.make_fd_network()
        
        data = []
        
        key = "numberVerification"
        datum = {key: [{'longNumber': 281474976710655}]}
        data.append(datum)
        
        key = "metaData"
        meta_data = [{'name': 'nodeAttributes', 'version': '1.0'},
        {'name': 'cyHiddenAttributes', 'version': '1.0'}, 
        {'name': 'nodes', 'version': '1.0'}, 
        {'name': 'cyNetworkRelations', 'version': '1.0'}, 
        {'name': 'cyGroups', 'version': '1.0'}, 
        {'name': 'networkAttributes', 'version': '1.0'}, 
        {'name': 'cyTableColumn', 'version': '1.0'}, 
        {'name': 'cartesianLayout', 'version': '1.0'}, 
        {'name': 'edgeAttributes', 'version': '1.0'}, 
        {'name': 'edges', 'version': '1.0'}, 
        {'name': 'cyVisualProperties', 'version': '1.0'}, 
        {'name': 'cySubNetworks', 'version': '1.0'}]

        datum = {key: meta_data}
        data.append(datum)
        
        
        key = "cyTableColumn"        
        values = """[{'applies_to': 'node_table', 'n': 'shared name'}, {'applies_to': 'node_table', 'n': 'name'}, {'applies_to': 'node_table', 'n': 'id'}, {'applies_to': 'node_table', 'n': 'shared_name'}, {'applies_to': 'edge_table', 'n': 'shared name'}, {'applies_to': 'edge_table', 'n': 'shared interaction'}, {'applies_to': 'edge_table', 'n': 'name'}, {'applies_to': 'edge_table', 'n': 'interaction'}, {'applies_to': 'edge_table', 'n': 'id'}, {'applies_to': 'edge_table', 'n': 'source'}, {'applies_to': 'edge_table', 'n': 'target'}, {'applies_to': 'edge_table', 'n': 'shared_name'}, {'applies_to': 'edge_table', 'n': 'shared_interaction'}, {'applies_to': 'network_table', 'n': 'shared name'}, {'applies_to': 'network_table', 'n': 'name'}, {'applies_to': 'network_table', 'n': 'shared_name'}, {'applies_to': 'network_table', 'n': '__Annotations', 'd': 'list_of_string'}]
"""
        datum = {key: values}
        data.append(datum)
        
        key = 'networkAttributes'
        values = [{'n': 'name', 'v': name}]
        datum = {key: values} 
        data.append(datum)
        
        key = "nodes"
        nodes_data = []
        for node in self.fd_nodes:
            value = {"@id": node["@id"], "n":node["n"]}
            nodes_data.append(value)
        datum = {key: nodes_data}
        data.append(datum)

        key = "edges"
        edges_data = []            
        for node in self.fd_edges:
            value = {"@id":node["@id"], "s": node["s"], "t": node["t"], 'i': 'interacts with'}
            edges_data.append(value)
        datum = {key: edges_data}            
        data.append(datum)
        
        if False:
            key = "nodeAttributes"
            nodes_data = []
            for node in self.fd_nodes:
                value = {"po": node["@id"], "n": "shared_name", "v":node["n"]}
                nodes_data.append(value)
                value = {"po": node["@id"], "n": "id", "v":str(node["@id"])}
                nodes_data.append(value)
            datum = {key: nodes_data}
            data.append(datum)

        
        key = "edgeAttributes"
        edges_data = []
        for node in self.fd_edges:
            if False:
                value = {'po': node["@id"], 'n': 'shared_interaction', 'v': 'interacts with'}
                edges_data.append(value)
            
            source_node = _find_name(self.fd_nodes, node["s"])
            target_node = _find_name(self.fd_nodes, node["t"])
            value = {'po': node["@id"], 'n': 'name', 
                     'v': " ".join([source_node["n"],'(interacts with)',target_node["n"]])}
            edges_data.append(value)
        datum = {key: edges_data}
        data.append(datum)
  
        
        key = "cyVisualProperties"
        prop_data = []
        for node in self.fd_nodes:
            if node["shape"] != "oval":
                value = {'properties_of': 'nodes', "applyies_to": node["@id"], 
                         'properties': {'NODE_SHAPE': node["shape"].upper()}}
                prop_data.append(value)
        datum = {key: prop_data}
        data.append(datum)
        
       
        key = "status"
        status_data = [{'error': '', 'success': True}]
        datum = {key: status_data}
        data.append(datum)
       
        
        
        if filename is not None:
            with open(filename,"w") as f:
                json.dump(data,f)
            print("save to",filename)

