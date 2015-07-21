Pineal
======

![random150215](http://i.imgur.com/dGbEcQi.png)

An engine for graphic live-coding on an audio stream, something between
[Fluxus](http://www.pawfal.org/fluxus/) and [Processing](https://processing.org/),
__but in Python!__  
(ok that's not true, it was in Python, now the back-end is in a
[pythonic Lisp dialect](http://hylang.org), but the part you can live-code
is still in Python <del>and I'm not planning to change that</del> (parentheses
are coming))


Examples
--------

### random170215
The code:
```python
from lib.graphic import *
import lib.audio as audio
from math import *
from random import *
from time import time

amp = audio.source("AMP")
bass = audio.source("(LPF 100) AMP")
high = audio.source("(HPF 10000) AMP")


def draw():
    strokeWeight(4)

    do(
        scale(0.98 + 2*amp()),
        frame,
    )()
    do(
        scale(0.5),
        frame,
    )()

    do(
        rotate(time2rad(2)),
        turnaround(6),
        translate(0.1 + 2*amp()),
        scale(0.04),
        psolid(30)(hsv(time())),
    )()
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
Make sure you are using Python 2, and run:
```
      $ pip install -r requirements.txt
```


License
-------
This project is released under the terms of [GNU AGPL](http://www.gnu.org/licenses/agpl-3.0.html), see [LICENSE](LICENSE) file for details


Warning
-------
This project is heavily in development. You can use it, I use it in "production"
(coding at parties). But be prepared to continuous and unexpected changes in
syntax (it's getting even more functional) and new features that randomly appear
or disappear.

I'll try to keep the following section updated, in case of doubt you can look at
`visions/test.py`, it should always work.


Little Tutorial
---------------

Visuals files are located in the `visions` folder, and are responsible for visualizing things on the screen - and thus they are the frontend for the livecoding stuff.

All those files must be written in valid Python - if you save a broken source Pineal will complain (in the debug window), and will keep executing the last valid source.

A visual file is composed by those parts:
* global declarations:
  - audio sources creation with the PinealAudioDSL
* a `draw()` function
* containing a function for every layer of shape manipulation

### Global declarations

Everytime you save a file, it is reloaded into Pineal, and thus executed.

Doing so, everything that is not in a function gets executed once, then the `draw()` function is executed for every frame (60 times a second ideally).

Why an initialization step? Because there are computationally expensive operations that cannot be executed once a frame (without losing much on the performance side).

#### Audio DSL
Audio values can be obtained through a (really simple) DSL, that has three keywords: `AMP, LPF, HPF`.
A stream obtained by a function can be 'piped' into a subsequent stream.

Examples:
```python
amp = audio.source("AMP")  # amp is a function that returns the volume
bass = audio.source"(LPF 100) AMP")  # bass() returns the volume of low-passed signal @ 100 Hz
high = audio.source"(HPF 10000) AMP")  # high() returns the volume of high-passed signal @ 10 kHz
mid = audio.source"(HPF 1000) (LPF 4000) AMP")  # mid() returns the volume of a signal band-passed between 1kHz and 4kHz
```

All the functions obtained through `audio.source` will return a float value of the currespondent parameter (respectively amplitude, bass and high), in the `[0.0, 1.0]` range.

#### Polygons
Example:
```python
p = pwired(4)  # p is an empty square, 4 is the number of sides
q = psolid(40)  # q is almost a circle
# and then:
colored_p = p(rgb(1))  # generate a white square
colored_q = (hsv(0.3))  # generate a green circle
# finally show with:
colored_p()
colored_q()
```
or in a more compact way:
```python
pwired(4)(rgb(1))()
psolid(40)(hsv(0.3))()
```


#### Images
You can load images into Pineal as long as they are in png format and in the `images` folder.
The file is loaded just the first time the function is called.

```python
# This load the images/antani.png file
img = image("antani")
# and this shows it
img()
```
or in a compact way:
```python
image("antani")()
```

#### frame
The frame is a dynamic image - it contains the screenshot of what you drawn just one moment ago - interesting for creating some magic feedback effects.

```python
frame()  # shows the screenshot
```

### Layers
A clean way to draw multiple indipendent layers on the screen (in order to make complex shapes) is to declare a function for every layer of manipulation.
Why is it convenient to do that?
Mainly because Pineal provides a set of Decorators that you can apply to the function, to apply a transformation to the layer in an easy way.

#### Decorators
Keep in mind that the coordinates of the screen canvas on which you are drawing are between -1 and 1 (this holds for both X and Y)
You can apply a bunch of decorators to each layer, for easy transforms:
* `@translate(x)`: moves the layer to the left or to the right of the x amount
* `@translate(x, y)`: set both x and y
* `@rotate(rad)`: rotates the layer of the rad amount (in radiants). To keep things rotating try to pass in e.g. `time.time()`
* `@scale(x)`: scales the layer horizontally
* `@scale(x, y)`: scales both x and y. Of course if you pass '1' as a value no transformation is applied
* `@turnaround(n)`: draws the layer n times, rotating it by one complete rotation divided by n.

#### Do
Decorators and drawing functions can be nestled with the do syntax:
```python
do(
    turnaround(23),
    scale(0.9),
    frame,
)()

do(
    translate(0.5 + amp()),
    psolid(4)(rgb(1)),
    pwired(4)(hsv(0.3)),
)()
```

#### Color functions
All those functions return a Color object, to be assigned to a fill or a stroke property
* `hsv(hue)`: 0.0 is red, 1/3 is green, 2/3 is blue, 1.0 is still red
* `hsv(hue, alpha)`: alpha is the opacity - 0.0 is transparent, 1.0 is completely opaque
* `hsv(hue, saturation, value)`: saturation is how much the color is far from white, and value how much it is far from black
* `hsv(h, s, v, alpha)`
* `rgb(light)`: 0.0 is black, 1.0 is white
* `rgb(light, alpha)`
* `rgb(red, blue, green)`: parameters should be in the [0.0, 1.0] range
* `rgb(r, g, b, alpha)`

#### Magic Feedback

// TODO

### draw()
for every frame, the draw function gets called.
Here you'll call the layer functions you defined in the file - pay attention to the ordering! Latter calls are drawn above.

##### Drawing Options
* `strokeWeight(weight)`: sets the thickness of the lines. Suggested values: [1-10]
