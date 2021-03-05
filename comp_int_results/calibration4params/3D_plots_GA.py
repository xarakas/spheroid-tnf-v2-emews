import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = "20"



data = pd.read_csv('./euclidean/generations.csv',sep=',')
data1 = pd.read_csv('./dtw/generations.csv',sep=',')
data2 = pd.read_csv('./l1/generations.csv',sep=',')
sweep = pd.read_csv('./sweep/sweep_per_individual_results_3dist.csv',sep=',')

GAtemp = data2[(data2['g']<=0.0015) & (data2['g']>=0.0009)]
sweeptemp = sweep[sweep['k4']==0.0013666666666666699]

GAtemp = GAtemp[GAtemp['j']!=-1]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



pld = ax.scatter(GAtemp.x, GAtemp.y, GAtemp.z, c=GAtemp.f, s=GAtemp.j,cmap="rainbow", alpha=0.5, vmin=sweeptemp[sweeptemp['l1']==sweeptemp['l1']].min()['l1'], vmax=sweeptemp[sweeptemp['l1']==sweeptemp['l1']].max()['l1'])
clb = fig.colorbar(pld, shrink=0.85)
ax.set_xlabel('Binding rate')
ax.set_ylabel('Endocytosis rate')
ax.set_zlabel('Recycling rate')
clb.set_label('L1', rotation=90)

ax.set_xlim((-0.05,1.05))
ax.set_ylim((-0.05,1.05))
ax.set_zlim((-0.05,1.05))
ax.xaxis.labelpad=15
ax.yaxis.labelpad=15
ax.zaxis.labelpad=15
ax.view_init(elev=20, azim=240)

plt.savefig('fig10GAa-matplotlib.pdf', format='pdf', dpi=320, bbox_inches='tight')


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

pld = ax.scatter(sweeptemp.k1, sweeptemp.k2, sweeptemp.k3, c=sweeptemp.l1, cmap="rainbow", alpha=0.5)#, vmin=0, vmax=45)
clb = fig.colorbar(pld, shrink=0.85)
ax.set_xlabel('Binding rate')
ax.set_ylabel('Endocytosis rate')
ax.set_zlabel('Recycling rate')
clb.set_label('L1', rotation=90)

ax.xaxis.labelpad=15
ax.yaxis.labelpad=15
ax.zaxis.labelpad=15
ax.view_init(elev=20, azim=240)

plt.savefig('fig10Sweepa-matplotlib.pdf', format='pdf', dpi=320, bbox_inches='tight')




onlybest_a = data.iloc[80::80,6]
onlybest_b = data1.iloc[80::80,6]
onlybest_c = data2.iloc[80::80,6]

norm = max(onlybest_a)
norm1 = max(onlybest_b)
norm2 = max(onlybest_c)


onlybest_a = onlybest_a/norm
onlybest_b = onlybest_b/norm1
onlybest_c = onlybest_c/norm2



fig, ax = plt.subplots(figsize=(12,5))
x = range(1,31)
line1, = ax.plot(x, onlybest_a, linewidth=2, color="black", label='Euclidean')
line2, = ax.plot(x, onlybest_b, linewidth=2, dashes=[6, 2], marker='s', color="black", label='DTW')
line3, = ax.plot(x, onlybest_c, linewidth=2, dashes=[2, 2], marker='x', color="black", label='$L_1$')
plt.xlabel("Generations")
plt.ylabel("Normalized Fitness Scores")
ax.legend()
plt.savefig('fig8-normalized-matplotlib.pdf', format='pdf', bbox_inches='tight')


fig, ax = plt.subplots(figsize=(12,5))
x = range(1,31)
line1, = ax.plot(x, data.iloc[80::80,6], linewidth=2, color="black", label='Euclidean')
line2, = ax.plot(x, data1.iloc[80::80,6], linewidth=2, dashes=[6, 2], marker='s', color="black", label='DTW')
line3, = ax.plot(x, data2.iloc[80::80,6], linewidth=2, dashes=[2, 2], marker='x', color="black", label='$L_1$')
plt.xlabel("Generations")
plt.ylabel("Fitness Scores")
ax.legend()
plt.savefig('fig8-matplotlib.pdf', format='pdf', bbox_inches='tight')
