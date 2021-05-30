#####################################################################################
#----------------------------Description--------------------------------------------#
# Utils file for the analysis of log files                                          #
#----------------------------Contents-----------------------------------------------#
# The functions defined below are:                                                  #
# -- make_dir : create directory                                                    #
# -- create_candidates_file : get the candidate points of each iteration            #
# -- get_sample : get the k most promising treatments                               #
# -- get_mixed_sample : get a sample containing k most promising treatments and     #
#                           j random treatments                                     #
# -- create_plot : plot the parameter space characterization                        #
# -- plot_initial : plot initial parameter space characterization and points se-    #
#                       lected for the initial training                             #
# -- plot_clustering : plot the result of the clustering algorithm                  #
# -- plot_uncertain : plot the number of uncertain points per iteration             #
# -- plot_simulations_file : plot total simulations and simulations per itera-      #
#                               tion per clustering Method                          #
# -- plot_uncertain_file : plot the number of uncertain points per iterations       #
# -- update_uncertain_file : update the csv file containing the number of uncer-    #
#                               tain points per iteration                           #
# -- update_simulations_file : update the csv file containing the number of sim-    #
#                               ulations per iteration                              #
# -- update_best_scores_file : update the csv file containing the best treatments   #
#                               evaluated per clustering method configuration       #
#-----------------------------------------------------------------------------------#
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
import pandas as pd
from collections import OrderedDict
#create directory
#paremters: path to new directory
def make_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory failed [{}]".format(path) )
    else:
        print ("Successfully created the directory [{}]".format(path))
    return

#create txt files with the candidate points of each iteration
#parameters: predictions, grid, number of iteration,experiment directory
def create_candidates_file(predictions,grid,it,experiment_dir):
    candidates_folder = os.path.join(experiment_dir,"candidates")
    make_dir(candidates_folder)
    uncertainties = [min(posterior_prob) for posterior_prob in predictions]
    uncertainty_threshold = 0.4
    max_indices = [i for i, u in enumerate(uncertainties) if u >= uncertainty_threshold]
    candidate_points = [grid[i] for i in max_indices]
    file1 = open(os.path.join(candidates_folder,'candidates{}.txt'.format(it)), "w+")
    file1.write(str(candidate_points))
    file1.close()
    return

#get sample to initialize the genetic algorithm population
#parameters: total evaluations, selected points, txt file to save the points, number of points required
def get_sample(total_evals,selected_points,filename,num_points):
    total_evals_arr = np.asarray(total_evals)
    idx = np.argpartition(total_evals_arr, num_points)

    final = []

    for index in idx[:num_points]:
        temp = []
        temp.append(selected_points[index][0])
        temp.append(selected_points[index][1])
        temp.append(selected_points[index][2])
        final.append(temp)

    file1 = open(filename, "w+")
    file1.write(str(final))
    file1.close()
    return

def get_mixed_sample(grid,predictions,filename,num_interesting,num_non_interesting):
    total_list = []
    total_list2 = []
    temp = []

    for h in range(len(grid)):
        temp = []

        if(predictions[h][1]>=0.5):
            for item in grid[h]:
                temp.append(item)
                total_list.append(temp)
        else:
            for item in grid[h]:
                temp.append(item)
                total_list2.append(temp)

    final1 = random.sample(total_list, num_interesting)
    final2 = random.sample(total_list2, num_non_interesting)
    final = final1 + final2
    file1 = open(filename, "w+")
    file1.write(str(final))
    file1.close()
    return

