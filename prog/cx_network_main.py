from graphviz import Digraph
import json
import numpy as np
from copy import deepcopy
from collections import OrderedDict
import sys

from cx_network import cxReader
from cx_network import FDNCXPlotter, FDNGraphvizPlotter

if __name__ == "__main__":
    import argparse

    def _parse_args():
        parser = argparse.ArgumentParser()

        parser.add_argument("--graphviz_workflow",
                            help="show workflows", action="store_true")
        parser.add_argument("--graphviz_is_a",
                            help="show is-a relation", action="store_true")
        parser.add_argument("--graphviz_FDN", action="store_true",
                            help="show graphviz FD network",
                            default=False)
        default_value = "fdn.png"
        parser.add_argument("--graphviz_FDN_filename",
                            help="output name (default: {})".format(
                                default_value),
                            default=default_value)

        parser.add_argument("--cx_FDN",
                            help="write cytoscape FD network in the CX format",
                            action="store_true")
        default_value = "output.cx"
        parser.add_argument("--cx_output_filename",
                            help="output name (default: {})".format(
                                default_value),
                            default=default_value)
        default_value = "fd_network"
        parser.add_argument("--cx_name",
                            help="Network name (default: {})".format(
                                default_value),
                            default=default_value)

        parser.add_argument("file", nargs="+")
        args = parser.parse_args()
        return args

    def main():
        args = _parse_args()
        filename_list = args.file

        cxreader_list = []
        for filename in filename_list:
            if "is-a" in filename:
                type_ = "is-a"
            else:
                type_ = "workflow"
            cxreader = cxReader(filename)
            cxreader.make_network(type_)
            if type_ == "workflow" and args.graphviz_workflow:
                cxreader.graphviz_workflow(filename+".png")
            if type_ == "is-a" and args.graphviz_is_a:
                cxreader.graphviz_workflow(
                    filename+".png", rankdir="TB")

            cxreader_list.append(cxreader)

        if args.graphviz_FDN:
            plotter = FDNGraphvizPlotter(cxreader_list)
            plotter.show(args.graphviz_FDN_filename)
        if args.cx_FDN:
            plotter = FDNCXPlotter(cxreader_list)
            plotter.save(args.cx_name, args.cx_output_filename)

    main()
