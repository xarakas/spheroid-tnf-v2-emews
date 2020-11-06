import files;
import string;
import sys;
import io;
import stats;
import python;
import math;
import location;
import assert;
// import R;

import EQPy;

string emews_root = getenv("EMEWS_PROJECT_ROOT");
string turbine_output = getenv("TURBINE_OUTPUT");
string resident_work_ranks = getenv("RESIDENT_WORK_RANKS");
string r_ranks[] = split(resident_work_ranks,",");

string to_xml_code =
"""
import params2xml
import json
import glob
import itertools

params = json.loads('%s')

replication = '%s'
params['user_parameters.random_seed'] = '1234'

default_settings_loc = '%s'
xml_out = '%s'

for i, f in enumerate(sorted(glob.glob(default_settings_loc+'/*'))):
  if i == int(replication):
    default_settings = f
    
params2xml.params_to_xml(params, default_settings, xml_out)
""";

string result_template =
"""
import statistics

x = '%s'.split(',')
x = [float(xx) for xx in x]

if len(x) > 0:
  res = sum(x)
else: 
  res = 9999999999
""";

string result_template2 =
"""
import statistics

x = '%s'.split(',')
x = [float(xx) for xx in x]

if len(x) > 0:
  res = statistics.mean(x)
else: 
  res = 9999999999
""";

string count_template =
"""
import get_metrics

instance_dir = '%s'
# '30240'
count = get_metrics.get_custom_cell_count(instance_dir)
""";

string dist_template =
"""
import get_metrics

instance_dir = '%s'
replication = '%s'
emews_root = '%s'
# '30240'
dist = get_metrics.get_simulation_dist(instance_dir, replication, emews_root)
""";

app (file out, file err) run_model (string model_sh, string executable_path, string settings_file, string instance)
{
    "bash" model_sh executable_path settings_file emews_root instance @stdout=out @stderr=err;
}

app (void o) move_file(string filepath, string folderpath) {
  "mv" filepath folderpath;
}

app (void o) summarize_simulation (file summarize_py, string instance_dir) {
    "python" summarize_py instance_dir;
}

(string result) get_result(string instance_dir, int replication) {

  string code = dist_template % (instance_dir, replication, emews_root);
  result = python_persist(code, "str(dist)");
}

(string result) run_obj(string custom_parameters, int ga_iteration, int parameter_iteration, int num_replications, int num_repetitions, string executable, string default_xml_loc)
{
    file summarize_py = input(emews_root + "/scripts/summarize_simulation.py");
    string distance[];
    foreach replication in [0:num_replications-1:1] {
      string distances[];
      foreach repetition in [0:num_repetitions-1:1] {
        // make instance dir
        string instance_dir = "%s/instance_%i_%i_%i_%i/" % (turbine_output, ga_iteration, parameter_iteration, replication+1, repetition+1);
        make_dir(instance_dir) => {
          string xml_out = instance_dir + "settings.xml";
          // replication iteration could be used as a seed, but we have fixed seed here
          string code = to_xml_code % (custom_parameters, replication, default_xml_loc, xml_out);
          file out <instance_dir + "out.txt">;
          file err <instance_dir + "err.txt">;
          string model_sh = emews_root + "/scripts/growth_model.sh";
          python_persist(code, "'ignore'") =>
          (out,err) = run_model(model_sh, executable, xml_out, instance_dir) => {
            distances[repetition] = get_result(instance_dir, replication);
  	        summarize_simulation (summarize_py, instance_dir) => {
                move_file(instance_dir + "output/metrics.txt", instance_dir) => {
                    rm_dir(instance_dir + "output/");
                }
            }
          }
        }
      }
      string distance_string = string_join(distances, ",");
      string code = result_template2 % distance_string;
      average = python_persist(code, "str(res)");
      distance[replication] = average;
    }
    string distances_string = string_join(distance, ",");
    string code = result_template % distances_string;
    result = python_persist(code, "str(res)");

}

