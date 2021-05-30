#####################################################################################
#----------------------------Description--------------------------------------------#
# Analysis of the log file of the sweep search                                      #
#----------------------------Instructions-------------------------------------------#
#  Place the log file of the sweep in the same directory with log_space.py          #
#----------------------------Contents-----------------------------------------------#
# --plot_space : plot the total results of the sweep search or plot points under    #
#                    threshold                                                      #
# --remove_outliers : remove point under threshold                                  #
# --print_outliers : print points under threshold                                   #
# --print_stats : print number of points under threshold                            #
# --print_test : test function/ util / not used                                     #
#----------------------------Outputs------------------------------------------------#
# Plots for the sweep search saved in current directory, stats printed in command   #
#       line                                                                        #
#####################################################################################

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *

#log file columns: id,k1,k2,k3,final alive tumour cells,initital alive tumour cells

id = []
k1 = []
k2 = []
k3 = []
score = []
score_init = []
label = []
percentage = []
k1_new = []
k2_new = []
k3_new = []
percentage_new = []

def plot_space(threshold):

    azim = -131
    elev = 21

    if(threshold==-1):
        #no threshold
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        colors = cm.hsv(np.asarray(percentage)/max(percentage))

        colmap = cm.ScalarMappable(cmap=cm.hsv)
        colmap.set_array(percentage)

        yg = ax.scatter(k1,k2,k3, c=colors,marker='o')
        cb = fig.colorbar(colmap)

        ax.set_xlabel('TIME ADD TNF')
        ax.set_ylabel('DURATION ADD TNF')
        ax.set_zlabel('CONCETRATION TNF')
        ax.view_init(elev, azim)
        plt.suptitle('Parameter Space after sweep search')
        plt.title('No threshold')
        plt.savefig('sweep_fig.png')

    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        colors = cm.hsv(np.asarray(percentage_new)/max(percentage_new))

        colmap = cm.ScalarMappable(cmap=cm.hsv)
        colmap.set_array(percentage_new)

        yg = ax.scatter(k1_new,k2_new,k3_new, color='blue',marker='o')

        ax.set_xlabel('TNF FREQUENCY',fontsize=12)
        ax.set_ylabel('TNF DURATION',fontsize=12)
        ax.set_zlabel('TNF CONCETRATION',fontsize=12)
        ax.set_xlim3d(10,1200)
        ax.set_ylim3d(5,30)
        ax.set_zlim3d(0.005,0.4)
        ax.view_init(elev, azim)
        ax.set_box_aspect((1, 1, 1))
        plt.savefig('sweep_fig_thresh{}.pdf'.format(int(round(threshold,2)*100)),format="pdf",bbox_inches = 'tight', pad_inches = 0)


    return

def remove_outliers(threshold):

    for i in range(len(percentage)):
        if(percentage[i]<threshold):
            k1_new.append(k1[i])
            k2_new.append(k2[i])
            k3_new.append(k3[i])
            percentage_new.append(percentage[i])

    return

def reset_news():

    k1_new.clear()
    k2_new.clear()
    k3_new.clear()
    percentage_new.clear()

    return


def print_outliers(threshold):
    for i in range(len(id)):
        if(percentage[i]>threshold):
            print(i)
            print(k1[i])
            print(k2[i])
            print(k3[i])
            print(percentage[i])
            print('------------------------------------')
    return

def print_stats(threshold):
    population = 0
    for i in range(len(id)):
        if(percentage[i]<threshold):
            population+=1

    print("Points with final score less than {} %: {}".format(round(threshold,2)*100,population))
    print('-------------------------------------------------')
    return

def print_points_under_thresh(threshold):

    for i in range(len(id)):
        if(percentage[i]<threshold):
            print(k1[i])
            print(k2[i])
            print(k3[i])
            print('-------------------------------------------------')

    return

def print_test(keyword):
    if(keyword=='len'):
        print(len(id))
        print(len(k1))
        print(len(k2))
        print(len(k3))
        print(len(score))
        print(len(score_init))

    if(keyword=='per'):
        print(percentage)

    if(keyword=='lab'):
        print(label)

    return

def main(filename):
    threshold1 = 1
    threshold2 = 0.5

    with open(filename,'r') as file:
        next(file)
        for line in file:
            sline = line.split(',')
            id.append(eval(sline[0]))
            k1.append(eval(sline[1]))
            k2.append(eval(sline[2]))
            k3.append(eval(sline[3]))
            score.append(eval(sline[4]))
            score_init.append(eval(sline[5]))

    for i in range(len(id)):

        if((1.0*score[i]/score_init[i])>0.25):
            label.append(0)
        else:
            label.append(1)

        percentage.append(1.0*score[i]/score_init[i])




    print()
    print('-------------------------------------------------')
    print("Initial population of points: {} ".format(len(id)))
    print('-------------------------------------------------')

    for i in range(8):
        remove_outliers(threshold1-i*0.1)
        plot_space(threshold1-i*0.1)
        reset_news()
        print_stats(threshold1-i*0.1)
    print_stats(0.25)
    print_stats(0.2)

    return


main('sweep_log_drug_discovery.log')
