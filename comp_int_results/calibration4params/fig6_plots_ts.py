import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = "24"

gs1 = pd.read_csv('./TNF_1_pulse150_cell_vs_time.csv',sep='\t')
gs2 = pd.read_csv('./TNF_2_pulse600_cell_vs_time.csv',sep='\t')
ga_dtw_gs1 = pd.read_csv('./dtw/instance_23_21_1_1time_course.tsv',sep='\t')
ga_dtw_gs2 = pd.read_csv('./dtw/instance_23_21_2_1time_course.tsv',sep='\t')
ga_l1_gs1 = pd.read_csv('./l1/instance_22_17_1_1time_course.tsv',sep='\t')
ga_l1_gs2 = pd.read_csv('./l1/instance_22_17_2_1time_course.tsv',sep='\t')
ga_euc_gs1 = pd.read_csv('./euclidean/instance_25_16_1_1time_course.tsv',sep='\t')
ga_euc_gs2 = pd.read_csv('./euclidean/instance_25_16_2_1time_course.tsv',sep='\t')
sweep_dtw_gs1 = pd.read_csv('./sweep/instance_8495_150/time_course.tsv',sep='\t')
sweep_dtw_gs2 = pd.read_csv('./sweep/instance_8495/time_course.tsv',sep='\t')
sweep_l1_gs1 = pd.read_csv('./sweep/instance_8355_150/time_course.tsv',sep='\t')
sweep_l1_gs2 = pd.read_csv('./sweep/instance_8355/time_course.tsv',sep='\t')
sweep_euc_gs1 = pd.read_csv('./sweep/instance_8355_150/time_course.tsv',sep='\t')
sweep_euc_gs2 = pd.read_csv('./sweep/instance_8355/time_course.tsv',sep='\t')

norm1 = max(gs1[:]['Alive'])
norm2 = max(gs2[:]['Alive'])


gs1norm = gs1[:][['Alive','Apoptotic','Necrotic']]/norm1
gs2norm = gs2[:][['Alive','Apoptotic','Necrotic']]/norm2
ga_dtw_gs1norm = ga_dtw_gs1[:][['alive','apoptotic','necrotic']]/norm1
ga_dtw_gs2norm = ga_dtw_gs2[:][['alive','apoptotic','necrotic']]/norm2
ga_l1_gs1norm = ga_l1_gs1[:][['alive','apoptotic','necrotic']]/norm1
ga_l1_gs2norm = ga_l1_gs2[:][['alive','apoptotic','necrotic']]/norm2
ga_euc_gs1norm = ga_euc_gs1[:][['alive','apoptotic','necrotic']]/norm1
ga_euc_gs2norm = ga_euc_gs2[:][['alive','apoptotic','necrotic']]/norm2
sweep_dtw_gs1norm = sweep_dtw_gs1[:][['alive','apoptotic','necrotic']]/norm1
sweep_dtw_gs2norm = sweep_dtw_gs2[:][['alive','apoptotic','necrotic']]/norm2
sweep_l1_gs1norm = sweep_l1_gs1[:][['alive','apoptotic','necrotic']]/norm1
sweep_l1_gs2norm = sweep_l1_gs2[:][['alive','apoptotic','necrotic']]/norm2
sweep_euc_gs1norm = sweep_euc_gs1[:][['alive','apoptotic','necrotic']]/norm1
sweep_euc_gs2norm= sweep_euc_gs2[:][['alive','apoptotic','necrotic']]/norm2



gs1_down = gs1norm.iloc[1::30,]
gs2_down = gs2norm.iloc[1::30,]


fig, ax = plt.subplots(figsize=(12,5))

line1, = ax.plot(ga_dtw_gs1.time[1:], gs1_down.Alive, linewidth=2, color="green")#, dashes=[6, 2])#label='GS1 Alive')
line2, = ax.plot(ga_dtw_gs1.time[1:], sweep_dtw_gs1norm.alive[1:], linewidth=2, dashes=[6, 2], marker='s', color="green")#label='GA DTW Alive')
line3, = ax.plot(ga_dtw_gs1.time[1:], sweep_l1_gs1norm.alive[1:], linewidth=2, dashes=[2, 2], marker='x', color="green")#label='GA $L_1$ Alive')
line4, = ax.plot(ga_dtw_gs1.time[1:], sweep_euc_gs1norm.alive[1:], linewidth=2, dashes=[6, 6], marker='.', color="green")#label='GA Euclidean Alive')
line5, = ax.plot(ga_dtw_gs1.time[1:], gs1_down.Apoptotic, linewidth=2, color="red")#, dashes=[6, 2])#label='GS1 Alive')
line6, = ax.plot(ga_dtw_gs1.time[1:], sweep_dtw_gs1norm.apoptotic[1:], linewidth=2, dashes=[6, 2], marker='s', color="red")#label='GA DTW Alive')
line7, = ax.plot(ga_dtw_gs1.time[1:], sweep_l1_gs1norm.apoptotic[1:], linewidth=2, dashes=[2, 2], marker='x', color="red")#label='GA $L_1$ Alive')
line8, = ax.plot(ga_dtw_gs1.time[1:], sweep_euc_gs1norm.apoptotic[1:], linewidth=2, dashes=[6, 6], marker='.', color="red")#label='GA Euclidean Alive')
line9, = ax.plot(ga_dtw_gs1.time[1:], gs1_down.Necrotic, linewidth=2, color="black")#, dashes=[6, 2])#label='GS1 Alive')
line10, = ax.plot(ga_dtw_gs1.time[1:], sweep_dtw_gs1norm.necrotic[1:], linewidth=2, dashes=[6, 2], marker='s', color="black")#label='GA DTW Alive')
line11, = ax.plot(ga_dtw_gs1.time[1:], sweep_l1_gs1norm.necrotic[1:], linewidth=2, dashes=[2, 2], marker='x', color="black")#label='GA $L_1$ Alive')
line12, = ax.plot(ga_dtw_gs1.time[1:], sweep_euc_gs1norm.necrotic[1:], linewidth=2, dashes=[6, 6], marker='.', color="black")#label='GA Euclidean Alive')


