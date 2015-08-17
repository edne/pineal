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

(draw my-layer)```


Instructions
------------
* Play your music
* Run `./pineal.hy`
* Edit a `.hy` file in the `visions` folder or create a new one
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

In case of doubt you can look at `visions/test.hy`, it should always work.
