Pineal Loop Project
===================

* Play your music
* Run PinealLoopProject.py
* Edit a `.py` file in the `visuals` folder or create a new one
* Every time you save output is updated
* Have fun!


Dependencies
------------
* Jack Audio Connection Kit, optional but reccomended
* Some python modules, on a Debian-based system:  
`sudo atp-get install python-pyo python-opengl python-pyglet python-webkit python-dev freeglut3-dev`


Settings
--------

### Graphical settings
With `--output-size WIDTHxHEIGHT` you can set the size of output window (visible only with a secondary monitor), default is fullscreen

### Audio backend
Select the audio backend with `--portaudio`, `--jack`, `--coreaudio`,
default is portaudio

### Network
Set the OSC address of core application or the webserver
with `--osc-core` or `--osc-web` followed by `ip:port`.  
With `--http` you set the address of webserver

### Modules
Remove modules with `--no-module` or select specific modules with `--module`
(e.g. `--no-browser`)

    Modules:
      core        Run visuals and show them in Overview and Master windows
      audio       Do the audio analysis
      web         Run the webserver for the browser interface
      browser     Display a browser window for the web interface

