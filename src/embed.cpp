#include "pineal.h"
#include "dsl/core.h"

BOOST_PYTHON_MODULE(core){
	def_core();
}

Embed::Embed(int argc, char ** argv){
	this->argc = argc;
	this->argv = argv;
}

void Embed::setup(){
	try{
		Py_Initialize();
		PySys_SetArgv(argc, argv);

		PyImport_AppendInittab("core", &initcore);

		vision = py::import("py.vision").attr("Vision")();

		ofSetVerticalSync(true);
		ofEnableDepthTest();

		camera.setDistance(1);
		camera.setNearClip(0.01);

		master.allocate(BUFFER_SIZE, BUFFER_SIZE, GL_RGBA);
		master.begin();
		ofClear(255,255,255, 0);
		master.end();


		ofSetColor(255);
		ofFill();
		ofSetLineWidth(1);

	}catch(py::error_already_set){
		PyErr_Print();
	}
}

void Embed::update(string code){
	try{
		ofLog() << "Updating:\n" << code << "\n";
		vision.attr("update")(code);
	}catch(py::error_already_set){
		PyErr_Print();
	}
}

void Embed::draw(){
	try{
		master.begin();
		camera.begin();
		vision.attr("draw")();
		camera.end();
		master.end();
	}catch(py::error_already_set){
		PyErr_Print();
	}
}

ofTexture Embed::getBuffer(){
	return master.getTexture();
}
