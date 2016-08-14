#pragma once

#include "ofMain.h"
#include "ofLog.h"
#include "ofxOsc.h"
#include "ofxAubio.h"

#include <boost/python.hpp>
namespace py = boost::python;


class Entity{
	public:
		Entity();
		Entity(py::object f);
		Entity(function<void(void)> f);

        void __call__();
		void operator()() const;

	private:
		function<void(void)> draw;
};

class Action{
	public:
		Action();
		Action(function<Entity(Entity&)> a);

		Entity __call__(Entity& e);
		Entity operator()(Entity e) const;

	private:
		function<Entity(Entity&)> apply;
};

class Value{
	public:
		Value();
		Value(float x);
		Value(function<float()> f);
		Value(py::list args, int index, Value default_value);
		Value(py::list args, int index, float default_value) :
			Value(args, index, Value(default_value)) {
		};

		Value __call__scale(float scale);
		Value __call__scale_offset(float scale, float offset);
		Value __call__scale_value(Value scale);
		Value __call__scale_offset_value(Value scale, Value offset);

		float __call__();
		float operator()() const;

    private:
		function<float()> getter;
};

class Color{
	public:
		Color(){}
		Color(ofColor _c);

		ofColor c;
};

Action render(int size);

Entity make_entity(string name, py::list args);
Action make_action(string name, py::list args);
Color make_color(string name, py::list args);

void osc_set_float(string name, float x);
void osc_set_string(string name, string x);
string osc_get_string(string name);
Value osc_value(string path, py::list args);

class Ear : public ofBaseApp{
	public:
		void setup();
		void update();

        void sendFloat(string name, float x);
		void audioIn(float * input, int bufferSize, int nChannels);
		void onsetEvent(float & time);
		void beatEvent(float & time);

	private:
		ofxOscSender oscServer;
		ofSoundBuffer inBuf;
		ofxAubioOnset onset;
		ofxAubioBeat beat;
};

class Pineal : public ofBaseApp{
	public:
		Pineal(int argc, char ** argv);
		void setup();
		void update();
		void exit();
		void draw();
		void drawOut(ofEventArgs & args);

		shared_ptr<ofAppBaseWindow> mainWindow;

	private:
		Ear ear;
		py::object code_to_entity;

		int argc;
		char ** argv;

		Entity drawing;
		Entity rendered;

		shared_ptr<ofAppBaseWindow> outWindow;

		ofxOscReceiver oscReceiver;
		ofxOscSender oscClient;

		ofFbo master;
};
