import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd
import seaborn as sns


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = "4"

sweep = pd.read_csv('./sweep_per_individual_results_3dist.csv',sep=',')


allk3 = sorted(sweep['k3'].unique())
allk4 = sorted(sweep['k4'].unique())

plt.figure(0)
cnt = 0
cnt2 = 0
for k4 in allk4:
	for k3 in allk3:
		temp = sweep[sweep['k3']==k3]
		temp = temp[temp['k4']==k4]
		onlyrelevant = temp[['k1','k2','l1']]
		toplot = pd.DataFrame(columns = sorted(onlyrelevant['k1'].unique()), index= sorted(onlyrelevant['k2'].unique()) )
		for i in sorted(onlyrelevant['k1'].unique()):
			for j in sorted(onlyrelevant['k2'].unique()):
				toplot1=onlyrelevant[(onlyrelevant['k1']==i) & (onlyrelevant['k2']==j)]
				toplot.at[i,j] =toplot1['l1'].values[0]
		toplot = toplot.astype(float)
		ax = plt.subplot2grid((10,10),(cnt,cnt2))
		sns.heatmap(toplot, vmin =min(sweep['l1']) , vmax = max(sweep['l1'])).invert_yaxis()
		# sns.heatmap(toplot).invert_yaxis()
		cnt = cnt+1
		# print(cnt)
	cnt = 0
	cnt2 = cnt2+1

plt.show()


