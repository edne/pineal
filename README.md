Pineal
======

![random150215](http://i.imgur.com/dGbEcQi.png)

An engine for graphic live-coding on an audio stream, something between 
[Fluxus](http://www.pawfal.org/fluxus/) and [Processing](https://processing.org/), 
__but in Python!__  
(ok that's not true, it was in Python, now the back-end is in a 
[pythonic Lisp dialect](http://hylang.org), but the part you can live-code 
is still in Python and I'm not planning to change that)


Examples
--------

### random170215
The code ([view the file](https://github.com/edne/pineal/blob/master/visions/examples/random170215.py)):
```python
amp = audio.source("AMP")
p = Polygon(30)
frame = Frame()


@turnaroud(6)
def a():
    translate(0.1 + amp())
    p.r = 0.04
    p.fill = hsv(time())
    p.stroke = rgb(0,0)

    p.draw()


def feedback():
    frame.r = 0.98 + amp()
    frame.draw()
    frame.r = 0.5
    frame.draw()


def draw():
    feedback()
    rotate(time2rad(2))
    a()
```
tapping on the microphone outputs:
![random170215](http://giant.gfycat.com/AshamedOrangeEastsiberianlaika.gif)


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
  ```
      # apt-get install python-pyglet python-hy python-watchdog python-pyo
```
* On other systems:
  ```
      $ pip install hy pyglet watchdog
```
  and manually download and install Pyo from [ajaxsoundstudio.com](http://ajaxsoundstudio.com/software/pyo/).


Hacking
-------
* Fork
* Write your amazing graphical modules in `lib/graphic/` folder using Python or Hy
* Import them in `lib/graphic/__init__.py`
* Check if everyting works
* Make a pull-request


IRC
---
`#pineal` on Freenode


License
-------
This project is released under the terms of [GNU AGPL](http://www.gnu.org/licenses/agpl-3.0.html), see [LICENSE](LICENSE) file for details
