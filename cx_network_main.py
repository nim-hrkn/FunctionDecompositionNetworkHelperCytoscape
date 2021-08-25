from graphviz import Digraph
import json
import numpy as np
from copy import deepcopy
from collections import OrderedDict
import sys

from cx_network import cxReader
from cx_network import FDNPlotter


if __name__ == "__main__":
    import argparse
    action = 2
    if action == 1:
        import sys
        file_list = sys.argv[1:]

    elif action == 2:
        parser = argparse.ArgumentParser()
        parser.add_argument("--show_workflow",
                            help="show workflows", action="store_true")
        parser.add_argument(
            "--show_is_a", help="show is-a relation", action="store_true")
        parser.add_argument("file", nargs="+")
        args = parser.parse_args()

        print(args.show_workflow)
        print(args.show_is_a)
        print(args.file)
        filename_list = args.file

    elif action == 3:
        # test set
        filename_list = ["light_workflow.cx",
                         "reading_workflow.cx", "light_is-a.cx"]

        class argDummy:
            def __init__(self):
                self.show_workflow = True
                self.show_is_a = False
        args = argDummy()

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

    plotter.graphviz_fd_network("df_network")
    # cxreader.cx_fd_network("temp","output.cx")

