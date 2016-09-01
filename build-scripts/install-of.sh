#!/bin/bash

OF_VERSION=0.9.0

if [ ! -d $HOME/openframeworks ]; then
    wget http://openframeworks.cc/versions/v${OF_VERSION}/of_v${OF_VERSION}_linux64_release.tar.gz
    tar xvf of_v${OF_VERSION}_linux64_release.tar.gz
    mv of_v${OF_VERSION}_linux64_release openframeworks
    rm of_v${OF_VERSION}_linux64_release.tar.gz

    sed -i "s/\#include \"RtAudio\.h\"/\#include \"rtaudio\/RtAudio\.h\"/g" openframeworks/libs/openFrameworks/sound/ofRtAudioSoundStream.cpp

    sudo openframeworks/scripts/linux/ubuntu/install_dependencies.sh
    sudo openframeworks/scripts/linux/ubuntu/install_codecs.sh
    openframeworks/scripts/linux/compileOF.sh

    mv openframeworks $HOME

    pushd $HOME/openframeworks/apps/projectGenerator/commandLine
    make
    popd

    pushd pushd $HOME/openframeworks/addond
    git clone https://github.com/aubio/ofxAubio
    popd
fi
