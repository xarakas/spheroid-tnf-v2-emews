#####################################################################################
#----------------------------Description--------------------------------------------#
# Plots of an overview of the results of the experiments conducted                  #
#----------------------------Outputs------------------------------------------------#
# Plots with error bar for the average uncertain points per iteration by each method#
#       ,the average number of simulations required by each method and the average  #
#       number of simulations required per iteration by each method.                #
#####################################################################################

from analysis_utils import *

current_dir = os.getcwd()
figures_dir = os.path.join(current_dir,"figures")
make_dir(figures_dir)

sims_file = 'simulations.csv'
final_sims_file = 'final_simulations.csv'

unc_file = 'uncertain.csv'
final_unc_file = 'final_uncertain.csv'

get_final_file(sims_file,final_sims_file,21)
get_final_file(unc_file,final_unc_file,21)


plot_uncertain_file(figures_dir,unc_file)
plot_simulations_file(figures_dir,sims_file,final_sims_file)
