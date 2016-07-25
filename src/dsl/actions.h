{{ begin_module("actions") }}

	{{ module.bind("hide", "hide") }}
	Action hide(){
		return Action([=](Entity& e){
			return Entity([=](){
			});
		});
	}

	{{ module.bind("scale_c", "scale") }}
	Action scale(py::list args){
		Value x(args, 0, 1.0);
		Value y(args, 1, x);
		Value z(args, 2, x);

		return Action([=](Entity& e){
			return Entity([=](){
				ofPushMatrix();
				ofScale(x(), y(), z());
				e();
				ofPopMatrix();
			});
		});
	}

	{{ module.bind("translate_c", "translate") }}
	Action translate(py::list args){
		Value x(args, 0, 0.0);
		Value y(args, 1, 0.0);
		Value z(args, 2, 0.0);

		return Action([=](Entity& e){
			return Entity([=](){
				ofPushMatrix();
				ofTranslate(x(), y(), z());
				e();
				ofPopMatrix();
			});
		});
	}

	{{ module.bind("rotate_x", "rotate_x") }}
	Action rotate_x(double rad){
		return Action([=](Entity& e){
			return Entity([=](){
				ofPushMatrix();
				ofRotateX(180 * rad / PI);
				e();
				ofPopMatrix();
			});
		});
	}

	{{ module.bind("rotate_y", "rotate_y") }}
	Action rotate_y(double rad){
		return Action([=](Entity& e){
			return Entity([=](){
				ofPushMatrix();
				ofRotateY(180 * rad / PI);
				e();
				ofPopMatrix();
			});
		});
	}

	{{ module.bind("rotate_z", "rotate_z") }}
	Action rotate_z(double rad){
		return Action([=](Entity& e){
			return Entity([=](){
				ofPushMatrix();
				ofRotateZ(180 * rad / PI);
				e();
				ofPopMatrix();
			});
		});
	}

{{ end_module() }}
