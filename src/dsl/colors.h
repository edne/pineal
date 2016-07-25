{{ begin_module("colors") }}

	void setup(){
		ofSetColor(255);
		ofFill();
		ofSetLineWidth(1);
	}

	{{ module.bind("lerp", "lerp") }}
	Color lerp(float amount, Color p, Color q){
		return Color(p.c.getLerped(q.c, amount));
	}

	{{ module.bind("invert", "invert") }}
	Color invert(Color in_color){
		return Color(in_color.c.getInverted());
	}

	{{ module.bind("rgb_c", "rgb") }}
	Color rgb(py::list args){
		Value r, g, b, a;

		if(py::len(args) <= 2){
			r = Value(args, 0, 1.0);
			g = Value(r);
			b = Value(r);
			a = Value(args, 1, 1.0);
		}else{
			r = Value(args, 0, 1.0);
			g = Value(args, 1, 1.0);
			b = Value(args, 2, 1.0);
			a = Value(args, 3, 1.0);
		}

		return Color(ofColor(255*r(), 255*g(), 255*b(), 255*a()));
	}

	{{ module.bind("color", "color") }}
	Action color(Color p){
		ofColor c = p.c;

		return Action([=](Entity& e){
			return Entity([=](){
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

	Action fill_status(bool status){
		return Action([=](Entity& e){
			return Entity([=](){
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

	{{ module.bind("fill", "fill") }}
	Action fill(){
		return fill_status(true);
	}

	{{ module.bind("no_fill", "no_fill") }}
	Action no_fill(){
		return fill_status(false);
	}

	{{ module.bind("line_width", "line_width") }}
	Action line_width(double new_width){
		return Action([=](Entity& e){
			return Entity([=](){
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

{{ end_module() }}
