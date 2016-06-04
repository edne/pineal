{{ begin_module("audio") }}

	bool beat_value = false;
	int beat_count = 0;
	float beat_time = 1.0;
	float last_beat = 0;

	bool onset_value = false;
	float last_onset = 0;

	ofSoundBuffer inBuf;
	ofxOscSender oscServer;

	void setup(){
		oscServer.setup("localhost", 7172);
	}

	void update(){
		beat_value = false;
		onset_value = false;

		float amplitude = inBuf.getRMSAmplitude();

		ofxOscMessage m;
		m.setAddress("/amp");
		m.addFloatArg(amplitude);
		oscServer.sendMessage(m, false);
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

	{{ module.bind("at_event", "at_event") }}
	pAction at_event(bool event){
		return pAction([=](pEntity& e){
			return pEntity([=](){
				if(event){
					e();
				}
			});
		});
	}

	{{ module.bind("at_beat", "at_beat") }}
	pAction at_beat(py::list args){
		pValue n(args, 0, 1.0);
		pValue position(args, 1, 0.0);
		pValue dur(args, 2, 1.0);

		return at_event(beat(n(), dur(), position()));
	}

	{{ module.bind("at_onset", "at_onset") }}
	pAction at_onset(float dur){
		return at_event(onset(dur));
	}

{{ end_module() }}
