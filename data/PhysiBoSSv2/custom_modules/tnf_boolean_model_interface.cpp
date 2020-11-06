
#include "./tnf_boolean_model_interface.h"

using namespace PhysiCell; 

Submodel_Information tnf_bm_interface_info;

void tnf_boolean_model_interface_setup()
{
    tnf_bm_interface_info.name = "TNF Boolean model interface"; 
	tnf_bm_interface_info.version = "0.1.0";
	
    tnf_bm_interface_info.main_function= tnf_bm_interface_main; 

	// These are just auxiliary variables to keep track of some BN nodes
	tnf_bm_interface_info.cell_variables.push_back( "tnf_node" );
    tnf_bm_interface_info.cell_variables.push_back( "fadd_node" );
    tnf_bm_interface_info.cell_variables.push_back( "nfkb_node" );

	tnf_bm_interface_info.register_model();
}


void update_boolean_model_inputs( Cell* pCell, Phenotype& phenotype, double dt )
{
    if( phenotype.death.dead == true )
	{ return; } 

    static int nR_EB = pCell->custom_data.find_variable_index( "bound_external_TNFR" ); 
    static int nTNF_threshold = pCell->custom_data.find_variable_index( "TNFR_activation_threshold" );

    // This if the step transfer function used to update the state of boolean model inputs
    // using the state of the receptor dynamics model. The continuos value thresholded is
    // the total TNF-recptor complex (doi:10.1016/j.cellsig.2010.08.016)
    if ( pCell->custom_data[nR_EB] > pCell->custom_data[nTNF_threshold] )
	{ pCell->boolean_network.set_node_value("TNF", 1); }
	else
    { pCell->boolean_network.set_node_value("TNF", 0); }

    return;

}


void update_cell_from_boolean_model(Cell* pCell, Phenotype& phenotype, double dt)
{	
    static int nTNF_external = microenvironment.find_density_index( "tnf" );
    static int nTNF_export_rate = pCell->custom_data.find_variable_index( "TFN_net_production_rate" );

    static int apoptosis_model_index = phenotype.death.find_death_model_index( "Apoptosis" );
    static int necrosis_model_index = phenotype.death.find_death_model_index( "Necrosis" );
    
    // Getting the state of the boolean model readouts (Readout can be in the XML)
    bool apoptosis = pCell->boolean_network.get_node_value( "Apoptosis" );
    bool nonACD = pCell->boolean_network.get_node_value( "NonACD" );
    bool survival = pCell->boolean_network.get_node_value( "Survival" );
    bool NFkB = pCell->boolean_network.get_node_value( "NFkB" );
	
	if ( apoptosis ) {
		pCell->start_death(apoptosis_model_index);
		return;
	}

	if ( nonACD ) {
		pCell->start_death(necrosis_model_index);
		return;
	}

	if ( survival && pCell->phenotype.cycle.current_phase_index() == PhysiCell_constants::Ki67_negative ) { 
        pCell->phenotype.cycle.advance_cycle(pCell, phenotype, dt); 
    }

    // If NFkB node is active produce some TNF
	if ( NFkB )	{ 
        double tnf_export_rate = pCell->custom_data[nTNF_export_rate]; 
        phenotype.secretion.net_export_rates[nTNF_external] = tnf_export_rate;
    } else {
        phenotype.secretion.net_export_rates[nTNF_external] = 0;
    }
    
    return;
}


void update_monitor_variables(Cell* pCell )
{
	static int index_tnf_node = pCell->custom_data.find_variable_index("tnf_node");
	static int index_fadd_node = pCell->custom_data.find_variable_index("fadd_node");
	static int index_nfkb_node = pCell->custom_data.find_variable_index("nfkb_node");

	pCell->custom_data[index_nfkb_node] = pCell->boolean_network.get_node_value( "NFkB" ) ;
	pCell->custom_data[index_tnf_node] = pCell->boolean_network.get_node_value("TNF");
	pCell->custom_data[index_fadd_node] = pCell->boolean_network.get_node_value("FADD");

    return;
}


void tnf_bm_interface_main(Cell* pCell, Phenotype& phenotype, double dt)
{
    if( phenotype.death.dead == true )
	{
		pCell->functions.update_phenotype = NULL;
		return;
	}

    static int index_next_physiboss_run = pCell->custom_data.find_variable_index("next_physiboss_run");
    if (PhysiCell_globals.current_time >= pCell->custom_data[index_next_physiboss_run])
    {
        // First we update 
        update_boolean_model_inputs(pCell, phenotype, dt );
    
        // Run maboss to update the boolean state of the cell
        pCell->boolean_network.run_maboss();

        // update the cell fate based on the boolean outputs
        update_cell_from_boolean_model(pCell, phenotype, dt);

        // Get track of some boolean node values for debugging
        update_monitor_variables(pCell);

        // Get noisy step size
        // this should be revisted...
        double next_run_in = pCell->boolean_network.get_time_to_update();
        pCell->custom_data[index_next_physiboss_run] = PhysiCell_globals.current_time + next_run_in;
    }

    return;
}
