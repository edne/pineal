bool beat_value = false;
int beat_count = 0;
float beat_time = 1.0;
float last_beat = 0;

bool onset_value = false;
float last_onset = 0;

float rms_value = 0;

void update(){
	beat_value = false;
	onset_value = false;
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

void set_rms(float value){
	rms_value = value;
}

PINEAL("beat")
bool beat_n_t(int n, float t){
	float actual_time = (float)ofGetSystemTimeMicros() / 1000;

	if(beat_count % n == 0 && actual_time - last_beat < beat_time * t){
		return true;
	}else{
		return false;
	}
}

PINEAL("beat")
bool beat_n(int n){
	return beat_n_t(n, 1.0);
}

PINEAL("beat")
bool beat(){
	return beat_n(1);
}

PINEAL("onset")
bool onset_t(float t){
	float actual_time = (float)ofGetSystemTimeMicros() / 1000;

	if(actual_time - last_onset < beat_time * t){
		return true;
	}else{
		return false;
	}
}

PINEAL("onset")
bool onset(){
	return onset_value;
}

PINEAL("rms")
float rms(){
	return rms_value;
}
