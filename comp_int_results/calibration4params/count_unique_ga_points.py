import os, re, sys
import numpy as np
import xml.dom.minidom
from scipy.spatial import distance
import logging
import pandas as pd

'''
    Usage:

        $ python3 count_unique_ga_points.py <exp_folder> 

    where exp_folder is a (relative) path to a folder containing the generations.csv file
'''

generations_orig = os.path.join(os.path.dirname(os.path.realpath(__file__)),sys.argv[1],"generations.csv")

df = pd.read_csv(generations_orig)

bf = df.groupby(['x','y','z','g']).size().reset_index().rename(columns={0:'count'})

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(bf)
print("Total individuals: {}".format(bf['count'].sum()))
print("Total sims performed: {}".format(len(bf.index)))