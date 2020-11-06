#ifndef _MaBoSS_Net_h_
#define _MaBoSS_Net_h_

#include "StochasticSimulationEngine.h"
#include "BooleanNetwork.h"
#include "RunConfig.h"
#include "utils.h"

/**
 *	\class MaBoSSNetwork
 *	\brief Interface with MaBoSS software
 * 
 *	\details The MaBOSS network class contains network configs to handle the initialization and run the simulations given an input.
 *
 *	\date 06/08/2020
 *	\author Gerard Pradas, BSC-CNS, based on code developed by Gaelle Letort, Institut Curie
 */

class MaBoSSNetwork
{
	private:
		/** \brief MaBoSS instances: network */
		Network* network;
		/** \brief MaBoSS instances: configurations */
		RunConfig* config;

		/** \brief Time step between each MaBoSS simulation */
		double update_time_step = 10;

		/** \brief Names and indices of network nodes */
		std::map< std::string, int > node_names;

		/**
		 * \brief Given a vectors of bools, returns the corresponding state 
		 * \param input Vector of bools with the same size as the network
		 * \return A NetworkState_Impl instance with the input values
		 */
		NetworkState_Impl create_networkstate(std::vector<bool>* input);

		/**
		 * \brief Given a state and a vectors of bools, writes the states into the vector
		 * \param state State to retrieve the boolean values
		 * \param output Vector of bools to store the state 
		 */
		void retrieve_networkstate_values(NetworkState_Impl state, std::vector<bool>* output);

	public:
		/** 
		 * \brief Class initializer 
		 * \param networkFile, configFile MaBoSS configutation files
		 */
		void init_maboss( std::string networkFile, std::string configFile);

		/** \brief Class destructor */
		void delete_maboss();

		/** 
		 * \brief Restart a vector of bools, to the init values of the network 
		 * \param node_values Vector of bools to write an initial state of the network
		 */
		void restart_node_values(std::vector<bool>* node_values);

		/** 
		 * \brief Run the current network
		 * \param node_values Vector mapping a boolean network to run a simulation
		 */
		void run_simulation(std::vector<bool>* node_values);

		/** 
		 * \brief Return node of given name current value
		 * \param name Node name existing in the boolean network
		 * \return -1 if node doesn't exit, 0 if node is 0, 1 if node is 1
		 */
		int get_maboss_node_index( std::string name );

		/** 
		 * \brief Get update time step 
		 * \return Time step between each MaBoSS simulation
		 */
		inline double get_update_time_step(){ return this->update_time_step; }

		/**
		 * \brief Set update time step 
		 * \param time_step Time step between each MaBoSS simulation
		 */
		inline void set_update_time_step(double time_step) { this->update_time_step = time_step;}
		
		/** 
		 * \brief Print current state of all the nodes of the network 
		 * \param node_values Boolean vector mapping a boolean network
		 */
		void print_nodes(std::vector<bool>* node_values);
};

#endif
