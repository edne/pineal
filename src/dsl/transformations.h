namespace transformations{
    PINEAL("hide")
	pAction hide(){
        return pAction([=](pEntity& e){
			return pEntity([=](){
			});
		});
	}

	PINEAL("scale")
	pAction scale(py::list args){
        pValue x(args, 0, 1.0);
        pValue y(args, 1, x);
        pValue z(args, 2, x);

		return pAction([=](pEntity& e){
			return pEntity([=](){
				ofPushMatrix();
				ofScale(x(), y(), z());
				e();
				ofPopMatrix();
			});
		});
	}

	PINEAL("translate")
	pAction translate(py::list args){
        pValue x(args, 0, 0.0);
        pValue y(args, 1, 0.0);
        pValue z(args, 2, 0.0);

		return pAction([=](pEntity& e){
			return pEntity([=](){
				ofPushMatrix();
				ofTranslate(x(), y(), z());
				e();
				ofPopMatrix();
			});
		});
	}

	PINEAL("rotate_x")
	pAction rotate_x(double rad){
		return pAction([=](pEntity& e){
			return pEntity([=](){
				ofPushMatrix();
				ofRotateX(180 * rad / PI);
				e();
				ofPopMatrix();
			});
		});
	}

	PINEAL("rotate_y")
	pAction rotate_y(double rad){
		return pAction([=](pEntity& e){
			return pEntity([=](){
				ofPushMatrix();
				ofRotateY(180 * rad / PI);
				e();
				ofPopMatrix();
			});
		});
	}

	PINEAL("rotate_z")
	pAction rotate_z(double rad){
		return pAction([=](pEntity& e){
			return pEntity([=](){
				ofPushMatrix();
				ofRotateZ(180 * rad / PI);
				e();
				ofPopMatrix();
			});
		});
	}
}
