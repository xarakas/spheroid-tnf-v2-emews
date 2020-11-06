import io;
import sys;
import files;
import string;
import python;
// import R;

string emews_root = getenv("EMEWS_PROJECT_ROOT");
string turbine_output = getenv("TURBINE_OUTPUT");

string to_xml_code =
"""
import params2xml
import json

params = json.loads('%s')
params['user_parameters.random_seed'] = '%s'

default_settings = '%s'
xml_out = '%s'

params2xml.params_to_xml(params, default_settings, xml_out)
""";

string count_template =
"""
import get_metrics

instance_dir = '%s'
# '30240'
count = get_metrics.get_custom_cell_count(instance_dir)
""";

string find_min =
"""
v <- c(%s)
res <- which(v == min(v))
""";

app (file out, file err) run_model (file shfile, string executable, string param_line, string instance)
{
    "bash" shfile executable param_line emews_root instance @stdout=out @stderr=err;
}

app (void o) summarize_simulation (file summarize_py, string instance_dir) {
    "python" summarize_py instance_dir;
}

(string result) get_result(string instance_dir) {
  // Use a few lines of R code to read the output file
  // See the read_last_row variable above
  string code = count_template % instance_dir;
  result = python_persist(code, "str(count)");
}

app (void o) make_dir(string dirname) {
  "mkdir" "-p" dirname;
}

app (void o) make_output_dir(string instance) {
  "mkdir" "-p" (instance+"/output");
}

// deletes the specified directory
app (void o) rm_dir(string dirname) {
  "rm" "-rf" dirname;
}

main() {

  string executable = argv("exe");
  string default_xml = argv("settings");

  file model_sh = input(emews_root + "/scripts/growth_model.sh");
  file upf = input(argv("parameters"));
  file summarize_py = input(emews_root + "/scripts/summarize_simulation.py");

  string results[];
  string upf_lines[] = file_lines(upf);
  foreach params,i in upf_lines {
    string instance_dir = "%s/instance_%i/" % (turbine_output, i+1);
    make_dir(instance_dir) => {
      make_output_dir(instance_dir) => {
        string xml_out = instance_dir + "settings.xml";
        string code = to_xml_code % (params, i, default_xml, xml_out);
        file out <instance_dir+"out.txt">;
        file err <instance_dir+"err.txt">;
        python_persist(code, "'ignore'") => {
          (out,err) = run_model(model_sh, executable, xml_out, instance_dir) => {
            // results[i] = get_result(instance_dir);
            summarize_simulation (summarize_py, instance_dir); 
            // =>
            //   rm_dir(instance_dir + "output/");
          }
        }
      }
    }
  }

  // string results_str = string_join(results, ",");
  // string code = find_min % results_str;
  // string mins = R(code, "toString(res)");
  // string min_idxs[] = split(mins, ",");
  // string best_params[];
  // foreach s, i in min_idxs {
    // int idx = toint(trim(s));
    // best_params[i] = upf_lines[idx - 1];
  // }
  //file best_out <turbine_output + "/output/best_parameters.txt"> =
  //  write(string_join(best_params, "\n"));
}
