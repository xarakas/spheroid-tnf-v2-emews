PhysiBoSSv2 - EMEWS
-----------------------
This EMEWS workflow incorporates PhysiBoSSv2 using the spheroid-TNF-v2 model to allow parallel execution and large-scale model exploration capabilities.

For more information regarding installation and execution, please see the file how-to-launch.txt

More info regarding PhysiBoSSv2:
https://github.com/bsc-life/PhysiBoSSv2

This project is compatible with swift-t v. 1.3+. Earlier
versions will NOT work.

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
