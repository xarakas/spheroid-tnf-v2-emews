import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd
import seaborn as sns
from mpl_toolkits.axes_grid1 import ImageGrid


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = "4"

sweep = pd.read_csv('./sweep_per_individual_results_3dist.csv',sep=',')


print("L1")
print(sweep[sweep['l1']==sweep['l1'].min()])
print("DTW")
print(sweep[sweep['DTW']==sweep['DTW'].min()])
print("Euclidean")
print(sweep[sweep['Eucl']==sweep['Eucl'].min()])

allk3 = sorted(sweep['k3'].unique())
allk4 = sorted(sweep['k4'].unique(), reverse=True)

# fig2, ax3 = plt.figure(0)



allplots = {}
allplotseu = {}
allplotsdtw = {}



fig, axn = plt.subplots(10, 10)#, sharex=True, sharey=True)
cbar_ax = fig.add_axes([.94, .3, .03, .4])
cbar_ax.set_title('L1', fontsize=8)
ii=0
cnt = 0
cnt2 = 0
#l 1
for k4 in allk4:
	for k3 in allk3:
		temp = sweep[sweep['k3']==k3]
		temp = temp[temp['k4']==k4]
		onlyrelevant = temp[['k1','k2','l1']]
		toplot = pd.DataFrame(columns = sorted(onlyrelevant['k1'].unique()), index= sorted(onlyrelevant['k2'].unique()) )
		for i in sorted(onlyrelevant['k1'].unique()):
			for j in sorted(onlyrelevant['k2'].unique()):
				toplot1=onlyrelevant[(onlyrelevant['k1']==i) & (onlyrelevant['k2']==j)]
				toplot.at[j,i] =toplot1['l1'].values[0]
		toplot = toplot.astype(float)
		allplots[ii] = toplot
		ii=ii+1
		# ax = plt.subplot2grid((10,10),(cnt,cnt2))
		cnt = cnt+1
		# print(cnt)
	cnt = 0
	cnt2 = cnt2+1


for i, ax in enumerate(axn.flat):
	if i==0:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(sweep['l1']), vmax=max(sweep['l1']), center=150, xticklabels=False, cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.set_title(allk3[0])
	elif i==9:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(sweep['l1']), vmax=max(sweep['l1']), center=150, yticklabels=False,  xticklabels=False,cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.set_title(allk3[-1])
		ax.text( 12, 3,round(allk4[0],5), fontsize = 4,rotation=270)
		# y2label
	elif i==90:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(sweep['l1']), vmax=max(sweep['l1']), center=150, cbar_ax=None if i else cbar_ax).invert_yaxis()
	elif i%10==0: 
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(sweep['l1']), vmax=max(sweep['l1']), center=150, xticklabels=False, cbar_ax=None if i else cbar_ax).invert_yaxis()
		if i==50:
			ax.text( -10, -7,'TNFR Endocytosis Rate', fontsize = 8, rotation=90)
	elif i<9:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(sweep['l1']), vmax=max(sweep['l1']), center=150, yticklabels=False,  xticklabels=False,cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.set_title(allk3[i])
		if i==3:
			ax.text( 11, 15,'TNFR Recycling Rate', fontsize = 8)

	elif i==19 or i==29 or i==39 or i==49 or i==59 or i==69 or i==79 or i==89:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(sweep['l1']), vmax=max(sweep['l1']), center=150, yticklabels=False,  xticklabels=False,cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.text( 12, 3,round(allk4[round(i/10)-1],5), fontsize = 4, rotation=270)
		if i==59:
			ax.text( 13.5, -3,'Cell Growth Rate', fontsize = 8, rotation=270)
	elif i==99:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(sweep['l1']), vmax=max(sweep['l1']), center=150, yticklabels=False, cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.text( 12, 3,round(allk4[9],5), fontsize = 4, rotation=270)
	elif i>=91 and i<99:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(sweep['l1']), vmax=max(sweep['l1']), center=150, yticklabels=False, cbar_ax=None if i else cbar_ax).invert_yaxis()
		if i==93:
			ax.text( 11, -10,'TNFR Binding Rate', fontsize = 8)
	else:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(sweep['l1']), vmax=max(sweep['l1']), center=150, yticklabels=False,  xticklabels=False,cbar_ax=None if i else cbar_ax).invert_yaxis()
		if i==55:
			ax.scatter(8.5, 3.5, marker='*', s=2, color='red')

