import threading
import random
import time
import math
import csv
import json
import sys
import pickle
import logging
import os

import numpy as np

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import eqpy, ga_utils

experiment_folder = os.getenv('TURBINE_OUTPUT')
checkpoint_file_input = os.getenv('CHECKPOINT_FILE')
termination_crit = os.getenv('TERMINATION_CRIT')
crossover_prob = float(os.getenv('CROSSOVER_PROB'))
mutation_prob = float(os.getenv('MUTATION_PROB'))
tournament_size = int(os.getenv('TOURNAMENT_SIZE'))
pop_num = int(os.getenv('POP_NUM'))
checkpoint_file = os.path.join(experiment_folder,"ga_checkpoint.pkl")
logging.basicConfig(format='%(message)s',filename=os.path.join(experiment_folder,"generations.log"),level=logging.DEBUG)
# list of ga_utils parameter objects
transformer = None

class Transformer:

    def __init__(self, ga_params, clf = None, scaler = None):
        self.ga_params = ga_params

    def mutate(self, population, indpb):
        """
        Mutates the values in list individual with probability indpb
        """
        # Note, if we had some aggregate constraint on the individual
        # (e.g. individual[1] * individual[2] < 10), we could copy
        # individual into a temporary list and mutate though until the
        # constraint was satisfied
        for i, param in enumerate(self.ga_params):
            individual = param.mutate(population[i], mu=0, indpb=indpb)          
            population[i] = individual

        return population,

    def cxUniform(self, ind1, ind2, indpb):
        for _ in range(100):
            c1, c2 = tools.cxUniform(ind1, ind2, indpb)

        return (c1, c2)

    def random_params(self):
        draws = []
        for p in self.ga_params:
            #draws.append(round(p.randomDraw(),2)) # if we wish to round, e.g. to 2 decimal digits
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
        
def printf(val):
    print(val)
    sys.stdout.flush()

# Not used
def obj_func(x):
    return 0

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

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

def queue_map(obj_func, pops):
    # Note that the obj_func is not used
    # sending data that looks like:
    # [[a,b,c,d],[e,f,g,h],...]
    if not pops:
        return []

    eqpy.OUT_put(create_list_of_json_strings(pops))
    result = eqpy.IN_get()
    split_result = result.split(';')
    # TODO determine if max'ing or min'ing and use -9999999 or 99999999
    return [(float(x),) if not math.isnan(float(x)) else (float(99999999),) for x in split_result]
    
    #return [(float(x),) for x in split_result]

def make_random_parameters():
    """
    Performs initial random draw on each parameter
    """
    return transformer.random_params()

# Returns a tuple of one individual
def custom_mutate(individual, indpb):
    """
    Mutates the values in list individual with probability indpb
    """
    return transformer.mutate(individual, indpb)
    # If we wish to round to, e.g. 2 decimal digits
    #mutated_ind = transformer.mutate(individual, indpb)
    #b = mutated_ind[0]
    #g1 = (round(b[0], 2),round(b[1], 2),round(b[2], 2))
    #ind1 = creator.Individual(g1)
    #ind1tuple = (ind1,)
    #return ind1tuple

def cxUniform(ind1, ind2, indpb):
    return transformer.cxUniform(ind1, ind2, indpb)

def timestamp(scores):
    return str(time.time())

