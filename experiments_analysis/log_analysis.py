#####################################################################################
#----------------------------Description--------------------------------------------#
# Analysis of the iterations.log file of an experiment                              #
#----------------------------Instructions-------------------------------------------#
#   1) Place the iterations.log file in the same directory with log_analysis.py     #
#   2) Define experiment_id on line 22                                              #
#   3) Define the clustering method on line 27                                      #
#   4) Run the python script                                                        #
#----------------------------Outputs------------------------------------------------#
# An experiment directory is created. Inside the experiment directory, a figure     #
#       directory containing all valuable figures is created. Moreover,             #
#       various infomative files are created in the experiment directory, such      #
#       as the sample files required for the seeded scenario of the second workflow.#
#####################################################################################


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import os
import sys
from pylab import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
import random
import csv
from csv import DictWriter
from analysis_utils import *

uncertain_file = 'uncertain.csv'
simulations_file = 'simulations.csv'
best_scores_file = 'best_evaluations.csv'
experiment_id = "birc"
clustering_method = "BIRCH"
working_dir = os.getcwd()
experiment_dir = os.path.join(working_dir,experiment_id)
figures_dir = os.path.join(experiment_dir,"figures")

make_dir(experiment_dir)
make_dir(figures_dir)

def run_analysis_from_log_file(filename):
    i=0
    it=0
    flag1 = False
    flag2 = False
    number_of_uncertain = []
    flag_temp = True
    flag_temp2 = False
    min_eval = 1
    total_selected_points = []
    total_evals = []
    uncertain = []
    simulations = []
    uncertain_file = 'uncertain.csv'
    simulations_file = 'simulations.csv'

    with open(filename,'r') as file:
        for line in file:

            if(i==0):
                initial_points = eval(line)
                print("Number of initial points is: {}".format(len(initial_points)))
                init_pop = len(initial_points)
            if(i==1):
                initial_evals = eval(line)
                print("Number of initial evaluations is: {}".format(len(initial_points)))
            if(i==2):
                initial_labels = eval(line)
                print("Number of initial labels is: {}".format(len(initial_labels)))
            if(i==3):
                init_points_not = eval(line)
                print("Number of initial points not simulated: {}".format(len(init_points_not)))
            if(i==4):
                initial_evals_not = eval(line)
                print("Number of evaluations of initial points not simulated: {}".format(len(initial_evals_not)))
            if(i==5):
                initial_points_new = eval(line)
                print("Number of initial points simulated: {}".format(len(initial_points_new)))
            if(i==6):
                initial_evals_new = eval(line)
                print("Number of evaluations of initial points simulated: {}".format(len(initial_evals_new)))
            if(i==7):
                grid = eval(line)
                print("Number of points in grid: {}".format(len(grid)))
            if(i==8):
                predictions = eval(line)
                print("Number of predictions: {}".format(len(predictions)))
                number_of_uncertain.append(count_uncertain(predictions))
                if(flag1==False):
                    plot_initial(figures_dir,initial_points,initial_evals,initial_labels,init_points_not,initial_evals_not,initial_points_new,initial_evals_new,grid,predictions)
                    flag1=True
                    print("-------- Iteration {} -----------".format(it))
            if(i==9):
                candidate_points = eval(line)
                print("Candidate_points: {}".format(len(candidate_points)))
                # create_candidates_file(predictions,grid,it,experiment_dir)
            if(i==10):
                labels_clust = eval(line)
                print("Length of clusters labels: {}".format(len(labels_clust)))
            if(i==11):
                if(flag2==False):
                    flag2=True
                selected_points_new_no_dist = eval(line)
                print("Selected points before distance: {}".format(len(selected_points_new_no_dist)))
                population = len(selected_points_new_no_dist)
            if(i==12):
                selected_points_new = eval(line)
                print("Selected points after distance: {}".format(len(selected_points_new)))
            if(i==13):
                selected_points_not = eval(line)
                print("Selected points evaluated from file: {}".format(len(selected_points_not)))
            if(i==14):
                points_already_selected_in_prev_iter = eval(line)
                print("Points already evaluated in previous iterations: {}".format(len(points_already_selected_in_prev_iter)))
            if(i==15):
                evals_new = eval(line)
                print("Number of evaluations via simulation: {}".format(len(evals_new)))
            if(i==16):
                evals_not = eval(line)
                print("Number of evaluations from file: {}".format(len(evals_not)))
            if(i==17):
                selected_points = eval(line)
                print("Number of total selected points: {}".format(len(selected_points)))
            if(i==18):
                evals = eval(line)
                print("Number of total evaluations: {}".format(len(evals)))
            if(i==19):
                # ind = np.argmin(evals)
                ind = np.where(np.asarray(evals) > 0, np.asarray(evals), np.inf).argmin()
                temp_min = evals[ind]
                if(min_eval>temp_min):
                    min_eval=temp_min
                    best_point = selected_points[ind]
                total_selected_points = total_selected_points + selected_points
                total_evals = total_evals + evals
                labels = eval(line)
                simulations.append(len(labels))
                print("Number of total labels: {}".format(len(labels)))
                create_plot(figures_dir,it,grid,predictions,selected_points,labels,selected_points_new_no_dist)
                # get_sample(total_evals,total_selected_points,os.path.join(experiment_dir,"interesting_12_50.txt"),12)
                it += 1
                print("-------- Iteration {} -----------".format(it))

                i=7
            i+=1

    plot_uncertain(figures_dir,number_of_uncertain,it)
    # get_sample(total_evals,total_selected_points,os.path.join(experiment_dir,"interesting_12_50.txt"),12)
    # get_best_point(best_point,os.path.join(experiment_dir,"best_point.txt"))
    update_uncertain_file(uncertain_file,clustering_method,number_of_uncertain)
    update_simulations_file(simulations_file,clustering_method,simulations)

run_analysis_from_log_file("iterations.log")
