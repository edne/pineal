Pineal
======

![random150215](http://i.imgur.com/dGbEcQi.png)

An engine for graphic live-coding on an audio stream, something between
[Fluxus](http://www.pawfal.org/fluxus/) and [Processing](https://processing.org/),
__but in Python!__  
(ok that's not true, it was in Python, now it is mainly in a
[pythonic Lisp dialect](http://hylang.org))


Example
-------

```hy
(osc-source amp  "/amp")
(osc-source bass "/bass")
(osc-source high "/high")


(stroke-weight 4)

(on my-layer
    (fx [(scale (amp 1 1))]
        (draw my-layer))

    (fx [(scale (amp 4))]
        (pwired 4 [0 1 1 1])
        (psolid 4 [0 0 0 0.1]))

    (fx [(scale (bass 2))]
        (pwired 4 [0 1 0 1])
        (psolid 4 [0 0 0 0.1]))

    (fx [(scale (high 4))]
        (pwired 4 [1 1 1 1])
        (psolid 4 [0 0 0 0.1])))

(draw my-layer)
```


Instructions
------------
**WARNING**: pineal require [Jack](http://www.jackaudio.org/) up and running, so
install and confugure it before everything else
* If you want to use pineal to "hear" audio from your pc, setup jack to create
  _monitor_ input ports
* Play your music
* Create a file where write your visuals
* Run `./run.hy yourfile.hy` and connect pineal to the input source using
  [qjackctl](http://qjackctl.sourceforge.net/),
  [claudia](http://kxstudio.linuxaudio.org/Applications:Claudia) or something else
* Edit your file
* Every time you save output is updated
* Have fun!


Dependencies
------------
Make sure you are using Python 2, and install:
```
    hy==0.11.0
    pyglet
    watchdog
    jack-client==0.3.0
    scipy
```
If you have troubles installing scipy from pip you can use the one from your
distribution repositories


Documentation
-------------
References are avaiable on [Readthedocs](http://pineal.readthedocs.org/en/latest/)


License
-------
This project is released under the terms of [GNU AGPL](http://www.gnu.org/licenses/agpl-3.0.html), see [LICENSE](LICENSE) file for details


Warning
-------
This project is heavily in development. You can use it, I use it in "production"
(coding at parties). But be prepared to continuous and unexpected changes in
syntax (it's getting even more functional) and new features that randomly appear
or disappear.

In case of doubt you can look at `sample.hy` or the `examples/` folder, they
should always work.
