#! /usr/bin/env bash

set -eu

if [ "$#" -lt 3 ]; then
  script_name=$(basename $0)
  echo "Usage: ${script_name} EXPERIMENT_ID GA_PARAMS_FILE GA_CONFIG_FILE CHECKPOINT_FILE"
  echo "(e.g. ${script_name} experiment_1 data/ga_params.json data/ga_config.json path/to/ga_checkpoint.pkl)"
  echo "GA_CONFIG_FILE mandatory argument pointing to a .json with corresponding GA hyperparameters"
  echo "CHECKPOINT_FILE (optional): path to a .pkl file to continue a previous experiment"
  exit 1
  # echo "Usage: ${script_name} EXPERIMENT_ID GA_PARAMS_FILE DISTANCE_TYPE TERMINATION_CRIT POP_NUM CROSSOVER_PROB MUTATION_PROB TOURNAMENT_SIZE CHECKPOINT_FILE"
  # echo "(e.g. ${script_name} experiment_1 data/ga_params.json dtw 30 50 0.75 0.5 3 path/to/ga_checkpoint.pkl)"
  # echo "DISTANCE_TYPE is 'euclidean' for Euclidean, 'dtw' for DTW, and 'l1' for l_1"
  # echo "TERMINATION_CRIT: if integer is given, then max number of generations,"
  # echo "                  else is lower limit of population fitness variance for 5 consecutive generations"
  # echo "POP_NUM: integer, number of individuals in the population"
  # echo "CROSSOVER_PROB: float \\in [0,1] - probability for applying the crossover operator,"
  # echo "MUTATION_PROB: float \\in [0,1] - probability for applying the mutation operator,"
  # echo "TOURNAMENT_SIZE: number of individuals to inclide in each tournament for selection"
  # echo "CHECKPOINT_FILE (optional): path to a .pkl file to continue a previous experiment"
  # exit 1
fi

# uncomment to turn on swift/t logging. Can also set TURBINE_LOG,
# TURBINE_DEBUG, and ADLB_DEBUG to 0 to turn off logging
# export TURBINE_LOG=1 TURBINE_DEBUG=1 ADLB_DEBUG=1
export EMEWS_PROJECT_ROOT=$( cd $( dirname $0 )/.. ; /bin/pwd )
# source some utility functions used by EMEWS in this script
source "${EMEWS_PROJECT_ROOT}/etc/emews_utils.sh"


if [ "$#" -eq 4 ]; then
  export CHECKPOINT_FILE=$EMEWS_PROJECT_ROOT/$4
fi

export EXPID=$1
export TURBINE_OUTPUT=$EMEWS_PROJECT_ROOT/experiments/$EXPID
check_directory_exists

export GA_CONFIG_FILE=$3
# export TERMINATION_CRIT=$4
# export POP_NUM=$5
# export CROSSOVER_PROB=$6
# export MUTATION_PROB=$7
# export TOURNAMENT_SIZE=$8

# TODO edit the number of processes as required (must be more than 3).
export PROCS=120

# TODO edit QUEUE, WALLTIME, PPN, AND TURNBINE_JOBNAME
# as required. Note that QUEUE, WALLTIME, PPN, AND TURNBINE_JOBNAME will
# be ignored if MACHINE flag (see below) is not set
export QUEUE=main
export WALLTIME=72:00:00
export PPN=12
export TURBINE_JOBNAME="${EXPID}_job"

# Extra argument passed to SLURM script
# export TURBINE_SBATCH_ARGS=--qos=debug

# if R cannot be found, then these will need to be
# uncommented and set correctly.
# export R_HOME=/path/to/R
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$R_HOME/lib
# export PYTHONHOME=/path/to/python
export PYTHONPATH=$EMEWS_PROJECT_ROOT/python:$EMEWS_PROJECT_ROOT/ext/EQ-Py

# Resident task workers and ranks
export TURBINE_RESIDENT_WORK_WORKERS=1
export RESIDENT_WORK_RANKS=$(( PROCS - 2 ))

# EQ/Py location
EQPY=$EMEWS_PROJECT_ROOT/ext/EQ-Py

# TODO edit command line arguments, e.g. -nv etc., as appropriate
# for your EQ/Py based run. $* will pass all of this script's
# command line arguments to the swift script
mkdir -p $TURBINE_OUTPUT

EXECUTABLE_SOURCE=$EMEWS_PROJECT_ROOT/data/PhysiBoSSv2/spheroid_TNF_v2
DEFAULT_XML_SOURCE=$EMEWS_PROJECT_ROOT/data/PhysiBoSSv2/config/*
GA_PARAMS_FILE_SOURCE=$2

EXECUTABLE_OUT=$TURBINE_OUTPUT/spheroid_TNF
DEFAULT_XML_OUT=$TURBINE_OUTPUT
GA_PARAMS_FILE_OUT=$TURBINE_OUTPUT/TNF_v2_ga_params.json

cp $EXECUTABLE_SOURCE $EXECUTABLE_OUT
cp -r $DEFAULT_XML_SOURCE $DEFAULT_XML_OUT
cp $GA_PARAMS_FILE_SOURCE $GA_PARAMS_FILE_OUT

CMP_XML_OUT=$DEFAULT_XML_OUT/comparison

SEED=1234
ITERATIONS=10
COMPARISONS=2 # Comparisons. Do NOT change this, unless number of files in the location "DEFAULT_XML_OUT/comparison/" changes.
NUM_POPULATION=4
NUM_REPETITIONS=1 # take the average of NUM_REPETITIONS similar runs (using the same GA individual)

CMD_LINE_ARGS="$* -seed=$SEED -ni=$ITERATIONS -nv=$COMPARISONS -np=$NUM_POPULATION -nr=$NUM_REPETITIONS -exe=$EXECUTABLE_OUT -settings=$CMP_XML_OUT -ga_parameters=$GA_PARAMS_FILE_OUT"

# Uncomment this for the BG/Q:
#export MODE=BGQ QUEUE=default

# set machine to your schedule type (e.g. pbs, slurm, cobalt etc.),
# or empty for an immediate non-queued unscheduled run
# MACHINE="slurm"
MACHINE="slurm"

if [ -n "$MACHINE" ]; then
  MACHINE="-m $MACHINE"
fi

# Add any script variables that you want to log as
# part of the experiment meta data to the USER_VARS array,
# for example, USER_VARS=("VAR_1" "VAR_2")
USER_VARS=()
# log variables and script to to TURBINE_OUTPUT directory
log_script

# echo's anything following this to standard out
set -x
SWIFT_FILE=swift_run_eqpy_compare.swift
swift-t -n $PROCS $MACHINE -p -I $EQPY -r $EQPY $EMEWS_PROJECT_ROOT/swift/$SWIFT_FILE $CMD_LINE_ARGS
