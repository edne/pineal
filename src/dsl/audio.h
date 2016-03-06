bool beat_value = false;
int beat_count = 0;

bool onset_value = false;

void update(){
	beat_value = false;
}

void set_beat(){
	beat_value = true;
	beat_count += 1;
}

PINEAL("beat")
bool beat_n(int n){
	if(beat_count % n == 0){
		return true;
	}
	return false;
}

PINEAL("beat")
bool beat(){
	return beat_n(2);
}

void set_onset(){
	onset_value = true;
}

PINEAL("onset")
bool onset(){
	bool value = onset_value;
	onset_value = false;
	return value;
}
