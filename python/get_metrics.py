import os, sys, glob
from scipy.spatial import distance
import numpy as np
import xml.dom.minidom
import logging
from datetime import datetime, time

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

def get_tumor_cell_count(instance_dir):
    """
    @return tumor cell count value from fname or -2, if file doesn't exist, or
    -1 if run terminated prematurely.
    """
    tumor_cell_count = '-2'
    fname = '{}/metrics.txt'.format(instance_dir)
    if os.path.exists(fname):
        file_lines = []
        with open(fname) as f_in:
            tumor_cell_count = '-1'
            file_lines.append(f_in.readlines()[-1].strip())
        file_lines.reverse() 
        items = file_lines[0].split("\t")
        if len(items) > 1:
            tumor_cell_count = items[1]

    return tumor_cell_count

def get_custom_cell_count(instance_dir):
    """
    @return tumor cell count value from fname or -2, if file doesn't exist, or
    -1 if run terminated prematurely.
    """
    output = '-2'
    fname = '{}/metrics.txt'.format(instance_dir)
    if os.path.exists(fname):
        file_lines = []
        with open(fname) as f_in:
            output = '-1'
            file_lines.append(f_in.readlines()[-1].strip())
        file_lines.reverse()
        items = file_lines[0].split("\t")
        if len(items) > 1:
            tumor_cell_count = int(items[1])
            death_cell_count = int(items[2])
            necrosis_cell_count = int(items[3])
            total_cells = tumor_cell_count + death_cell_count + necrosis_cell_count

            tumor_percent = tumor_cell_count * 100 / total_cells
            necrosis_percent = necrosis_cell_count * 100 / total_cells
            output = tumor_percent - necrosis_percent

    return output

def eucl_dist(x, y):
    dst = distance.euclidean(x, y)
    return dst

def get_simulation_dist(instance_dir, replication, emews_root):
    """
    @return distance value between fname and "data/original_physiboss_timeseries", or -2 if file doesn't exist, or
    -1 if run terminated prematurely.
    """
    experiment_folder = os.getenv('TURBINE_OUTPUT')
    distance_type_id = os.getenv('DISTANCE_TYPE_ID')
    logpath = os.path.join(instance_dir,'..','verbose_scores.log')
    logging.basicConfig(format='%(message)s',filename=logpath,level=logging.DEBUG)
    output = '-2'
    output2 = '-2'
    output3 = '-3'
    fname = '{}/metrics.txt'.format(instance_dir)
    if os.path.exists(fname):
        file_lines = []
        with open(fname) as f_in:
            output = '-1'
            tmp = f_in.readlines()
            file_lines = [x.strip() for x in tmp]
        # file_lines.reverse() 
        check = file_lines[-1].split("\t")
        if len(check) > 1:
            time_points = []
            tumor_cells = []
            death_cells = []
            necrosis_cells = []
            for i in range(len(file_lines)):
                items = file_lines[i].split("\t")
                time_points.append(int(items[0]))
                tumor_cells.append(int(items[1]))
                death_cells.append(int(items[2]))
                necrosis_cells.append(int(items[3]))

            # Find and parse corresponding original csv
            for i, f in enumerate(sorted(glob.glob(emews_root+'/data/original_physiboss_timeseries/*.csv'))):
                if i == int(replication):
                    csv_file = f
                    fh = open(csv_file)
                    tmp = fh.readlines()
                    lines = [x.strip() for x in tmp]
                    alive = []
                    apoptotic = []
                    necrotic = []
                    for i in time_points:
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

                    start_eucl = datetime.now()
                    output = eucl_dist(alive, tumor_cells)
                    output += eucl_dist(apoptotic, death_cells)
                    output += eucl_dist(necrotic, necrosis_cells)
                    end_eucl = datetime.now()

                    start_dtw = datetime.now()
                    outputDTWa = dtw(alive, tumor_cells)
                    outputDTWap = dtw(apoptotic, death_cells)
                    outputDTWn = dtw(necrotic, necrosis_cells)
                    end_dtw = datetime.now()
                    output2 = outputDTWa + outputDTWap + outputDTWn

                    start_l1 = datetime.now()
                    outputl1a = np.linalg.norm(np.asarray(alive) - np.asarray(tumor_cells), ord=1)
                    outputl1ap = np.linalg.norm(np.asarray(apoptotic) - np.asarray(death_cells), ord=1)
                    outputl1n = np.linalg.norm(np.asarray(necrotic) - np.asarray(necrosis_cells), ord=1)
                    end_l1 = datetime.now()
                    output3 = outputl1a + outputl1ap + outputl1n

                    doc = xml.dom.minidom.parse(os.path.join(instance_dir,"settings.xml"))
                    custom_data = doc.getElementsByTagName("TNFR_binding_rate")
                    k1 = custom_data[0].firstChild.nodeValue
                    custom_data = doc.getElementsByTagName("TNFR_endocytosis_rate")
                    k2 = custom_data[0].firstChild.nodeValue
                    custom_data = doc.getElementsByTagName("TNFR_recycling_rate")
                    k3 = custom_data[0].firstChild.nodeValue
                    logging.debug("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(replication, k1, k2, k3, output, eucl_dist(alive, tumor_cells), eucl_dist(apoptotic, death_cells),eucl_dist(necrotic, necrosis_cells), outputDTWa+outputDTWap+outputDTWn,outputDTWa, outputDTWap, outputDTWn, outputl1a+outputl1ap+outputl1n,outputl1a,outputl1ap,outputl1n,(end_eucl-start_eucl).total_seconds()*1000,(end_dtw-start_dtw).total_seconds()*1000,(end_l1-start_l1).total_seconds()*1000 ))
    else:
        logging.error("File metrics.txt not found!")
    if distance_type_id == 'dtw':
        return output2
    elif distance_type_id == 'l1':
        return output3
    else:
        return output

