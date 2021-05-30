import threading
import random
import time
import math
import csv
import json
import sys
import time
import pickle
import logging
import os
import matplotlib.pyplot as plt
import numpy as np
import itertools
from sklearn.cluster import Birch,KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import DBSCAN,OPTICS, cluster_optics_dbscan

import eqpy, ga_utils


experiment_folder = os.getenv('TURBINE_OUTPUT')
logging.basicConfig(format='%(message)s',filemode = 'a+',filename=os.path.join(experiment_folder,"iterations.log"),level=logging.DEBUG)

with open(os.path.join(experiment_folder,'..','..',os.getenv('RAND_CONFIG_FILE'))) as f:
    rand_config = json.load(f)

clustering_method = rand_config['method']
param1 = rand_config['param1'] #KMEANS->k, DBSCAN->eps, BIRCH->branching factor
param2 = rand_config['param2'] #KMEANS->Nothing, DBSCAN->MinPts, BIRCH->threshold

transformer = None
fileDir = os.getcwd()
previous_results_file = os.path.join(fileDir, '../../python/all_exps_DD.csv')
# previous_results_file = '/gpfs/scratch/bsc08/bsc08646/vasilis/spheroid-tnf-v2-emews/python/all_exps_DD.csv'

#
def create_plot(dimension,iteration,interesting_points,non_interesting_points,selected_points):

    plt.scatter(interesting_points[:,1],interesting_points[:,2],color='red')
    plt.scatter(non_interesting_points[:,1],non_interesting_points[:,2],color='blue')
    plt.scatter(selected_points[:,1],selected_points[:,2],color='yellow')
    plt.savefig("fig_{}_{}.png")
#
class Transformer:

    def __init__(self, ga_params, clf = None, scaler = None):
        self.ga_params = ga_params

    def random_params(self):
        draws = []
        for p in self.ga_params:
            draws.append(p.randomDraw())
        return draws

    def parse_init_params(self, params_file):
        init_params = []
        with open(params_file) as f_in:
            reader = csv.reader(f_in)
            header = next(reader)
            for row in reader:
                init_params.append(dict(zip(header,row)))
        return init_params

    def create_grid(self):
        ranges = []
        n_points = 100
        for p in self.ga_params:
            rr = p.get_points(n_points)
            ranges.append(rr)

        points = list(itertools.product(*ranges))
        return points


def printf(val):
    print()
    print(val)
    print()
    sys.stdout.flush()

# {"batch_size":512,"epochs":51,"activation":"softsign",
#"dense":"2000 1000 1000 500 100 50","optimizer":"adagrad","drop":0.1378,
#"learning_rate":0.0301,"conv":"25 25 25 25 25 1"}
def create_list_of_json_strings(list_of_lists, super_delim=";"):
    # create string of ; separated jsonified maps
    res = []
    global transformer
    for l in list_of_lists:
        jmap = {}
        for i,p in enumerate(transformer.ga_params):
            jmap[p.name] = l[i]

        jstring = json.dumps(jmap)
        res.append(jstring)

    return (super_delim.join(res))

def evaluate(points):
    # sending data that looks like:
    # [[a,b,c,d],[e,f,g,h],...]
    if not points:
        return []

    eqpy.OUT_put(create_list_of_json_strings(points))
    result = eqpy.IN_get()
    split_result = result.split(';')
    return [float(x) if not math.isnan(float(x)) else (float(99999999),) for x in split_result]


def make_random_parameters():
    """
    Performs initial random draw on each parameter
    """
    return transformer.random_params()

def make_random_points(n_init_points):
    points = []
    for i in range(n_init_points):
        point = make_random_parameters()
        points.append(point)
    return points

def create_grid():
    """
    Creates a grid in the parameter space
    """
    return transformer.create_grid()

