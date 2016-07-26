#pragma once

#include "ofMain.h"
#include "ofLog.h"
#include "ofxOsc.h"
#include "ofxAubio.h"

const int BUFFER_SIZE = 1366;

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
		Value(py::list args, int index, Value default_value);
		Value(py::list args, int index, float default_value) :
			Value(args, index, Value(default_value)) {
		};
		float operator()() const;

    private:
		float value;
};

class Color{
	public:
		Color(){}
		Color(ofColor _c);

		ofColor c;
};

Entity make_entity(string name, py::list args);
Action make_action(string name, py::list args);
Color make_color(string name, py::list args);


class Pineal : public ofBaseApp{
	public:
		Pineal(int argc, char ** argv);
		void setup();
		void update();
		void exit();
		void draw();

		ofTexture getTexture();

        void sendFloat(string name, float x);
		void audioIn(float * input, int bufferSize, int nChannels);

		void onsetEvent(float & time);
		void beatEvent(float & time);

	private:
		int argc;
		char ** argv;

		ofFbo output;

		ofxOscReceiver oscReceiver;
		ofxOscSender oscClient;
		ofxOscSender oscServer;

		py::object vision;
		ofEasyCam camera;
		ofFbo master;

		ofSoundBuffer inBuf;
		ofxAubioOnset onset;
		ofxAubioBeat beat;
};
