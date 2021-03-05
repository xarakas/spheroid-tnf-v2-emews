import os, re
import numpy as np
import xml.dom.minidom
from scipy.spatial import distance
import logging
import pandas as pd

logpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'sweep_log_drug_discovery_filtered.log')
logging.basicConfig(format='%(message)s',filename=logpath,level=logging.DEBUG)
logging.debug("id,k1,k2,k3,score,score_init")

for path, subdirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
    #print("Path {}\n subdirs {}\n files {}".format(path,subdirs,files))
    tumor_cells = []
    try:
        for name in files:
            #print("Name {}\n in files {}".format(name,files))
            text2 = 'instance_(.+?)/'
            #print(text2, os.path.join(path, name))
            found2 = re.search(text2, os.path.join(path, name)).group(1)
            if "metrics.txt" in name:
                fname2=os.path.join(path,"settings.xml")
                doc = xml.dom.minidom.parse(fname2)
                custom_data = doc.getElementsByTagName("time_add_tnf")
                k1 = custom_data[0].firstChild.nodeValue
                custom_data = doc.getElementsByTagName("duration_add_tnf")
                k2 = custom_data[0].firstChild.nodeValue
                custom_data = doc.getElementsByTagName("concentration_tnf")
                k3 = custom_data[0].firstChild.nodeValue
                fname1=os.path.join(path,name)
                df = pd.read_csv(fname1,sep="\t", names=['time', 'alive', 'apoptotic', 'necrotic'])
                tumor_cell_count = '-2'
                
                tumor_cells = df['alive'].tolist()
                if tumor_cells[0] > tumor_cells[-1]:
                    logging.debug("{},{},{},{},{},{}".format(found2, k1, k2, k3, tumor_cells[-1], tumor_cells[0]))
            else:
                continue
                
    except AttributeError:
                found = ''
        
                
    
    tumor_cells = []
    k1=0
    k2=0
    k3=0