#plot the parameter space characterization
#parameters:
#it: number of iteration
#predictions: list of predictions
#selected_points: list of selected points
#labels: evaluation labels
#selected_points_new_no_dist: selected points after distance threshold
def create_plot(figures_dir,it,grid,predictions,selected_points,labels,selected_points_new_no_dist):
    temp_path = os.path.join(figures_dir,"iteration{}".format(it))
    make_dir(temp_path)

    interesting = []
    non_interesting = []

    for h in range(len(grid)):
        if(predictions[h][0]>=0.5):
            non_interesting.append(grid[h])
        else:
            interesting.append(grid[h])

    interesting_labels = []
    non_interesting_labels = []

    for h in range(len(selected_points)):
        if(labels[h]==1):
            interesting_labels.append(selected_points[h])
        else:
            non_interesting_labels.append(selected_points[h])

    selected_points_new_no_dist_arr = np.asarray(selected_points_new_no_dist)

    interesting_n = np.asarray(interesting)
    non_interesting_n = np.asarray(non_interesting)
    interesting_labels_n = np.asarray(interesting_labels)
    non_interesting_labels_n = np.asarray(non_interesting_labels)

    #viewing angle options
    azim = [-131,-53.25806451612897,-60.0]
    elev = [21,-149.38709677419342,69.9193548387097]

    fig = plt.figure(figsize=(15,12))
    ax1 = fig.add_subplot(121, projection='3d')

    ax1.set_xlim([0,30])
    ax1.set_ylim([0,1200])
    ax1.set_zlim([0,0.4])

    if interesting_labels_n.size:
        ax1.scatter(selected_points_new_no_dist_arr[:,1],selected_points_new_no_dist_arr[:,0],selected_points_new_no_dist_arr[:,2])

    ax1.invert_xaxis()
    ax1.set_ylabel("TNF Frequency")
    ax1.set_xlabel("TNF Duration'")
    ax1.set_zlabel("TNF Concentration")
    ax1.set_title("Selected points before distance threshold")
    ax1.set_box_aspect((1, 1, 1))

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_xlim([0,30])
    ax2.set_ylim([0,1200])
    ax2.set_zlim([0,0.4])
    if interesting_labels_n.size:
        ax2.scatter(interesting_labels_n[:,1],interesting_labels_n[:,0],interesting_labels_n[:,2],color='green',label='Interesting')
    if non_interesting_labels_n.size:
        ax2.scatter(non_interesting_labels_n[:,1],non_interesting_labels_n[:,0],non_interesting_labels_n[:,2],color='orange',label='Non Interesting')

    ax2.invert_xaxis()
    ax2.set_ylabel("TNF Frequency")
    ax2.set_xlabel("TNF Duration'")
    ax2.set_zlabel("TNF Concentration")
    ax2.set_title("Parameters Valuated via Simulation")
    ax2.legend()
    ax2.set_box_aspect((1, 1, 1))
    plt.savefig(os.path.join(temp_path,"selected_points_it_{}_fig.png".format(it)),bbox_inches = 'tight', pad_inches = 0)
    plt.close(fig)

    # plt.show()
    for i in range(4): #4 is the number of different desired views ( 1 default 3 custom )

        fig = plt.figure()

        #Set depthshade=false in order to disable opacity/shading

        #subplot for points clasified via simulation

        size = fig.get_size_inches()*fig.dpi
        #subplot for points clasified via the classifier
        ax2 = fig.add_subplot(111, projection='3d')
        ax2.set_ylim([5,30])
        ax2.set_xlim([10,1200])
        ax2.set_zlim([0.005,0.4])
        if interesting_n.size:
            ax2.scatter(interesting_n[:,0],interesting_n[:,1],interesting_n[:,2],color='blue',label='Interesting',alpha=0.05)
        ax2.set_ylabel("TNF DURATION",fontsize=12)
        ax2.set_xlabel("TNF FREQUENCY",fontsize=12)
        ax2.set_zlabel("TNF CONCETRATION",fontsize=12)  #Time_add_tnf
        ax2.set_box_aspect((1, 1, 1))
        if(i!=0):
            ax2.view_init(elev[i-1], azim[i-1])

        plt.savefig(os.path.join(temp_path,"it_{}_fig_view{}.pdf".format(it,i)),format="pdf",bbox_inches = 'tight', pad_inches = 0)  #format of filename: (number_of_variation)_(iteration)_(Number_of_view)
        plt.close(fig)
        i+=1

    return

#plot initial parameter space characterization
#parameters
#initial_points: initial points
#initial_evals: evaluations of initial points
#initial_labels: labels of initial evaluated points (1 for interesting, 0 for non insteresting)
#init_points_not: initial points evaluated
#initial_evals_not:
#initial_points_new:
#initial_evals_new:
#grid:
#predictions:

def plot_initial(figures_dir,initial_points,initial_evals,initial_labels,init_points_not,initial_evals_not,initial_points_new,initial_evals_new,grid,predictions):

    interesting_initials = []
    non_interesting_initials = []

    for h in range(len(initial_points)):
        if(initial_labels[h]==1):
            interesting_initials.append(initial_points[h])
        else:
            non_interesting_initials.append(initial_points[h])
    azim = -131
    elev = 21

    inital_points_n = np.asarray(initial_points)

    fig = plt.figure(figsize=(15,12))
    ax1 = fig.add_subplot(121, projection='3d')

    non_interesting_initials_n = np.asarray(non_interesting_initials)
    interesting_initials_n = np.asarray(interesting_initials)

    if non_interesting_initials_n.size:
        ax1.scatter(non_interesting_initials_n[:,0],non_interesting_initials_n[:,1],non_interesting_initials_n[:,2],color='red',label='Non Interesting')
    if interesting_initials_n.size:
        ax1.scatter(interesting_initials_n[:,0],interesting_initials_n[:,1],interesting_initials_n[:,2],color='blue',label='Interesting')

    ax1.set_xlabel('TNF Frequency')
    ax1.set_ylabel('TNF Duration')
    ax1.set_zlabel('TNF Concentration')
    ax1.legend()
    ax1.set_box_aspect((1, 1, 1))
    ax1.view_init(elev, azim)


    ax2 = fig.add_subplot(122, projection='3d')
    colors = cm.viridis(np.asarray(initial_evals)/max(initial_evals))

    colmap = cm.ScalarMappable(cmap=cm.viridis)
    colmap.set_array(initial_evals)

    yg = ax2.scatter(inital_points_n[:,0],inital_points_n[:,1],inital_points_n[:,2], c=colors,marker='o')
    cb = fig.colorbar(colmap)

    ax2.set_xlabel('TNF Frequency')
    ax2.set_ylabel('TNF Duration')
    ax2.set_zlabel('TNF Concentration')
    ax2.view_init(elev, azim)

    plt.suptitle('Initial Points')
    plt.savefig(os.path.join(figures_dir,'initial.png'),bbox_inches = 'tight', pad_inches = 0)
    plt.close(fig)
    interesting_initials_not = []
    non_interesting_initials_not = []

    for h in range(len(init_points_not)):
        if(initial_evals_not[h]<=0.3):
            interesting_initials_not.append(init_points_not[h])
        else:
            non_interesting_initials_not.append(init_points_not[h])


    init_points_not_n = np.asarray(init_points_not)

    fig2 = plt.figure(figsize=(15,12))
    ax12 = fig2.add_subplot(121, projection='3d')

    non_interesting_initials_not_n = np.asarray(non_interesting_initials_not)
    interesting_initials_not_n = np.asarray(interesting_initials_not)

    if non_interesting_initials_not_n.size:
        ax12.scatter(non_interesting_initials_not_n[:,0],non_interesting_initials_not_n[:,1],non_interesting_initials_not_n[:,2],color='red',label='Non Interesting')
    if interesting_initials_not_n.size:
        ax12.scatter(interesting_initials_not_n[:,0],interesting_initials_not_n[:,1],interesting_initials_not_n[:,2],color='blue',label='Interesting')

    ax12.set_xlabel('TNF Frequency')
    ax12.set_ylabel('TNF Duration')
    ax12.set_zlabel('TNF Concentration')
    ax12.legend()
    ax12.set_box_aspect((1, 1, 1))
    ax12.view_init(elev, azim)
    ax12.set_title('Points evaluted from file')
    interesting_initials_new = []
    non_interesting_initials_new = []

    for h in range(len(initial_points_new)):
        if(initial_evals_new[h]<=0.3):
            interesting_initials_new.append(initial_points_new[h])
        else:
            non_interesting_initials_new.append(initial_points_new[h])

    initial_points_new_n = np.asarray(initial_points_new)

    ax22 = fig2.add_subplot(122, projection='3d')

    non_interesting_initials_new_n = np.asarray(non_interesting_initials_new)
    interesting_initials_new_n = np.asarray(interesting_initials_new)

    if non_interesting_initials_new_n.size:
        ax22.scatter(non_interesting_initials_new_n[:,0],non_interesting_initials_new_n[:,1],non_interesting_initials_new_n[:,2],color='red',label='Non Interesting')
    if interesting_initials_new_n.size:
        ax22.scatter(interesting_initials_new_n[:,0],interesting_initials_new_n[:,1],interesting_initials_new_n[:,2],color='blue',label='Interesting')

    ax22.set_xlabel('TNF Frequency')
    ax22.set_ylabel('TNF Duration')
    ax22.set_zlabel('TNF Concentration')
    ax22.legend()
    ax22.set_box_aspect((1, 1, 1))
    ax22.view_init(elev, azim)
    ax22.set_title('Points evaluted via simulation')

    plt.suptitle('Initial Points')
    plt.savefig(os.path.join(figures_dir,"detailed.png"),bbox_inches = 'tight', pad_inches = 0)
    plt.close(fig)
    interesting = []
    non_interesting = []

    for h in range(len(grid)):
        if(predictions[h][0]>=0.5):
            non_interesting.append(grid[h])
        else:
            interesting.append(grid[h])

    interesting_n = np.asarray(interesting)
    non_interesting_n = np.asarray(non_interesting)
    #viewing angle options
    azim = [-130.79032258064518,-53.25806451612897,-60.0]
    elev = [30.354838709677438,-149.38709677419342,69.9193548387097]



    for i in range(4): #4 is the number of different desired views ( 1 default 3 custom )

        fig = plt.figure(figsize=(15,12))

        #subplot for points clasified via the classifier
        ax1 = fig.add_subplot(111, projection='3d')
        if interesting_n.size:
            ax1.scatter(interesting_n[:,1],interesting_n[:,0],interesting_n[:,2],color='blue',label='Interesting',alpha=0.05)

        ax1.set_xlim([5,30])
        ax1.set_ylim([10,1200])
        ax1.set_zlim([0.005,0.4])
        ax1.invert_xaxis()
        ax1.set_ylabel("TNF Frequency")
        ax1.set_xlabel("TNF Duration")
        ax1.set_zlabel("TNF Concentration")  #Time_add_tnf
        ax1.set_title("Parameters Valuated via Classifier")
        ax1.legend()
        ax1.set_box_aspect((1, 1, 1))
        if(i!=0):
            ax1.view_init(elev[i-1], azim[-1])
        plt.suptitle('First Classification', fontsize=16)
        plt.savefig(os.path.join(figures_dir,"pre_iter_classification_view{}".format(i)),bbox_inches = 'tight', pad_inches = 0)
        plt.close(fig)
    return

