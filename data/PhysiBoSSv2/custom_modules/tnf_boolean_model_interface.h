#include "../core/PhysiCell.h"
#include "../modules/PhysiCell_standard_modules.h" 

using namespace BioFVM; 
using namespace PhysiCell;

#include "./submodel_data_structures.h" 

void tnf_boolean_model_interface_setup();

void update_boolean_model_inputs( Cell* pCell, Phenotype& phenotype, double dt );

void update_cell_from_boolean_model(Cell* pCell, Phenotype& phenotype, double dt);

void tnf_bm_interface_main(Cell* pCell, Phenotype& phenotype, double dt);