plt.xlabel("Time (minutes)")
plt.ylabel("Normalized No. of Cells")
plt.savefig('fig6a-matplotlib.pdf', format='pdf', bbox_inches='tight')
# plt.show()



fig, ax = plt.subplots(figsize=(12,5))

line1, = ax.plot(ga_dtw_gs1.time[1:], gs2_down.Alive, linewidth=2, color="green")#, dashes=[6, 2])#label='GS1 Alive')
line2, = ax.plot(ga_dtw_gs1.time[1:], sweep_dtw_gs2norm.alive[1:], linewidth=2, dashes=[6, 2], marker='s', color="green")#label='GA DTW Alive')
line3, = ax.plot(ga_dtw_gs1.time[1:], sweep_l1_gs2norm.alive[1:], linewidth=2, dashes=[2, 2], marker='x', color="green")#label='GA $L_1$ Alive')
line4, = ax.plot(ga_dtw_gs1.time[1:], sweep_euc_gs2norm.alive[1:], linewidth=2, dashes=[6, 6], marker='.', color="green")#label='GA Euclidean Alive')
line5, = ax.plot(ga_dtw_gs1.time[1:], gs2_down.Apoptotic, linewidth=2, color="red")#, dashes=[6, 2])#label='GS1 Alive')
line6, = ax.plot(ga_dtw_gs1.time[1:], sweep_dtw_gs2norm.apoptotic[1:], linewidth=2, dashes=[6, 2], marker='s', color="red")#label='GA DTW Alive')
line7, = ax.plot(ga_dtw_gs1.time[1:], sweep_l1_gs2norm.apoptotic[1:], linewidth=2, dashes=[2, 2], marker='x', color="red")#label='GA $L_1$ Alive')
line8, = ax.plot(ga_dtw_gs1.time[1:], sweep_euc_gs2norm.apoptotic[1:], linewidth=2, dashes=[6, 6], marker='.', color="red")#label='GA Euclidean Alive')
line9, = ax.plot(ga_dtw_gs1.time[1:], gs2_down.Necrotic, linewidth=2, color="black")#, dashes=[6, 2])#label='GS1 Alive')
line10, = ax.plot(ga_dtw_gs1.time[1:], sweep_dtw_gs2norm.necrotic[1:], linewidth=2, dashes=[6, 2], marker='s', color="black")#label='GA DTW Alive')
line11, = ax.plot(ga_dtw_gs1.time[1:], sweep_l1_gs2norm.necrotic[1:], linewidth=2, dashes=[2, 2], marker='x', color="black")#label='GA $L_1$ Alive')
line12, = ax.plot(ga_dtw_gs1.time[1:], sweep_euc_gs2norm.necrotic[1:], linewidth=2, dashes=[6, 6], marker='.', color="black")#label='GA Euclidean Alive')


plt.xlabel("Time (minutes)")
plt.ylabel("Normalized No. of Cells")

plt.savefig('fig6b-matplotlib.pdf', format='pdf', bbox_inches='tight')
# plt.show()





fig, ax = plt.subplots(figsize=(12,5))

