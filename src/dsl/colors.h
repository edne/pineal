namespace colors{
	void setup(){
		ofSetColor(255);
		ofFill();
		ofSetLineWidth(1);
	}

    {{ bind("colors", "background", "background") }}
	void background(pColor p){
		ofBackground(p.c);
	}

    {{ bind("colors", "lerp", "lerp") }}
	pColor lerp(float amount, pColor p, pColor q){
		return pColor(p.c.getLerped(q.c, amount));
	}

    {{ bind("colors", "invert", "invert") }}
	pColor invert(pColor in_color){
		return pColor(in_color.c.getInverted());
	}

    {{ bind("colors", "rgb_c", "rgb") }}
	pColor rgb(py::list args){
		pValue r, g, b, a;

		if(py::len(args) <= 2){
			r = pValue(args, 0, 1.0);
			g = pValue(r);
			b = pValue(r);
			a = pValue(args, 1, 1.0);
		}else{
			r = pValue(args, 0, 1.0);
			g = pValue(args, 1, 1.0);
			b = pValue(args, 2, 1.0);
			a = pValue(args, 3, 1.0);
		}

		return pColor(ofColor(255*r(), 255*g(), 255*b(), 255*a()));
	}

    {{ bind("colors", "color", "color") }}
	pAction color(pColor p){
		ofColor c = p.c;

		return pAction([=](pEntity& e){
			return pEntity([=](){
				static ofColor status_color;
				ofColor old_color = status_color;
				ofColor new_color = ofColor(c.r, c.g, c.b, c.a);

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

    {{ bind("colors", "fill", "fill") }}
	pAction fill(){
		return fill_status(true);
	}

    {{ bind("colors", "no_fill", "no_fill") }}
	pAction no_fill(){
		return fill_status(false);
	}

    {{ bind("colors", "line_width", "line_width") }}
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
