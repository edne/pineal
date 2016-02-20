#include "pineal.h"

namespace dsl{
    int size;
    ofEasyCam camera;
    unordered_map<string, shared_ptr<ofFbo>> layers;

	ofColor status_color;
    double status_line_width = 1;
	bool status_fill = true;

    void new_layer(string name){
        if(layers.find(name) != layers.end()){
            return;
        }
        auto fbo = make_shared<ofFbo>();

		fbo->allocate(size, size, GL_RGBA);
		fbo->begin();
		ofClear(255,255,255, 0);
		fbo->end();
        layers[name] = fbo;
    }

    void on_layer(py::object f, string name){
        if(layers.find(name) == layers.end()){
            new_layer(name);
        }
        layers[name]->begin();
        camera.begin();
        f();
        camera.end();
        layers[name]->end();
    }

    void draw_layer(string name){
        if(layers.find(name) == layers.end()){
            new_layer(name);
        }
        layers[name]->getTexture().draw(-1, -1, 2, 2);
    }

	void of_log(string s){
		ofLog() << s;
	}

	void background(double r, double g, double b, double a){
		ofBackground(r * 255, g * 255, b * 255, a * 255);
	}

	void cube(double r){
		ofDrawBox(r);
	}

	void scale_xyz(py::object f, double x, double y, double z){
		ofPushMatrix();
		ofScale(x, y, z);
		f();
		ofPopMatrix();
	}

	void scale_xy(py::object f, double x, double y){
		scale_xyz(f, x, y, 1);
	}

	void scale_r(py::object f, double r){
		scale_xyz(f, r, r, r);
	}

	void translate_xyz(py::object f, double x, double y, double z){
		ofPushMatrix();
		ofTranslate(x, y, z);
		f();
		ofPopMatrix();
	}

	void translate_xy(py::object f, double x, double y){
		translate_xyz(f, x, y, 0);
	}

	void translate_x(py::object f, double x){
		translate_xyz(f, x, 0, 0);
	}

	void rotate_x(py::object f, double rad){
		ofPushMatrix();
		ofRotateX(180 * rad / PI);
		f();
		ofPopMatrix();
	}

	void rotate_y(py::object f, double rad){
		ofPushMatrix();
		ofRotateY(180 * rad / PI);
		f();
		ofPopMatrix();
	}

	void rotate_z(py::object f, double rad){
		ofPushMatrix();
		ofRotateZ(180 * rad / PI);
		f();
		ofPopMatrix();
	}

	void turn_x(py::object f, int n){
		ofPushMatrix();
		for(int i=0; i<n; i++){
			f();
			ofRotateX(360.0 / n);
		}
		ofPopMatrix();
	}

	void turn_y(py::object f, int n){
		ofPushMatrix();
		for(int i=0; i<n; i++){
			f();
			ofRotateY(360.0 / n);
		}
		ofPopMatrix();
	}

	void turn_z(py::object f, int n){
		ofPushMatrix();
		for(int i=0; i<n; i++){
			f();
			ofRotateZ(360.0 / n);
		}
		ofPopMatrix();
	}

	void color(py::object f, double r, double g, double b, double a){
		ofColor old_color = status_color;
		ofColor new_color = ofColor(r * 255, g * 255, b * 255, a * 255);

		status_color = new_color;
		ofSetColor(status_color);

		f();

		status_color = old_color;
		ofSetColor(status_color);
	}

	void _fill(py::object f, bool status){
		bool old_fill = status_fill;
		bool new_fill = status;

		status_fill = new_fill;
		if(status_fill){
			ofFill();
		}else{
			ofNoFill();
		}

		f();

		status_fill = old_fill;
		if(status_fill){
			ofFill();
		}else{
			ofNoFill();
		}
	}

	void fill(py::object f){
		_fill(f, true);
	}

	void no_fill(py::object f){
		_fill(f, false);
	}

	void line_width(py::object f, double new_width){
		double old_width = status_line_width;

		status_line_width = new_width;
		ofSetLineWidth(status_line_width);

		f();

        status_line_width = old_width;
		ofSetLineWidth(status_line_width);
	}

	BOOST_PYTHON_MODULE(core){
		py::def("on_layer", &on_layer);
		py::def("draw_layer", &draw_layer);

		py::def("of_log", &of_log);
		py::def("background", &background);
		py::def("cube", &cube);

		py::def("scale", &scale_r);
		py::def("scale", &scale_xy);
		py::def("scale", &scale_xyz);

		py::def("translate", &translate_x);
		py::def("translate", &translate_xy);
		py::def("translate", &translate_xyz);

		py::def("rotate_x", &rotate_x);
		py::def("rotate_y", &rotate_y);
		py::def("rotate_z", &rotate_z);

		py::def("turn_x", &turn_x);
		py::def("turn_y", &turn_y);
		py::def("turn_z", &turn_z);

		py::def("color", &color);
		py::def("line_width", &line_width);
		py::def("fill", &fill);
		py::def("no_fill", &no_fill);
	}
}


Embed::Embed(int size, int argc, char ** argv){
    this->size = size;
    this->argc = argc;
    this->argv = argv;
}

void Embed::setup(){
	try{
		Py_Initialize();
		PySys_SetArgv(argc, argv);
		PyImport_AppendInittab("core", &dsl::initcore);

		vision = py::import("py.vision").attr("Vision")();

		ofSetVerticalSync(true);
		ofEnableDepthTest();

        dsl::camera.setDistance(1);
        dsl::camera.setNearClip(0.01);

        dsl::size = size;
        dsl::new_layer("master");

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
        dsl::on_layer(vision.attr("draw"), "master");
	}catch(py::error_already_set){
		PyErr_Print();
	}
}

ofTexture Embed::getBuffer(){
	return dsl::layers["master"]->getTexture();
}
