import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd
import seaborn as sns
from mpl_toolkits.axes_grid1 import ImageGrid


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = "4"

GA1 = pd.read_csv('./l1/generations.csv',sep=',')
sweep = pd.read_csv('./sweep/sweep_per_individual_results_3dist.csv',sep=',')


GA1 = GA1[GA1['j']!=-1]
GA2 = GA1.iloc[:,2:7]

print("L1")
print(GA2[GA2['f']==GA2['f'].min()])

GA=GA2.drop_duplicates()
print(len(GA))

allk1 = sorted(GA['x'].unique())
allk2 = sorted(GA['y'].unique())
allk3 = sorted(GA['z'].unique())
allk4 = sorted(GA['g'].unique(), reverse=True)

rangek1=sorted(sweep['k1'].unique())
rangek2=sorted(sweep['k2'].unique())
rangek3=sorted(sweep['k3'].unique())
rangek4=sorted(sweep['k4'].unique(), reverse=True)

print(rangek4)
print(rangek3)
print(len(rangek3))


fig, axn = plt.subplots(9, 9)#, sharex=True, sharey=True)
cbar_ax = fig.add_axes([.96, .3, .03, .4])
cbar_ax.set_title('L1', fontsize=8)
allplots = {}
ii=0

for ik4 in range(1, len(rangek4)):
    for ik3 in range(1, len(rangek3)):
        temp4 = GA[(GA['g']>rangek4[ik4]) & (GA['g']<=rangek4[ik4-1])]
        temp3 = temp4[(temp4['z']<rangek3[ik3]) & (temp4['z']>=rangek3[ik3-1])]
        onlyrelevant = temp3[['x','y','f']]
        toplot = pd.DataFrame(1500, columns = rangek1, index= rangek2)
        for i in range(1, len(rangek1)):
            for j in range(1, len(rangek2)):
                try:
                    toplot1=onlyrelevant[(onlyrelevant['x']<rangek1[i]) & (onlyrelevant['x']>=rangek1[i-1]) & (onlyrelevant['y']<rangek2[j]) & (onlyrelevant['y']>=rangek2[j-1])]
                    toplot.at[rangek2[j],rangek1[i]] =toplot1['f'].values[0]
                except IndexError:
                    continue
        toplot = toplot.astype(float)
        allplots[ii] = toplot
        ii=ii+1



for i, ax in enumerate(axn.flat):
    if i==0:
        sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(GA['f']), vmax=max(GA['f']), center=150, xticklabels=False, cbar_ax=None if i else cbar_ax).invert_yaxis()
        ti = str(round(rangek3[0],3))+"-"+str(round(rangek3[1],3))
        ax.set_title(ti)
    elif i==8:
        sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(GA['f']), vmax=max(GA['f']), center=150, yticklabels=False,  xticklabels=False,cbar_ax=None if i else cbar_ax).invert_yaxis()
        ti = str(round(rangek3[-2],3))+"-"+str(round(rangek3[-1],3))
        ax.set_title(ti)
        ti2 = str(round(rangek4[0],5))+"-"+str(round(rangek4[1],5))
        ax.text( 12, 0.5, ti2, fontsize = 4,rotation=270)
    elif i==72:
        sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(GA['f']), vmax=max(GA['f']), center=150, cbar_ax=None if i else cbar_ax).invert_yaxis()
    elif i==9 or i==18 or i==27 or i==36 or i==45 or i==54 or i==63: 
        sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(GA['f']), vmax=max(GA['f']), center=150, xticklabels=False, cbar_ax=None if i else cbar_ax).invert_yaxis()
        if i==36:
            ax.text( -10, -10,'TNFR Endocytosis Rate', fontsize = 8, rotation=90)
    elif i<8:
        sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(GA['f']), vmax=max(GA['f']), center=150, yticklabels=False,  xticklabels=False,cbar_ax=None if i else cbar_ax).invert_yaxis()
        ti = str(round(rangek3[i],3))+"-"+str(round(rangek3[i+1],3))
        ax.set_title(ti)
        if i==3:
            ax.text( 8, 15,'TNFR Recycling Rate', fontsize = 8)

    elif i==17 or i==26 or i==35 or i==44 or i==53 or i==62 or i==71:
        sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(GA['f']), vmax=max(GA['f']), center=150, yticklabels=False,  xticklabels=False,cbar_ax=None if i else cbar_ax).invert_yaxis()
        ti2 = str(round(rangek4[round(i/9)-1],5))+"-"+str(round(rangek4[round(i/9)],5))
        ax.text( 12, 0.5,ti2, fontsize = 3.75, rotation=270)
        if i==44:
            ax.text( 13.5, -3,'Cell Growth Rate', fontsize = 8, rotation=270)
    elif i==80:
        sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(GA['f']), vmax=max(GA['f']), center=150, yticklabels=False, cbar_ax=None if i else cbar_ax).invert_yaxis()
        ti = str(round(rangek4[8],5))+"-"+str(round(rangek4[9],5))
        ax.text( 12, 0.5,ti, fontsize = 3.75, rotation=270)
    elif i>=73 and i<80:
        sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(GA['f']), vmax=max(GA['f']), center=150, yticklabels=False, cbar_ax=None if i else cbar_ax).invert_yaxis()
        if i==75:
            ax.text( 7, -10,'TNFR Binding Rate', fontsize = 8)
    else:
        sns.heatmap(allplots[i], ax=ax, cbar=i == 0, vmin=min(GA['f']), vmax=max(GA['f']), center=150, yticklabels=False,  xticklabels=False,cbar_ax=None if i else cbar_ax).invert_yaxis()
        if i==40:
            ax.scatter(2.5, 1.5, marker='*', s=2, color='red')
        
plt.savefig('cal-GA-f-hm-matplotlib-noNAN.pdf', format='pdf', dpi=320, bbox_inches='tight')






