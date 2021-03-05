import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = "20"

sweep = pd.read_csv('./sweep_log_drug_discovery.log',sep=',')
print("DD: Min from Sweep")
print(sweep[sweep['score']==sweep['score'].min()])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

pld = ax.scatter(sweep.k1, sweep.k2, sweep.k3, c=sweep.score, cmap="rainbow", alpha=0.5)#, vmin=0, vmax=45)
clb = fig.colorbar(pld, shrink=0.85)
ax.set_xlabel('TNF Frequency')
ax.set_ylabel('TNF Duration')
ax.set_zlabel('TNF Concentration')
clb.set_label('Alive Tumor Cells', rotation=90)

ax.xaxis.labelpad=15
ax.yaxis.labelpad=15
ax.zaxis.labelpad=15
ax.view_init(elev=20, azim=240)
# rcParams['axes.labelpad'] = 10

plt.savefig('DD-sweep-3D-matplotlib.pdf', format='pdf', dpi=320, bbox_inches='tight')
# plt.show()


sweep = pd.read_csv('./sweep_log_drug_discovery_filtered.log',sep=',')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

pld = ax.scatter(sweep.k1, sweep.k2, sweep.k3, c=sweep.score, cmap="rainbow", alpha=0.5)#, vmin=0, vmax=45)
clb = fig.colorbar(pld, shrink=0.85)
ax.set_xlabel('TNF Frequency')
ax.set_ylabel('TNF Duration')
ax.set_zlabel('TNF Concentration')
clb.set_label('Alive Tumor Cells', rotation=90)

ax.xaxis.labelpad=15
ax.yaxis.labelpad=15
ax.zaxis.labelpad=15
ax.view_init(elev=20, azim=240)
# rcParams['axes.labelpad'] = 10
# plt.title("Sweep")
# plt.figtext(0.5, 0.001,"Only points where no. of alive cells is reduced",horizontalalignment='center')
plt.savefig('DD-sweep-filtered-3D-matplotlib.pdf', format='pdf', dpi=320, bbox_inches='tight')
# plt.show()



data = pd.read_csv('./DD_GA/generations.csv',sep=',')

print("DD: Min from GA")
print(data[data['g']==data['g'].min()])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

pld = ax.scatter(data.x, data.y, data.z, c=data.g, cmap="rainbow", alpha=0.5, vmin=191, vmax=1150)
clb = fig.colorbar(pld, shrink=0.85)
ax.set_xlabel('TNF Frequency')
ax.set_ylabel('TNF Duration')
ax.set_zlabel('TNF Concentration')
clb.set_label('Alive Tumor Cells', rotation=90)

ax.xaxis.labelpad=15
ax.yaxis.labelpad=15
ax.zaxis.labelpad=15
ax.view_init(elev=20, azim=240)
# rcParams['axes.labelpad'] = 10

plt.savefig('DD-GA-3D-matplotlib.pdf', format='pdf', dpi=320, bbox_inches='tight')



data = pd.read_csv('./DD_GA/generations.csv',sep=',')
# eliminate -1 values to tackle runtime warnings
data.j=data.j+2

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

pld = ax.scatter(data.x, data.y, data.z, c=data.g, s=data.j, cmap="rainbow", alpha=0.5, vmin=191, vmax=1150)
clb = fig.colorbar(pld, shrink=0.85)
ax.set_xlabel('TNF Frequency')
ax.set_ylabel('TNF Duration')
ax.set_zlabel('TNF Concentration')
clb.set_label('Alive Tumor Cells', rotation=90)

ax.xaxis.labelpad=15
ax.yaxis.labelpad=15
ax.zaxis.labelpad=15
ax.view_init(elev=20, azim=240)
# plt.title("Genetic Algorithm")
# plt.figtext(0.5, 0.001,"Point size denotes generations",horizontalalignment='center')
# rcParams['axes.labelpad'] = 10

plt.savefig('DD-GA-3D-vol-matplotlib.pdf', format='pdf', dpi=320, bbox_inches='tight')

# plt.show()