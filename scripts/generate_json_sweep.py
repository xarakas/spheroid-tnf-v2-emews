#!/usr/bin/env python
# coding: utf-

import json
import argparse
import numpy as np
from numpy.random import normal
from numpy.random import uniform

from sklearn.model_selection import ParameterGrid

MODES = ("uniform", "normal", "grid")

def create_parser():
    parser = argparse.ArgumentParser(description="Parameter grid generator to run model exploration sweep")
    parser.add_argument("param_json", action="store", help="JSON file having param name as key and a dic with ref values")
    parser.add_argument("--out", action="store", help="output name", default=None)
    parser.add_argument("--mode", action="store", help="Sampling mode", choices=MODES, default='grid')
    parser.add_argument("--size", action="store", type=int, help="Total values for each parameter")
    return parser


def main():
    
    parser = create_parser()
    args = parser.parse_args()
    params = {}
    with open(args.param_json) as fh:
        params = json.load(fh)

    grid = {}
    if args.mode == "uniform":
        for k,v in params.items():
            grid[k] = uniform(v['min'], v['max'], size=(args.size,))
    if args.mode == "normal":
        for k,v in params.items():
            grid[k] = normal(loc=v['loc'], scale=v['scale'], size=(args.size,))
    if args.mode == "grid":
        for k,v in params.items():
            grid[k] = np.linspace(v['min'], v['max'], args.size)


    if args.out is not None:
        with open(args.out, 'w') as fh:
            for p in ParameterGrid(grid):
                print(json.dumps(p), file=fh)
    else:
        for p in ParameterGrid(grid):
            print(json.dumps(p))

main()