def file_to_dict(filename,evaluated_points_dict):

    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for line in reader:
            k1_l = eval(line[1])
            k2_l = eval(line[2])
            k3_l = eval(line[3])
            point = (k1_l,k2_l,k3_l)
            score = eval(line[4])
            score_init = eval(line[5])

            percentage = 1.0*score/score_init

            evaluated_points_dict[str(point)] = percentage

    return

def run():
    """
    :param num_iterations: iterations of the active learning algorithm
    :param num_estimators: number of classification trees to be combined for creating each rf
    :param seed: random seed
    :param rf_parameters_file: rf parameters file name (e.g., "ga_params.json")
    :param num_init_population: size of init random "dataset" for learning the initial rf
    :param num_population: upper bound on the points to be evaluated in each iteration
    """
    eqpy.OUT_put("Params")
    parameters = eqpy.IN_get()

    # parse params
    printf("--- Parameters: {}".format(parameters))
    (num_iterations, num_estimators, num_init_population, num_population, seed, rf_parameters_file) = eval('{}'.format(parameters))
    random.seed(seed)
    rf_parameters = ga_utils.create_parameters(rf_parameters_file)
    global transformer
    transformer = Transformer(rf_parameters)

    # num_iter-1 generations since the initial population is evaluated once first
    start_time = time.time()

    evaluated_points_from_file = {}

    file_to_dict(previous_results_file,evaluated_points_from_file)

    #dictionary to save already evaluated points of this run and their results
    evaluated_points = {}

    # Initialization of dataset
    x = make_random_points(num_init_population)

    x_new = [point for point in x if (str(point) not in evaluated_points_from_file)]
    x_not = [point for point in x if (str(point) in evaluated_points_from_file)]

    evals_new = evaluate(x_new)

    evals_n = []

    for i in range(len(x_not)):
        evals_n.append(evaluated_points_from_file[str(x_not[i])])

    evals = evals_new+evals_n
    x = x_new+x_not

    y = (list(map(lambda v : 0 if v>0.3 else 1, evals)))
    zeros, ones = y.count(0), y.count(1)
    printf("--- Init dataset has: {} positive and {} negative samples".format(ones,zeros))

    printf("--- Round -1 evaluations:{}".format(evals))

    #log training points and their labels
    logging.debug("{}".format(x))
    logging.debug("{}".format(evals))
    logging.debug("{}".format(y))
    logging.debug("{}".format(x_not))
    logging.debug("{}".format(evals_n))
    logging.debug("{}".format(x_new))
    logging.debug("{}".format(evals_new))


    for i in range(len(x)):
        evaluated_points[str(x[i])] = evals[i]


    # Train random forest classifier
    model = RandomForestClassifier(n_estimators=num_estimators)
    model.fit(x, y)


    # Active Learning with Random Forests
    points = create_grid()
    logging.debug("{}".format(points))



    # Predict class probabilities of testing points
    predictions = model.predict_proba(points)
    predictions_to_list = predictions.tolist()
    logging.debug("{}".format(predictions_to_list))

    # Calculate the uncertainty of each testing point
    uncertainties = [min(posterior_prob) for posterior_prob in predictions]
    # Filter all (candidate) points having uncertainty above our threshold
    uncertainty_threshold = 0.4
    max_indices = [i for i, u in enumerate(uncertainties) if u >= uncertainty_threshold]
    candidate_points = [points[i] for i in max_indices]

    for it in range(num_iterations):

        # Cluster candidate points if the points are more than the given number of clusters,
        # then select one point from each cluster

        logging.debug("{}".format(candidate_points))

        if len(candidate_points) > num_population:
            selected_points = []
            if(clustering_method=='KMEANS'):
                k_means = KMeans(n_clusters=param1, random_state=0).fit(np.array(candidate_points))
                labels = k_means.labels_

                for k in range(num_population):
                    points_k = [p for i, p in enumerate(candidate_points) if labels[i] == k]
                    selected_points.append(points_k[0])

            elif(clustering_method=='DBSCAN'):
                candidate_points_arr_no_norm = np.asarray(candidate_points)
                candidate_points_arr = candidate_points_arr_no_norm / candidate_points_arr_no_norm.max(axis=0)
                db = DBSCAN(eps=param1,min_samples=param2).fit(candidate_points_arr)
                labels = db.labels_

                n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                n_outliers = list(labels).count(-1)
                core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
                core_samples_mask[db.core_sample_indices_] = True

                printf("Round_{} clusters: {}".format(it,n_clusters))
                printf("Round_{} outliers: {}".format(it,n_outliers))
                printf("Round_{} candidates: {}".format(it,len(candidate_points)))

                for k in range(n_clusters):
                    class_member_mask = (labels == k)
                    core_points_k = candidate_points_arr_no_norm[class_member_mask & core_samples_mask]
                    selected_points.append(core_points_k[0])

            elif(clustering_method=='BIRCH'):
                candidate_points_arr_no_norm = np.asarray(candidate_points)
                candidate_points_arr = candidate_points_arr_no_norm / candidate_points_arr_no_norm.max(axis=0)
                max_axes = candidate_points_arr_no_norm.max(axis=0)
                clusterer = Birch(branching_factor = param1, n_clusters = None, threshold = param2)
                labels = clusterer.fit_predict(candidate_points_arr)
                n_clusters = np.unique(labels).size
                cluster_centers = clusterer.subcluster_centers_*max_axes
                selected_points = cluster_centers.tolist()
                printf("Round_{} clusters: {}".format(it,n_clusters))

            else:
                logging.info("Unknown Clustering Method value: '{}'... Exiting".format(clustering_method))
                return
        else:
            selected_points = candidate_points

        labels_to_list = labels.tolist()
        logging.debug("{}".format(labels_to_list))
        logging.debug("{}".format(selected_points))

        selected_points_n = []
        selected_points_not = []
        selected_points_n = [point for point in selected_points if (str(point) not in evaluated_points_from_file)]
        selected_points_not = [point for point in selected_points if (str(point) in evaluated_points_from_file)]
        points_already_selected_in_prev_iter = [point for point in selected_points if (str(point) in evaluated_points)]

        logging.debug("{}".format(selected_points_n))
        logging.debug("{}".format(selected_points_not))
        logging.debug("{}".format(points_already_selected_in_prev_iter))

        # Evaluate selected points
        labels = []
        evals = evaluate(selected_points_n)

        evals_n = []

        for i in range(len(selected_points_not)):
            evals_n.append(evaluated_points_from_file[str(selected_points_not[i])])

        logging.debug("{}".format(evals))
        logging.debug("{}".format(evals_n))

        selected_points = selected_points_n+selected_points_not
        evals = evals+evals_n

        logging.debug("{}".format(selected_points))
        logging.debug("{}".format(evals))

        #1136
        labels = (list(map(lambda v : 0 if v>0.3 else 1, evals)))
        printf("--- Round {} evaluations {}: ".format(it,evals))

        logging.debug("{}".format(labels))

        # Add evaluated points to the training set and re-train random forest
        x += selected_points
        y += labels
        model.fit(x, y)

        for i in range(len(selected_points)):
            evaluated_points[str(selected_points[i])] = evals[i]

        predictions = model.predict_proba(points)
        predictions_to_list = predictions.tolist()
        logging.debug("{}".format(predictions_to_list))

        uncertainties = [min(posterior_prob) for posterior_prob in predictions]
        # Filter all (candidate) points having the maximum uncertainty
        max_uncertainty = max(uncertainties)
        max_indices = [i for i, u in enumerate(uncertainties) if u >= uncertainty_threshold]
        candidate_points = [points[i] for i in max_indices]


    end_time = time.time()


    eqpy.OUT_put("DONE")

    eqpy.OUT_put("{}\n{}\n{}\n{}".format(create_list_of_json_strings(selected_points), ';'.join(evals),
        start_time, end_time))
