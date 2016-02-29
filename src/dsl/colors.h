namespace colors{
	void background(double r, double g, double b, double a){
		ofBackground(r * 255, g * 255, b * 255, a * 255);
	}

	void color(py::object f, double r, double g, double b, double a){
		static ofColor status_color;
		ofColor old_color = status_color;
		ofColor new_color = ofColor(r * 255, g * 255, b * 255, a * 255);

		status_color = new_color;
		ofSetColor(status_color);

		f();

		status_color = old_color;
		ofSetColor(status_color);
	}

	void fill_status(py::object f, bool status){
		static bool status_fill = true;
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
		fill_status(f, true);
	}

	void no_fill(py::object f){
		fill_status(f, false);
	}

	void line_width(py::object f, double new_width){
		static double status_line_width = 1;
		double old_width = status_line_width;

		status_line_width = new_width;
		ofSetLineWidth(status_line_width);

		f();

		status_line_width = old_width;
		ofSetLineWidth(status_line_width);
	}
}

void def_colors(){
	py::def("background", &colors::background);
	py::def("color", &colors::color);
	py::def("line_width", &colors::line_width);
	py::def("fill", &colors::fill);
	py::def("no_fill", &colors::no_fill);
}