(void v) loop (location ME, int trials, int repetitions, string executable_model, string default_xml_loc) {
    for (boolean b = true, int i = 1;
       b;
       b=c, i = i + 1)
  {
    // gets the model parameters from the python algorithm
    string params =  EQPy_get(ME);
    boolean c;
    // TODO
    // Edit the finished flag, if necessary.
    // when the python algorithm is finished it should
    // pass "DONE" into the queue, and then the
    // final set of parameters. If your python algorithm
    // passes something else then change "DONE" to that
    if (params == "DONE")
    {
        string finals =  EQPy_get(ME);
        // TODO if appropriate
        // split finals string and join with "\\n"
        // e.g. finals is a ";" separated string and we want each
        // element on its own line:
        // multi_line_finals = join(split(finals, ";"), "\\n");
        string fname = "%s/final_result" % (turbine_output);
        file results_file <fname> = write(finals) =>
        printf("Writing final result to %s", fname) =>
        // printf("Results: %s", finals) =>
        v = make_void() =>
        c = false;
    }
    else if (params == "EQPY_ABORT")
    {
        printf("EQPy Aborted");
        string why = EQPy_get(ME);
        // TODO handle the abort if necessary
        // e.g. write intermediate results ...
        printf("%s", why) =>
        v = propagate() =>
        c = false;
    }
    else
    {
        string param_array[] = split(params, ";");
        string results[];
        foreach parameter, parameter_iteration in param_array
        {
            results[parameter_iteration] = run_obj(parameter, i, parameter_iteration, trials, repetitions, executable_model, default_xml_loc);
        }

        string result = join(results, ";");
        //printf("passing %s", res);
        EQPy_put(ME, result) => c = true;
    }
  }
}

// TODO
// Edit function arguments to include those passed from main function
// below
(void o) start (int ME_rank, int num_iterations, int num_population, int num_variations, int num_repetitions, int random_seed, string ga_parameters_file, string executable_model, string default_xml_loc) {
    location ME = locationFromRank(ME_rank);
    // TODO: Edit algo_params to include those required by the python
    // algorithm.
    // algo_params are the parameters used to initialize the
    // python algorithm. We pass these as a comma separated string.
    // By default we are passing a random seed. String parameters
    // should be passed with a \"%s\" format string.
    // e.g. algo_params = "%d,%\"%s\"" % (random_seed, "ABC");
    string algo_params = "%d,%d,%d,'%s'" %  (num_iterations, num_population, random_seed, ga_parameters_file);
    EQPy_init_package(ME,"deap_ga") =>
    EQPy_get(ME) =>
    EQPy_put(ME, algo_params) =>
      loop(ME, num_variations, num_repetitions, executable_model, default_xml_loc) => {
        EQPy_stop(ME);
        o = propagate();
    }
}

// deletes the specified directory
app (void o) rm_dir(string dirname) {
  "rm" "-rf" dirname;
}

// call this to create any required directories
app (void o) make_dir(string dirname) {
  "mkdir" "-p" dirname;
}

main() {

  // TODO
  // Retrieve arguments to this script here
  // these are typically used for initializing the python algorithm
  // Here, as an example, we retrieve the number of variations (i.e. trials)
  // for each model run, and the random seed for the python algorithm.

  string executable = argv("exe");
  string default_xml_loc = argv("settings");

  int random_seed = toint(argv("seed", "0"));
  int num_variations = toint(argv("nv", "1"));
  int num_repetitions = toint(argv("nr", "2"));
  int num_iterations = toint(argv("ni","10"));
  int num_population = toint(argv("np", "5"));
  string ga_parameters_file = argv("ga_parameters");

  // PYTHONPATH needs to be set for python code to be run
  assert(strlen(getenv("PYTHONPATH")) > 0, "Set PYTHONPATH!");
  assert(strlen(emews_root) > 0, "Set EMEWS_PROJECT_ROOT!");

  int rank = string2int(r_ranks[0]);
  start(rank, num_iterations, num_population, num_variations, num_repetitions, random_seed, ga_parameters_file, executable, default_xml_loc);
}