def plot_uncertain(figures_dir,number_of_uncertain,it):
    labels = [str(i) for i in range(it+1)]
    fig = plt.figure(figsize=(15,12))
    ax = fig.add_subplot(111)
    x = np.arange(it+1)
    ax.set_title("Points")
    ax.bar(x,number_of_uncertain)
    ax.set_ylabel('Number of points')
    ax.set_title('Number of points over uncertainty threshold per iteration')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel('Iteration')
    # plt.savefig("Uncertain_points.png")
    plt.savefig(os.path.join(figures_dir,"Uncertain_points.png"),bbox_inches = 'tight', pad_inches = 0)
    plt.close(fig)
    return

def count_uncertain(predictions):
    uncertainty = [min(prob) for prob in predictions]
    count = len([1 for i in uncertainty if i >=0.4])
    return count



# def plot_uncertain_file(figures_dir,filename):
#     with open(filename,'r',newline='') as csv_file:
#         for line in csv_file:
#             line_e = line.split(',')
#             cluster = line_e[0]
#             del line_e[0]
#             line_e = list(map(float, line_e))
#             iterations = [str(i) for i in range(1,len(line_e)+1)]
#             # line_e = line_e[:22]
#             # iterations = iterations[:22]
#             plt.plot(iterations,line_e,label=cluster)
#     plt.suptitle("Number of uncertain points per iteration")
#     plt.ylabel("Number of Points over uncertainty threshold")
#     plt.xlabel("Number of Iterations")
#     plt.legend()
#     plt.tight_layout()
#     # plt.show()
#     plt.savefig(os.path.join(figures_dir,"Uncertain_per_iter.png"),bbox_inches = 'tight', pad_inches = 0)
#
#     return

