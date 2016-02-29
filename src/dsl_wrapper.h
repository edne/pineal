#include "pineal.h"
#include "dsl/primitives.h"
#include "dsl/layers.h"
#include "dsl/colors.h"
#include "dsl/transformations.h"


void def_core(){
	def_primitives();
	def_layers();
	def_colors();
	def_transformations();
}

BOOST_PYTHON_MODULE(core){
	def_core();
}