def eaSimpleExtended(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__, checkpoint=None):
    visited_inds = {}
    # If previous sim has failed, or we want to continue from previous generation
    if checkpoint:
        # A file name has been given, then load the data from the file
        with open(checkpoint, "rb") as cp_file:
            cp = pickle.load(cp_file)
        population = cp["population"]
        #start_gen = cp["generation"]
        halloffame = cp["halloffame"]
        logbook = cp["logbook"]
        random.setstate(cp["rndstate"])
    else:
        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    # invalid_ind = [ind for ind in population if not ind.fitness.valid]
    invalid_ind = [ind for ind in population if (not ind.fitness.valid) and (not str(ind) in visited_inds)]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
        visited_inds[str(ind)] = fit

    if halloffame is not None:
        halloffame.update(population)
    gen_variance = []
    variance_log = []
    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        # printf("Logbookstream: {}\nhalloffame: {}\n".format(logbook.stream, halloffame))
        for p in population:
            logging.debug("0, {}, {}, {}".format(0, p, p.fitness))
    # for p in population:
    #     gen_variance.append(p.fitness.values)
    # variance_log.append(np.var(gen_variance))
    logging.info("Initial Generation fitness variance = {}".format(math.pow(float(logbook.select("std")[-1]),2)))
    # logging.debug("Stats: {}".format(stats))
    # logging.debug("Record: {}, length: {}".format(record, len(record)))
    logging.debug("Term crit type: {}".format(type(ngen)))
    if type(ngen)==int: # Run for ngens
        logging.debug("Following normal termination criterion process.")
        # Begin the generational process
        for gen in range(1, ngen + 1):
            # Select the next generation individuals
            offspring = toolbox.select(population, len(population))

            # Vary the pool of individuals
            offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)
            for ind in offspring:
                try:
                    ind.fitness.values = visited_inds[str(ind)]
                except KeyError:
                    pass
            # Evaluate the individuals with an invalid fitness
            # invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            invalid_ind = [ind for ind in offspring if (not ind.fitness.valid) and (not str(ind) in visited_inds)]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
                visited_inds[str(ind)] = fit

            # Update the hall of fame with the generated individuals
            if halloffame is not None:
                halloffame.update(offspring)

            # Replace the current population by the offspring
            population[:] = offspring

            # Append the current generation statistics to the logbook
            record = stats.compile(population) if stats else {}
            logbook.record(gen=gen, nevals=len(invalid_ind), **record)
            # Fill the dictionary using the dict(key=value[, ...]) constructor
            cp = dict(population=population, generation=gen, halloffame=halloffame,
                       logbook=logbook, rndstate=random.getstate())
            with open(checkpoint_file, "wb") as cp_file:
                pickle.dump(cp, cp_file)
            logging.info("Generation {} Stored at {}".format(gen, time.strftime("%H:%M:%S", time.localtime())))
            if verbose:
                printf("Logbookstream: {}\nhalloffame: {}\n".format(logbook.stream, halloffame))
                for p in population:
                    logging.debug("0, {}, {}, {}".format(gen, p, p.fitness))
                for h in halloffame:
                    logging.debug("-1, {}, {}, {}".format(gen, h, h.fitness))
    else: # Run while population fitness variance is less than limit for 5 consecutive generations
        # Begin the generational process
        counter = 0
        gen = 1
        while counter<5:
            logging.debug("Into while, counter = {}".format(counter))
            # gen_variance = []
            # Select the next generation individuals
            offspring = toolbox.select(population, len(population))

            # Vary the pool of individuals
            offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)
            for ind in offspring:
                try:
                    ind.fitness.values = visited_inds[str(ind)]
                except KeyError:
                    pass
            # Evaluate the individuals with an invalid fitness
            # invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            invalid_ind = [ind for ind in offspring if (not ind.fitness.valid) and (not str(ind) in visited_inds)]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
                visited_inds[str(ind)] = fit
            
            # Update the hall of fame with the generated individuals
            if halloffame is not None:
                halloffame.update(offspring)

            # Replace the current population by the offspring
            population[:] = offspring

            # Append the current generation statistics to the logbook
            record = stats.compile(population) if stats else {}
            logbook.record(gen=gen, nevals=len(invalid_ind), **record)
            # Fill the dictionary using the dict(key=value[, ...]) constructor
            cp = dict(population=population, generation=gen, halloffame=halloffame,
                       logbook=logbook, rndstate=random.getstate())
            with open(checkpoint_file, "wb") as cp_file:
                pickle.dump(cp, cp_file)
            logging.info("Generation {} Stored at {}".format(gen, time.strftime("%H:%M:%S", time.localtime())))
            if verbose:
                printf("Logbookstream: {}\nhalloffame: {}\n".format(logbook.stream, halloffame))
                for p in population:
                    logging.debug("0, {}, {}, {}".format(gen, p, p.fitness))
                for h in halloffame:
                    logging.debug("-1, {}, {}, {}".format(gen, h, h.fitness))
            # for p in population:
            #     gen_variance.append(p.fitness.values)
            # variance_log.append(np.var(gen_variance))
            # if abs(variance_log[-1]-variance_log[-2]) <= ngens:
            if math.pow(float(logbook.select("std")[-1]),2) <= ngen:
                counter = counter + 1
            else:
                counter = 0
            logging.debug("Generation fitness variance = {}, counter is now: {}".format(math.pow(float(logbook.select("std")[-1]),2), counter))
            gen = gen + 1

    logging.info("{}\n".format(logbook.stream))
    return population, logbook

def run():
    """
    :param num_iterations: number of generations
    :param seed: random seed
    :param ga parameters file name: ga parameters file name (e.g., "ga_params.json")
    :param num_population population of ga algorithm
    """
    eqpy.OUT_put("Params")
    parameters = eqpy.IN_get()
    # parse params
    # printf("Parameters: {}".format(parameters))
    # logging.info("Parameters: {}".format(parameters))
    (num_iterations, num_population, seed, ga_parameters_file) = eval('{}'.format(parameters))
    distance_type_id = os.getenv('DISTANCE_TYPE_ID')
    logging.info("No. of population: {}, Random seed: {}, GA parameters file: {}".format(pop_num, seed, ga_parameters_file))
    logging.info("Distance type - [{}]\t Termination criterion - [{}]\tCheckpoint file: {}\n".format(distance_type_id,termination_crit,checkpoint_file_input))
    logging.info("Begin at: {}".format(time.strftime("%H:%M:%S", time.localtime())))
    # num_iterations not used
    random.seed(seed)
    ga_parameters = ga_utils.create_parameters(ga_parameters_file)
    global transformer
    transformer = Transformer(ga_parameters)

    # deap class creators
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    # deap method definitions
    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual,
                     make_random_parameters)

    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", obj_func)
    toolbox.register("mate", cxUniform, indpb=crossover_prob)
    toolbox.register("mutate", custom_mutate, indpb=mutation_prob)
    toolbox.register("select", tools.selTournament, tournsize=tournament_size)
    toolbox.register("map", queue_map)

    pop = toolbox.population(n=pop_num)

    hof = tools.HallOfFame(pop_num)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    stats.register("ts", timestamp)

    start_time = time.time()
    pop, log = eaSimpleExtended(pop, toolbox, cxpb=crossover_prob, mutpb=mutation_prob, ngen=num(termination_crit), stats=stats, halloffame=hof, verbose=True, checkpoint=checkpoint_file_input)

    end_time = time.time()

    fitnesses = [str(p.fitness.values[0]) for p in pop]
    logging.info("Logbook: \n{}".format(log))
    logging.info("\n Hall of Fame: \n")
    logging.info("End at: {}".format(time.strftime("%H:%M:%S", time.localtime())))
    for h in hof:
        logging.debug("-1, {}, {}, {}".format(-1, h, h.fitness))

    eqpy.OUT_put("DONE")
    # return the final population
    eqpy.OUT_put("{}\n{}\n{}\n{}\n{}".format(create_list_of_json_strings(pop), ';'.join(fitnesses),
        start_time, log, end_time))

