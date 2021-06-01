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

import eqpy, ga_utils

experiment_folder = os.getenv('TURBINE_OUTPUT')
with open(os.path.join(experiment_folder,'..','..',os.getenv('SA_CONFIG_FILE'))) as f:
    sa_config = json.load(f)

temperature = sa_config['temperature']
min_temperature = sa_config['min_temperature']
cooling = sa_config['cooling']
max_iterations = sa_config['max_iterations']
distance_threshold = sa_config['distance_threshold']
seeded_pop = sa_config['seeded_pop']
filename = os.path.join(experiment_folder,"annealing.log")

transformer = None

class Transformer:

    def __init__(self, sa_params, clf = None, scaler = None):
        self.sa_params = sa_params

    def random_params(self):
        draws = []
        for p in self.sa_params:
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
        for p in self.sa_params:
            rr = p.get_points(n_points)
            ranges.append(rr)

        points = list(itertools.product(*ranges))
        return points

def printf(val):
    print(val)
    sys.stdout.flush()

# def obj_func(x):
#     return 0

def create_list_of_json_strings(list_of_lists, super_delim=";"):
    # create string of ; separated jsonified maps
    res = []
    global transformer
    for l in list_of_lists:
        jmap = {}
        for i,p in enumerate(transformer.sa_params):
            jmap[p.name] = l[i]

        jstring = json.dumps(jmap)
        res.append(jstring)

    return (super_delim.join(res))

def evaluate_one_point(point):

    global transformer
    jmap = {}

    for i,p in enumerate(transformer.sa_params):
        jmap[p.name] = point[i]

    jstring = json.dumps(jmap)

    eqpy.OUT_put(jstring)
    result = eqpy.IN_get()
    split_result = result.split(';')
    score_list = [float(x) if not math.isnan(float(x)) else (float(99999999),) for x in split_result]

    return score_list[0]

def evaluate_multiple_points(pops):

    if not pops:
        return []

    eqpy.OUT_put(create_list_of_json_strings(pops))
    result = eqpy.IN_get()
    split_result = result.split(';')
    # TODO determine if max'ing or min'ing and use -9999999 or 99999999
    return [float(x) if not math.isnan(float(x)) else (float(99999999),) for x in split_result]

def create_grid():
    """
    Creates a grid in the parameter space
    """
    return transformer.create_grid()

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

class Simulated_Annealing():

    def __init__(self,pop,temperature,min_temperature,cooling,max_iterations,distance_threshold):
        self.grid = pop
        self.pop_num = len(pop)
        self.temperature = temperature
        self.stop = min_temperature
        self.cooling = cooling
        self.max_iterations = max_iterations
        self.distance_threshold = distance_threshold
        self.max_dims = list(map(max, zip(*pop)))
        self.best_point = None
        self.best_score = math.inf
        self.history = []
        self.history_scores = []
        self.current_score = []
        self.current_point = []

    def verbose(self,filename):

        logging.basicConfig(format='%(message)s',filemode = 'a+',filename=filename,level=logging.DEBUG)
        logging.debug("{}".format(self.best_point))
        logging.debug("{}".format(self.best_score))
        logging.debug("{}".format(self.history))
        logging.debug("{}".format(self.history_scores))
        logging.debug("{}".format(self.temperature))

        return

    def distance(self,point1,point2):
        if(point1==point2):
            return 100.0
        return math.sqrt(((point1[0]-point2[0])/self.max_dims[0])**2 + ((point1[1]-point2[1])/self.max_dims[1])**2 + ((point1[2]-point2[2])/self.max_dims[2])**2)

    def cool(self):
        #temperature reduction
        self.temperature *= self.cooling
        return


    def accept(self,candidate_point):
        #candidate point acceptance
        candidate_score = evaluate_one_point(candidate_point)
        printf("Candidate: {}".format(candidate_point))
        printf("Candidate's Score: {}".format(candidate_score))
        self.history.append(candidate_point)
        self.history_scores.append(candidate_score)

        DE =  candidate_score - self.current_score

        if(DE < 0):
            self.current_point = candidate_point
            self.current_score = candidate_score


            if(self.current_score<self.best_score):
                self.best_score = self.current_score
                self.best_point = candidate_point
        else:

            probability = random.random()
            thresh = math.exp(-(DE/self.temperature))

            if(thresh>probability):
                    self.current_point = candidate_point
                    self.current_score = candidate_score

        return


    def inititialize(self):
        #get initial point and its score
        if(seeded_pop == "YES"):
            # fileDir = os.path.dirname(os.path.realpath('__file__'))
            fileDir = os.getcwd()
            # '../best_point.txt'
            with open(os.path.join(fileDir, '../../python/best_point.txt')) as f:
                initial_point = eval(f.readline())
                printf("Seeded initial point")
        else:
            initial_point = random.choice(self.grid)

        printf("Initial Point: {}".format(initial_point))
        initial_score = evaluate_one_point(initial_point)
        self.current_point = initial_point
        self.current_score = initial_score
        self.history.append(initial_point)
        self.history_scores.append(initial_score)
        printf("Initial evaluation: {}".format(initial_score))

        return

    def anneal(self):

        printf("Start Time: {}".format(time.time()))
        self.inititialize()

        while self.temperature >= self.stop:
            iterations = 0
            printf("Tempeature: {}".format(self.temperature))

            while iterations < self.max_iterations:
                iterations += 1
                candidates = [point for point in self.grid if self.distance(self.current_point,point) < self.distance_threshold]
                candidate_point = random.choice(candidates)

                self.accept(candidate_point)
            self.verbose(filename)
            self.cool()

        printf("End Time: {}".format(time.time()))
        return

def run():

    eqpy.OUT_put("Params")
    parameters = eqpy.IN_get()
    (num_iterations, num_population, seed, sa_parameters_file) = eval('{}'.format(parameters))
    random.seed(seed)
    sa_parameters = ga_utils.create_parameters(sa_parameters_file)
    global transformer
    transformer = Transformer(sa_parameters)

    pop = create_grid()

    sim_anneal = Simulated_Annealing(pop,temperature,min_temperature,cooling,max_iterations,distance_threshold)

    sim_anneal.anneal()

    sim_anneal.verbose(filename)

    eqpy.OUT_put("DONE")
    eqpy.OUT_put("{}\n{}\n{}\n{}".format(create_list_of_json_strings(sim_anneal.history), ';'.join(sim_anneal.history_scores),sim_anneal.start_time, sim_anneal.end_time))
