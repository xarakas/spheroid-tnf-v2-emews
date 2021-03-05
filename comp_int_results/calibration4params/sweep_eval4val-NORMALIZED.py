import os, re
import numpy as np
import xml.dom.minidom
from scipy.spatial import distance
import logging
import pandas as pd

logpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'sweep_log_eucl_dtw_l1-NORMALIZED-4params.log')
logging.basicConfig(format='%(message)s',filename=logpath,level=logging.DEBUG)
logging.debug("id,GS,k1,k2,k3,k4,Eucl,Eucl_alive,Eucl_apoptotic,Eucl_necrotic,DTW,DTW_alive,DTW_apoptotic,DTW_necrotic,l1,l1_alive,l1_apoptotic,l1_necrotic")
# Dynamic Time Warping
def dtw(s, t):
    n, m = len(s), len(t)
    dtwM = np.zeros((n+1, m+1))
    for i in range(n+1):
        for j in range(m+1):
            dtwM[i, j] = np.inf
    dtwM[0, 0] = 0
    
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = abs(s[i-1] - t[j-1])
            # take last min from a square box
            last_min = np.min([dtwM[i-1, j], dtwM[i, j-1], dtwM[i-1, j-1]])
            dtwM[i, j] = cost + last_min
    return dtwM[-1,-1]

def eucl_dist(x, y):
    dst = distance.euclidean(x, y)
    return dst


for path, subdirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
    time_points = []
    tumor_cells = []
    death_cells = []
    necrosis_cells = []
    alive = []
    apoptotic = []
    necrotic = []
    k1=0
    k2=0
    k3=0
    k4=0
    csv_file1 = os.path.join(os.path.dirname(os.path.realpath(__file__)),"TNF_2_pulse600_cell_vs_time.csv")
    fh1 = open(csv_file1)
    tmp1 = fh1.readlines()
    csv_file2 = os.path.join(os.path.dirname(os.path.realpath(__file__)),"TNF_1_pulse150_cell_vs_time.csv")
    fh2 = open(csv_file2)
    tmp2 = fh2.readlines()
    for name in files:
        if "metrics.txt" in name:
            fname2=os.path.join(path,"settings.xml")
            doc = xml.dom.minidom.parse(fname2)
            custom_data = doc.getElementsByTagName("TNFR_binding_rate")
            k1 = custom_data[0].firstChild.nodeValue
            custom_data = doc.getElementsByTagName("TNFR_endocytosis_rate")
            k2 = custom_data[0].firstChild.nodeValue
            custom_data = doc.getElementsByTagName("TNFR_recycling_rate")
            k3 = custom_data[0].firstChild.nodeValue
            custom_data = doc.getElementsByTagName("rate")
            k4 = custom_data[0].firstChild.nodeValue
            fname1=os.path.join(path,name)
            df = pd.read_csv(fname1,sep="\t", names=['time', 'alive', 'apoptotic', 'necrotic'])
            try:
                time_points = df['time'].tolist()
                tumor_cells = df['alive'].tolist()
                death_cells = df['apoptotic'].tolist()
                necrosis_cells = df['necrotic'].tolist()
                time_points = time_points[0:48]
                tumor_cells = tumor_cells[0:48]
                death_cells = death_cells[0:48]
                necrosis_cells = necrosis_cells[0:48]
                text = 'sweep-calibration-(.+?)/'
                text2 = 'instance_(.+?)/'
                norm_val = 0
            except KeyError:
                print("{} has missing file".format(path))
                continue
            try:
                found = re.search(text, os.path.join(path, name)).group(1)
                found2 = re.search(text2, os.path.join(path, name)).group(1)
                if found=="600":
                    lines = [x.strip() for x in tmp1]

                    for i in time_points:#range(len(lines)):
                        #if i>0:
                        data = lines[int(i)+1].split('\t')
                        alive.append(float(data[2]))
                        apoptotic.append(float(data[3]))
                        necrotic.append(float(data[4]))
                    norm_val = max(alive)
                    alive[:] = [x / norm_val for x in alive]
                    apoptotic[:] = [x / norm_val for x in apoptotic]
                    necrotic[:] = [x / norm_val for x in necrotic]
                else:
                    lines = [x.strip() for x in tmp2]
                    # print(len(lines))
                    # print(lines)
                    for i in time_points:#range(len(lines)):
                        #if i>0:
                        # print(i)
                        data = lines[int(i)+1].split('\t')
                        alive.append(float(data[2]))
                        apoptotic.append(float(data[3]))
                        necrotic.append(float(data[4]))
                    norm_val = max(alive)
                    alive[:] = [x / norm_val for x in alive]
                    apoptotic[:] = [x / norm_val for x in apoptotic]
                    necrotic[:] = [x / norm_val for x in necrotic]
                tumor_cells[:] = [x / norm_val for x in tumor_cells]
                death_cells[:] = [x / norm_val for x in death_cells]
                necrosis_cells[:] = [x / norm_val for x in necrosis_cells]
                # print("Case "+str(tumor_cells))
                # print("GS" +str(alive))
                output = eucl_dist(alive, tumor_cells)
                output += eucl_dist(apoptotic, death_cells)
                output += eucl_dist(necrotic, necrosis_cells)  
                outputDTWa = dtw(alive, tumor_cells)
                outputDTWap = dtw(apoptotic, death_cells)
                outputDTWn = dtw(necrotic, necrosis_cells)
                outputl1a = np.linalg.norm(np.asarray(alive) - np.asarray(tumor_cells), ord=1)
                outputl1ap = np.linalg.norm(np.asarray(apoptotic) - np.asarray(death_cells), ord=1)
                outputl1n = np.linalg.norm(np.asarray(necrotic) - np.asarray(necrosis_cells), ord=1)
                score=output
                logging.debug("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(found2, found, k1, k2, k3, k4, score, eucl_dist(alive, tumor_cells), eucl_dist(apoptotic, death_cells) , eucl_dist(necrotic, necrosis_cells),outputDTWa+outputDTWap+outputDTWn, outputDTWa, outputDTWap, outputDTWn,outputl1a+outputl1ap+outputl1n,outputl1a,outputl1ap,outputl1n))
                # d.append([found2, found, k1, k2, k3, score, eucl_dist(alive, tumor_cells), eucl_dist(apoptotic, death_cells) , eucl_dist(necrotic, necrosis_cells),outputDTWa+outputDTWap+outputDTWn, outputDTWa, outputDTWap, outputDTWn])
            except AttributeError:
                found = ''
            

        else:
            continue
            #print(name)
            
    time_points = []
    tumor_cells = []
    death_cells = []
    necrosis_cells = []
    alive = []
    apoptotic = []
    necrotic = []    
    k1=0
    k2=0
    k3=0
    k4=0
