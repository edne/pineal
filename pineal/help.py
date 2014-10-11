def help_string():
    return '''
Pineal Loop Project
===================

Graphic settings
----------------
* With `--output-size WIDTHxHEIGHT` you can set the size of output window
(visible only with a secondary monitor), default is fullscreen

* `--render-size` sets the size of the hidden rendering window

Audio backend
-------------
Select the audio backend with `--portaudio`, `--jack` or `--coreaudio`. 
Default is `portaudio`

Network
-------
Set the OSC addresses with `--osc-core` or `--osc-gui` followed by `ip:port`.


Modules
-------
Use only specific modules with `--core`, `--audio` and `--gui`

'''
