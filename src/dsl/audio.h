bool beat_value = false;

void set_beat(){
	beat_value = true;
}

PINEAL("beat")
bool beat(){
	bool value = beat_value;
	beat_value = false;
	return value;
}

bool onset_value = false;

void set_onset(){
	onset_value = true;
}

PINEAL("onset")
bool onset(){
	bool value = onset_value;
	onset_value = false;
	return value;
}
