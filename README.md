Pineal
======

Graphic synthesis engine, designed for live performances.

![screenshot](https://i.imgur.com/3lBNKan.png)

Like in an audio (subtractive) synthesizer you have some basic oscillators and
then chains of effects and filters, here there are primitive _entities_ and
chains of _actions_ applied to them.


Simple Example
--------------

The code:
```hy
(draw (change (cube)
              (no-fill)
              (line-width 4)
              (color (rgb 0 1 0))
              (rotate-y time)
              ))


```

Will show:

![screenshot](https://i.imgur.com/jTpXBbM.png)

Rotating at 1 turn per second.

Build
-----
- Install OpenFrameworks and make sure to have the command-line
  version of `projectGenerator` in your PATH.
- **TODO:** Linux/Debian build dependencies
- Generate the project with `projectGenerator -a"ofxOsc, ofxAubio" -o"YOUR_OF_PATH" .`
- Change `config.make` with your Python paths.
- Install Python dependencies with `pip install -r requirements.txt`.
- build with `make`.


Run Code
--------
Pineal is an OSC server waiting for code on the path `/run-code`, (similarly to
the Sonic PI Ruby back-end).

You can send the code manually with some OSC utility or use the [Python
Client](https://github.com/edne/pineal-python-client), a small script that
watches a file for changes and sends its content to the server.


Documentation
-------------
References are available on
[Readthedocs](http://pineal.readthedocs.org/en/latest/) and there are some
examples in the `examples/` folder.


License
-------
This project is released under the terms of [GNU
AGPL](http://www.gnu.org/licenses/agpl-3.0.html), see [LICENSE](LICENSE) file
for details