line1, = ax.plot(ga_dtw_gs1.time[1:], gs1_down.Alive, linewidth=2, color="green")#, dashes=[6, 2])#label='GS1 Alive')
line2, = ax.plot(ga_dtw_gs1.time[1:], ga_dtw_gs1norm.alive[1:], linewidth=2, dashes=[6, 2], marker='s', color="green")#label='GA DTW Alive')
line3, = ax.plot(ga_dtw_gs1.time[1:], ga_l1_gs1norm.alive[1:], linewidth=2, dashes=[2, 2], marker='x', color="green")#label='GA $L_1$ Alive')
line4, = ax.plot(ga_dtw_gs1.time[1:], ga_euc_gs1norm.alive[1:], linewidth=2, dashes=[6, 6], marker='.', color="green")#label='GA Euclidean Alive')
line5, = ax.plot(ga_dtw_gs1.time[1:], gs1_down.Apoptotic, linewidth=2, color="red")#, dashes=[6, 2])#label='GS1 Alive')
line6, = ax.plot(ga_dtw_gs1.time[1:], ga_dtw_gs1norm.apoptotic[1:], linewidth=2, dashes=[6, 2], marker='s', color="red")#label='GA DTW Alive')
line7, = ax.plot(ga_dtw_gs1.time[1:], ga_l1_gs1norm.apoptotic[1:], linewidth=2, dashes=[2, 2], marker='x', color="red")#label='GA $L_1$ Alive')
line8, = ax.plot(ga_dtw_gs1.time[1:], ga_euc_gs1norm.apoptotic[1:], linewidth=2, dashes=[6, 6], marker='.', color="red")#label='GA Euclidean Alive')
line9, = ax.plot(ga_dtw_gs1.time[1:], gs1_down.Necrotic, linewidth=2, color="black")#, dashes=[6, 2])#label='GS1 Alive')
line10, = ax.plot(ga_dtw_gs1.time[1:], ga_dtw_gs1norm.necrotic[1:], linewidth=2, dashes=[6, 2], marker='s', color="black")#label='GA DTW Alive')
line11, = ax.plot(ga_dtw_gs1.time[1:], ga_l1_gs1norm.necrotic[1:], linewidth=2, dashes=[2, 2], marker='x', color="black")#label='GA $L_1$ Alive')
line12, = ax.plot(ga_dtw_gs1.time[1:], ga_euc_gs1norm.necrotic[1:], linewidth=2, dashes=[6, 6], marker='.', color="black")#label='GA Euclidean Alive')


plt.xlabel("Time (minutes)")
plt.ylabel("Normalized No. of Cells")
plt.savefig('fig6c-matplotlib.pdf', format='pdf', bbox_inches='tight')
# plt.show()






fig, ax = plt.subplots(figsize=(12,5))

line1, = ax.plot(ga_dtw_gs1.time[1:], gs2_down.Alive, linewidth=2, color="green")#, dashes=[6, 2])#label='GS1 Alive')
line2, = ax.plot(ga_dtw_gs1.time[1:], ga_dtw_gs2norm.alive[1:], linewidth=2, dashes=[6, 2], marker='s', color="green")#label='GA DTW Alive')
line3, = ax.plot(ga_dtw_gs1.time[1:], ga_l1_gs2norm.alive[1:], linewidth=2, dashes=[2, 2], marker='x', color="green")#label='GA $L_1$ Alive')
line4, = ax.plot(ga_dtw_gs1.time[1:], ga_euc_gs2norm.alive[1:], linewidth=2, dashes=[6, 6], marker='.', color="green")#label='GA Euclidean Alive')
line5, = ax.plot(ga_dtw_gs1.time[1:], gs2_down.Apoptotic, linewidth=2, color="red")#, dashes=[6, 2])#label='GS1 Alive')
line6, = ax.plot(ga_dtw_gs1.time[1:], ga_dtw_gs2norm.apoptotic[1:], linewidth=2, dashes=[6, 2], marker='s', color="red")#label='GA DTW Alive')
line7, = ax.plot(ga_dtw_gs1.time[1:], ga_l1_gs2norm.apoptotic[1:], linewidth=2, dashes=[2, 2], marker='x', color="red")#label='GA $L_1$ Alive')
line8, = ax.plot(ga_dtw_gs1.time[1:], ga_euc_gs2norm.apoptotic[1:], linewidth=2, dashes=[6, 6], marker='.', color="red")#label='GA Euclidean Alive')
line9, = ax.plot(ga_dtw_gs1.time[1:], gs2_down.Necrotic, linewidth=2, color="black")#, dashes=[6, 2])#label='GS1 Alive')
line10, = ax.plot(ga_dtw_gs1.time[1:], ga_dtw_gs2norm.necrotic[1:], linewidth=2, dashes=[6, 2], marker='s', color="black")#label='GA DTW Alive')
line11, = ax.plot(ga_dtw_gs1.time[1:], ga_l1_gs2norm.necrotic[1:], linewidth=2, dashes=[2, 2], marker='x', color="black")#label='GA $L_1$ Alive')
line12, = ax.plot(ga_dtw_gs1.time[1:], ga_euc_gs2norm.necrotic[1:], linewidth=2, dashes=[6, 6], marker='.', color="black")#label='GA Euclidean Alive')


plt.xlabel("Time (minutes)")
plt.ylabel("Normalized No. of Cells")
# ax.legend()
plt.savefig('fig6d-matplotlib.pdf', format='pdf', bbox_inches='tight')
# plt.show()




