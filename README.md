Pineal
======
An engine for graphic live-coding on an audio stream, something between 
[Fluxus](http://www.pawfal.org/fluxus/) and [Processing](https://processing.org/), 
__but in Python!__  
(ok that's not true, it was in Python, now the back-end is in a 
[pythonic Lisp dialect](http://hylang.org), but the part you can live-code 
is still in Python and I'm not planning to change that)


Example
-------

[![Puff & Chill](http://img.youtube.com/vi/F1WsmDq4GzM/1.jpg)](http://www.youtube.com/watch?v=F1WsmDq4GzM)


Instructions
------------
* Play your music
* Run `./pineal.hy`
* Edit a `.py` file in the `visions` folder or create a new one
* Every time you save output is updated
* Have fun!


Dependencies
------------
* On Debian-Ubuntu:

      # apt-get install python-pyglet python-hy python-watchdog python-pyo


Hacking
-------
* Fork
* Write your amazing graphical modules in `lib/graphic/` folder using Python or Hy
* Import them in `lib/graphic/__init__.py`
* Check if everyting works
* Make a pull-request
