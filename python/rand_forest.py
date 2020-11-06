import threading
import random
import time
import math
import csv
import json
import sys
import time
import pickle

import numpy as np
import itertools

from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

import eqpy, ga_utils

# list of ga_utils parameter objects
transformer = None


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
    # TODO determine if max'ing or min'ing and use -9999999 or 99999999
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


    # Initialization of dataset  

    x = make_random_points(num_init_population) 
    evals = evaluate(x)
    y = (list(map(lambda v : 0 if v>0 else 1, evals)))

    zeros, ones = y.count(0), y.count(1)
    printf("--- Init dataset has: {} positive and {} negative samples".format(ones,zeros))

    printf("--- Round -1 evaluations: ",evals)
    
    # Train the init random forest

    model = RandomForestClassifier(n_estimators=num_estimators)
    model.fit(x, y)


    # Active Learning with Random Forests

    points = create_grid()

    for i in range(num_iterations):

        # Predict class probabilities of testing points
        predictions = model.predict_proba(points)

        # Calculate the uncertainty of each testing point
        uncertainties = [min(posterior_prob) for posterior_prob in predictions]

        # Filter all (candidate) points having the maximum uncertainty
        max_uncertainty = max(uncertainties)
        max_indices = [i for i, u in enumerate(uncertainties) if u == max_uncertainty]
        candidate_points = [points[i] for i in max_indices]

        # Cluster candidate points if the points are more than the given number of clusters,
        # then select one point from each cluster
        if len(candidate_points) > num_population:
            k_means = KMeans(n_clusters=num_population, random_state=0).fit(np.array(candidate_points))
            labels = k_means.labels_
            selected_points = []
            for k in range(num_population):
                points_k = [p for i, p in enumerate(candidate_points) if labels[i] == k]
                selected_points.append(points_k[0])
        else:
            selected_points = candidate_points

        # Evaluate selected points
        labels = []
        evals = evaluate(selected_points)
        labels = (list(map(lambda v : 0 if v>0 else 1, evals)))
        printf("--- Round {} evaluations: ".format(i),evals)

        # Add evaluated points to the training set and re-train random forest
        x += selected_points
        y += labels
        model.fit(x, y)
        

    end_time = time.time()

    # fitnesses = [str(p.fitness.values[0]) for p in pop]

    eqpy.OUT_put("DONE")
    # # return the final population
    # eqpy.OUT_put("{}\n{}\n{}\n{}\n{}".format(create_list_of_json_strings(pop), ';'.join(fitnesses),
    #     start_time, log, end_time))
    eqpy.OUT_put("{}\n{}".format(start_time, end_time))

