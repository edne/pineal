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


Example
-------

```python
from tools import *
from lib.audio import amp, bass, high


def draw():
    strokeWeight(5)

    Layer("out")()

    n = 4
    Layer("layer1")(
        Scale(0.9 + high())(
            Turnaround(3)(
                Layer("out"))),

        Turnaround(4)(
            Rotate(time2rad())(
                Translate(0.5 + 8*amp())(
                    Pwired(n, hsv(2*time(), 1 - bass())),
                    Scale(0.1 + 4*bass())(
                        Psolid(n, rgb(0.0, 1)))))))()

    Layer("out")(
        Scale(1.0 - bass())(
            Layer("layer1")))()
```


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

In case of doubt you can look at `visions/test.py`, it should always work.
