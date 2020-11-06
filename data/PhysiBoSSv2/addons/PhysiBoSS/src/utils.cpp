#include "utils.h"

std::random_device rd;
std::mt19937 gen(rd());

/* Generate a random integer */
int UniformInt()
{
	std::uniform_int_distribution<int> int_dis;
	return int_dis(gen);
}

/* Generate a random float */
double UniformRandom()
{
	return std::generate_canonical<double, 10>(gen);
}

/* Generate a random float */
double UniformRandom11()
{
	double res = UniformRandom();
	return ( 2.0 * ( res - 0.5 ) ); 
}
