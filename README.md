PhysiBoSSv2 - EMEWS
-----------------------

### Description:
This EMEWS workflow incorporates PhysiBoSSv2 using the spheroid-TNF-v2 model to allow parallel execution and large-scale model exploration capabilities.

The spheroid-TNF-v2 is an implementation of a multi-scale agent-based model to simulate the growth of a tumor spheroid, that can take into account the effects of a signaling molecule that binds to cell receptors and can trigger a wide range of difference responses.
Specifically, this workflow uses PhysiCell to provide the cell agents with an intracellular signal transduction model utilizing the PhysiBoSS extension. This signalling model is used to compute cell responses to perturbations such as the presence of signalling molecules and drugs.

Besides finding optimal treatments for tumor reduction, the source code in this repository can also be used to calibrate biophysical parameters of the given model.

The parallel search is performed with the use of a Genetic Algorithm that has configurable objective functions as replaceable components. 

-For calibrating the biophysical parameters, various distance metrics are utilized to measure the difference between the simulation output produced using the various candidate solutions, and the output of two ground truth simulations, which have predefined settings related to drug treatments and are produced by previous (validated) simulator versions.
In particular, the distance types that can be used are the following:

* Euclidean distance
* Dynamic Time Warping
* l1 distance

and the parameters that are being explored are: TNFR Binding rate, TNFR Endocytosis rate, TNFR Recycling rate.

-For the evaluation of drug treatment configurations a different objective function is used, which counts the number of alive tumor cells at the end of the simulation, when applying treatments with the following configurable parameters: TNF Administration frequency, TNF Administration duration, TNF Concentration.

### Installation and Execution
Clone the repository:

`$ git clone https://github.com/xarakas/spheroid-tnf-v2-emews.git`

Compile PhysiBoSSv2:

`$ cd data/PhysiBoSSv2`

`$ make`

`$ cd ../..`

Run a calibration experiment (with the params file being described in .json format, see examples in `data/`):

`$ bash swift/swift_run_eqpy_compare.sh <EXPERIMENT_ID> <GA_PARAMS_FILE> <DISTANCE_TYPE> <CHECKPOINT_FILE> (e.g. ${script_name} experiment_1 data/ga_params.json euclidean last_experiment.pkl)`

<CHECKPOINT_FILE> is optional, and contains the GA state from a previous run (stored automatically inside the experiment folder `experiments/`.
Logs regarding time, individuals examined and their fitness scores can be found in `experiments/<EXPERIMENT_ID>/generations.log`.

Perform parameter sweep (again, a params file should be given, see e.g. `data/inputs.txt`:

`$ bash swift/swift_run_sweep.sh <EXPERIMENT_ID> <SWEEP_INPUT> (e.g. ${script_name} experiment_1 data/input.txt)`

### Important note:
.sh files in the `swift/` folder  set various environment parameters for the execution.
Make sure that:
* PROCS is set to a number higher than 3.
* MACHINE is set to blank ("") if not having `slurm` installed (e.g. when executing locally and not on HPC)

This project is compatible with swift-t v. 1.3+. Earlier
versions will NOT work.

### Further reading:
For more information regarding installation and execution, please see the file how-to-launch.txt

More info regarding EMEWS:
https://emews.github.io

More info regarding PhysiBoSSv2:
https://github.com/bsc-life/PhysiBoSSv2

### Structure:
The project consists of the following directories:

```
EMEWS-PhysiBoSSv2/
  data/
  ext/
  etc/
  python/
    test/
  R/
    test/
  scripts/
  swift/
  README.md
```
The directories are intended to contain the following:

 * `data` - model input etc. data
 * `etc` - additional code used by EMEWS
 * `ext` - swift-t extensions such as eqpy, eqr
 * `python` - python code (e.g. model exploration algorithms written in python)
 * `python/test` - tests of the python code
 * `R` - R code (e.g. model exploration algorithms written R)
 * `R/test` - tests of the R code
 * `scripts` - any necessary scripts (e.g. scripts to launch a model), excluding
    scripts used to run the workflow.
 * `swift` - swift code

Use the subtemplates to customize this structure for particular types of
workflows. These are: sweep, eqpy, and eqr.
