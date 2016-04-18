namespace audio{
	bool beat_value = false;
	int beat_count = 0;
	float beat_time = 1.0;
	float last_beat = 0;

	bool onset_value = false;
	float last_onset = 0;

	ofSoundBuffer inBuf;

	void update(){
		beat_value = false;
		onset_value = false;
	}

	void set_inBuf(ofSoundBuffer in){
		inBuf = in;
	}

	void set_beat(){
		beat_value = true;
		beat_count += 1;

		float actual_time = (float)ofGetSystemTimeMicros() / 1000;
		beat_time = actual_time - last_beat;
		last_beat = actual_time;
	}

	void set_onset(){
		onset_value = true;

		float actual_time = (float)ofGetSystemTimeMicros() / 1000;
		last_onset = actual_time;
	}

	bool beat(int n, float t, int position){
		float actual_time = (float)ofGetSystemTimeMicros() / 1000;

		if(beat_count % n == position && actual_time - last_beat < beat_time * t){
			return true;
		}else{
			return false;
		}
	}

	bool onset(float t){
		float actual_time = (float)ofGetSystemTimeMicros() / 1000;

		if(actual_time - last_onset < beat_time * t){
			return true;
		}else{
			return false;
		}
	}

	PINEAL("rms")
	float rms(){
		return inBuf.getRMSAmplitude();
	}

	PINEAL("at_event")
	pAction at_event(bool event){
		return pAction([=](pEntity& e){
			return pEntity([=](){
				if(event){
					e();
				}
			});
		});
	}

	PINEAL("at_beat")
	pAction at_beat(py::list args){
        pValue n(args, 0, 1.0);
        pValue position(args, 1, 0.0);
        pValue dur(args, 2, 1.0);

		return at_event(beat(n(), dur(), position()));
	}

	PINEAL("at_onset")
	pAction at_onset(float dur){
		return at_event(onset(dur));
	}
}