plt.savefig('cal-sweep-l1-hm-matplotlib.pdf', format='pdf', dpi=320, bbox_inches='tight')


fig, axn = plt.subplots(2, 3)#, sharex=True, sharey=True)
cbar_ax = fig.add_axes([.94, .3, .03, .4])
cbar_ax.set_title('L1', fontsize=12)
ii=0
cnt = 0
cnt2 = 0
#l 1
allk3 = allk3[3:6]
allk4 = allk4[4:6]
for k4 in allk4:
	for k3 in allk3:
		temp = sweep[sweep['k3']==k3]
		temp = temp[temp['k4']==k4]
		onlyrelevant = temp[['k1','k2','l1']]
		toplot = pd.DataFrame(columns = sorted(onlyrelevant['k1'].unique()), index= sorted(onlyrelevant['k2'].unique()) )
		for i in sorted(onlyrelevant['k1'].unique()):
			for j in sorted(onlyrelevant['k2'].unique()):
				toplot1=onlyrelevant[(onlyrelevant['k1']==i) & (onlyrelevant['k2']==j)]
				toplot.at[j,i] =toplot1['l1'].values[0]
		toplot = toplot.astype(float)
		allplots[ii] = toplot
		ii=ii+1
		cnt = cnt+1
		

	cnt = 0
	cnt2 = cnt2+1


for i, ax in enumerate(axn.flat):
	if i==0:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(onlyrelevant['l1']), vmax=max(onlyrelevant['l1']),  yticklabels=2,xticklabels=False, cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.set_title(allk3[0], fontsize = 8)
		ax.tick_params(labelsize=8, label2On=False)
	elif i==2:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(onlyrelevant['l1']), vmax=max(onlyrelevant['l1']),  yticklabels=False,  xticklabels=False,cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.set_title(allk3[-1], fontsize = 8)
		ax.text( 10.5, 4.5,round(allk4[0],5), fontsize = 8,rotation=270)
		ax.tick_params(labelsize=8, label2On=False)
	elif i==3: 
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(onlyrelevant['l1']), vmax=max(onlyrelevant['l1']),  yticklabels=2,  xticklabels=2, cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.tick_params(labelsize=8, label2On=False)
	elif i<2:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(onlyrelevant['l1']), vmax=max(onlyrelevant['l1']),   yticklabels=False,  xticklabels=False,cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.set_title(allk3[i], fontsize = 8)
		ax.tick_params(labelsize=8, label2On=False)
	elif i==5:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(onlyrelevant['l1']), vmax=max(onlyrelevant['l1']) , yticklabels=False, xticklabels=2,cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.tick_params(labelsize=8, label2On=False)
		ax.text( 10.5, 4.5,round(allk4[1],5), fontsize = 8, rotation=270)
	elif i==4:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(onlyrelevant['l1']), vmax=max(onlyrelevant['l1']),   yticklabels=False, xticklabels=2, cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.tick_params(labelsize=8, label2On=False)
	else:
		sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(onlyrelevant['l1']), vmax=max(onlyrelevant['l1']),  yticklabels=False,  xticklabels=False,cbar_ax=None if i else cbar_ax).invert_yaxis()
		ax.tick_params(labelsize=8, label2On=False)
	if i==5:
		ax.scatter(8.5, 3.5, marker='*', s=10, color='red')
	elif i==2:
		ax.scatter(2.4, 1.5, marker='x', s=10, color='yellow')
		ax.scatter(2.4, 1.5, marker='.', s=10, color='green')
	elif i==3:
		ax.scatter(3.5, 1.5, marker='s', s=10, color='olive')

	

plt.savefig('3dzoomed.pdf', format='pdf', dpi=320, bbox_inches='tight')




