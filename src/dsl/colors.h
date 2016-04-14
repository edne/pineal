namespace colors{
	void setup(){
		ofSetColor(255);
		ofFill();
		ofSetLineWidth(1);
	}

	PINEAL("background")
	void background(double r, double g, double b, double a){
		ofBackground(r * 255, g * 255, b * 255, a * 255);
	}

	PINEAL("color")
	pAction color(double r, double g, double b, double a){
		return pAction([=](pEntity& e){
			return pEntity([=](){
				static ofColor status_color;
				ofColor old_color = status_color;
				ofColor new_color = ofColor(r * 255, g * 255, b * 255, a * 255);

				status_color = new_color;
				ofSetColor(status_color);

				e();

				status_color = old_color;
				ofSetColor(status_color);
			});
		});
	}

	pAction fill_status(bool status){
		return pAction([=](pEntity& e){
			return pEntity([=](){
				static bool status_fill = true;
				bool old_fill = status_fill;
				bool new_fill = status;

				status_fill = new_fill;
				if(status_fill){
					ofFill();
				}else{
					ofNoFill();
				}

				e();

				status_fill = old_fill;
				if(status_fill){
					ofFill();
				}else{
					ofNoFill();
				}
			});
		});
	}

	PINEAL("fill")
	pAction fill(){
		return fill_status(true);
	}

	PINEAL("no_fill")
	pAction no_fill(){
		return fill_status(false);
	}

	PINEAL("line_width")
	pAction line_width(double new_width){
		return pAction([=](pEntity& e){
			return pEntity([=](){
				static double status_line_width = 1;
				double old_width = status_line_width;

				status_line_width = new_width;
				ofSetLineWidth(status_line_width);

				e();

				status_line_width = old_width;
				ofSetLineWidth(status_line_width);
			});
		});
	}
}