def plot_uncertain_file(figures_dir,filename):
    file = pd.read_csv(filename,header=None,index_col=False)
    file = file.iloc[:, : 21]
    file = file.groupby(0).agg([np.mean, np.std])
    std = file.iloc[:, 1::2]
    mean = file.iloc[:,::2]
    mean_list = mean.values.tolist()
    std_list = std.values.tolist()
    labels = file.index.tolist()

    fig, ax = plt.subplots()
    for i in range(len(mean_list)):
        mean_list_e = list(map(float, mean_list[i]))
        std_list_e = list(map(float, std_list[i]))
        iterations = [str(i) for i in range(1,len(mean_list_e)+1)]
        ax.errorbar(iterations, mean_list_e,yerr=std_list_e,fmt='-o',label=labels[i])
    plt.ylabel("Number of Points over uncertainty threshold",fontsize=12)
    plt.xlabel("Number of Iterations",fontsize=12)
    plt.legend()
    plt.savefig(os.path.join(figures_dir,"Uncertain_per_iter.png"),bbox_inches = 'tight', pad_inches = 0)
    plt.close(fig)
    return

# def plot_simulations_file(figures_dir,filename):
#
#     clusters = []
#     total_sims_list = []
#     with open(filename,'r',newline='') as csv_file:
#         for line in csv_file:
#             line_e = line.split(',')
#             cluster = line_e[0]
#             clusters.append(cluster)
#             del line_e[0]
#             line_e = list(map(float, line_e))
#             total_sims = sum(line_e)
#             total_sims_list.append(total_sims)
#
#     x = np.arange(len(clusters))
#     width = 0.35
#     fig, ax = plt.subplots()
#     ax.bar(x, total_sims_list, width)
#     ax.set_ylabel('Total Simulations')
#     ax.set_title('Total Simulations per Clustering Method')
#     ax.set_xticks(x)
#     ax.set_xticks(x)
#     ax.set_xticklabels(clusters)
#     fig.tight_layout()
#     plt.savefig(os.path.join(figures_dir,"Total_sims.png"),bbox_inches = 'tight', pad_inches = 0)
#
#     fig = plt.figure()
#     ax1 = fig.add_subplot(111)
#     with open(filename,'r',newline='') as csv_file:
#         for line in csv_file:
#             line_e = line.split(',')
#             cluster = line_e[0]
#             del line_e[0]
#             line_e = list(map(float, line_e))
#             iterations = [str(i) for i in range(1,len(line_e)+1)]
#             ax1.plot(iterations,line_e,label=cluster)
#         ax1.set_yscale('log')
#         plt.suptitle("Number of simulations per iteration")
#         plt.ylabel("Number of Simulations")
#         plt.xlabel("Number of Iterations")
#         box = ax.get_position()
#         # ax.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9])
#         # ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),fancybox=True, ncol=5)
#         ax1.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
#         # plt.legend(prop={'size': 7})
#         # plt.tight_layout()
#         # plt.show()
#         plt.savefig(os.path.join(figures_dir,"Sims_per_iter.png"),bbox_inches = 'tight', pad_inches = 0)
#
#     return

def plot_simulations_file(figures_dir,filename,final_sims_file):
    file = pd.read_csv(filename,header=None,index_col=False)
    file = file.iloc[:, : 21]
    file_list = file.values.tolist()
    total_sims_dict = OrderedDict()
    total_sims_dict["BIRCH"] = []
    total_sims_dict["DBSCAN"] = []
    total_sims_dict["KMEANS_20"] = []
    total_sims_dict["KMEANS_50"] = []
    total_sims_dict["KMEANS_500"] = []

    clusters = []
    for i in range(len(file_list)):
        _sum=0
        cluster = file_list[i][0]
        clusters.append(cluster)

        for j in range(1,len(file_list[i])):
            _sum+=file_list[i][j]
        total_sims_dict[cluster].append(_sum)

    clusters = list(set(clusters))

    file = file.groupby(0).agg([np.mean, np.std])
    std = file.iloc[:, 1::2]
    mean = file.iloc[:,::2]
    mean_list = mean.values.tolist()
    std_list = std.values.tolist()
    labels = file.index.tolist()

    fig, ax = plt.subplots()

    for i in range(len(mean_list)):
        mean_list_e = list(map(float, mean_list[i]))
        std_list_e = list(map(float, std_list[i]))
        iterations = [str(i) for i in range(1,len(mean_list_e)+1)]
        ax.errorbar(iterations, mean_list_e,yerr=std_list_e,fmt='-o',label=labels[i])
    ax.set_yscale('log')
    plt.ylabel("Number of Simulations",fontsize=12)
    plt.xlabel("Number of Iterations",fontsize=12)
    axbox = ax.get_position()
    ax.legend( bbox_to_anchor=(0.95,0.75), prop={'size': 9},borderaxespad=0.)
    # plt.show()
    plt.savefig(os.path.join(figures_dir,"Sims_per_iter.pdf"),format="pdf",bbox_inches = 'tight')

    final_sims_file = final_sims_file

    _max = [max(value) for key, value in total_sims_dict.items()  if value]
    _min = [min(value) for key, value in total_sims_dict.items()  if value]

    clusters = []
    total_sims_list = []
    with open(final_sims_file,'r',newline='') as csv_file:
        for line in csv_file:
            line_e = line.split(',')
            cluster = line_e[0]
            clusters.append(cluster)
            del line_e[0]
            line_e = list(map(float, line_e))
            total_sims = sum(line_e)
            total_sims_list.append(total_sims)

    x = np.arange(len(clusters))
    width = 0.35
    fig, ax = plt.subplots()
    yerr = [np.subtract(total_sims_list, _min), np.subtract(_max, total_sims_list)]
    ax.bar(x, total_sims_list, width,yerr=yerr,capsize=10)
    ax.set_ylabel('Total Simulations',fontsize=12)
    ax.set_xticks(x)
    ax.set_xticks(x)
    ax.set_xticklabels(clusters)
    ax.set_yscale('log')
    plt.savefig(os.path.join(figures_dir,"Total_sims.pdf"),format="pdf",bbox_inches = 'tight')
    # plt.show()
    return

def update_uncertain_file(filename,clustering_method,uncertain):

    with open(filename,'a',newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        row = [clustering_method] + uncertain
        csv_writer.writerow(row)


    return

def update_simulations_file(filename,clustering_method,simulations):

    with open(filename,'a',newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        row = [clustering_method] + simulations
        csv_writer.writerow(row)

    return

def get_final_sims_file(source_filename,dest_filename,iterations):

    sims_file = pd.read_csv(source_filename,header=None)
    sims_file = sims_file.iloc[:, : iterations]
    final_file = sims_file.groupby(0).mean()
    final_file.to_csv(dest_filename,header=False)

    return

def get_final_file(source_filename,dest_filename,iterations):

    file = pd.read_csv(source_filename,header=None)
    file = file.iloc[:, : iterations]
    final_file = file.groupby(0).mean()
    final_file.to_csv(dest_filename,header=False)

    return

def get_final_unc_file(source_filename,dest_filename):

    unc_file = pd.read_csv(source_filename,header=None)
    final_file = unc_file.groupby(0).mean()
    final_file.to_csv(dest_filename,header=False)

    return

def update_best_scores_file(filename,clustering_method,best_point,min_eval):

    headers = ["Estimators", "k1", "k2", "k3", "best_eval"]

    if(not os.path.exists(filename)):
        with open(filename,'a+') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(headers)
            csv_file.close()

    row = []
    row.append(clustering_method)
    row.append(best_point[0])
    row.append(best_point[1])
    row.append(best_point[2])
    row.append(min_eval)


    with open(filename,'a',newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(row)
        csv_file.close()

    return

def get_best_point(best_point,filename):

    file1 = open(filename, "w+")
    row = []
    row.append(best_point[0])
    row.append(best_point[1])
    row.append(best_point[2])
    file1.write(str(row))

    file1.close()
    return
