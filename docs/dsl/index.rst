===
DSL
===

Misc
====

osc-source
----------
Define a function returning the latest value of an osc
signal

.. code-block:: clj

    (osc-source name osc-path)
    (name mult add)

Example:

.. code-block:: clj

    ; at the beginning:
    (osc-source amp "/amp")

    ; and then, later in your code:
    (amp 2 0.5)  ; returns (value of /amp) * 2 + 0.5


stroke-weight
-------------
OpenGL lines width, in pixels

.. code-block:: clj

    (stroke-weight w)


time
----
Time in seconds, scales and translated

.. code-block:: clj

    (time mult add)

time-rad
--------
Like time, but the output spins inside ther interval [0, 2·pi]

.. code-block:: clj

    (time-rad mult add)

Primitives
==========

psolid
------
Draw a solid regular polygon

.. code-block:: clj

    (psolid 4 "b")  ; a blue square


pwired
------
Draw juste the border of a regular polygon

.. code-block:: clj

    (psolid 3 "g")  ; a green triangle


Effects
=======

fx
--
Apply an effect chain

.. code-block:: clj

    (fx [effects] drawings)

Example:

.. code-block:: clj

    (fx [(scale 0.5)
         (rotate (/ pi 6))]

        (draw my-layer)
        (pwired 3 (grey 0.5)))


translate
---------
.. code-block:: clj

    (translate x)
    (translate x y)
    (translate x y z)


scale
-----
.. code-block:: clj

    (scale ratio)
    (scale x y)
    (scale x y z)


rotate
------
.. code-block:: clj

    (rotate angle)
    (rotate angle x y z)

Where `x y z` are the rotation axis, if omitted `0 0 1`

turnaround
----------
By now the only "complex" effect, redraws the content `n` times rotating and
performing optionals translations. In order to dispose the image at the vertexes
of a regular polygon

.. code-block:: clj

    (turnaround n)
    (turnaround n r)
    (turnaround n r1 r2)
    (turnaround n r1 r2 r3 ...)


Coloring
========
Defaults colors are represented by single-letter string, here the definition:

.. code-block:: python

    default_colors = {
        "r": [1, 0, 0],  # red
        "g": [0, 1, 0],  # green
        "b": [0, 0, 1],  # blue

        "y": [1, 1, 0],  # yellow
        "c": [0, 1, 1],  # cyan
        "m": [1, 0, 1],  # magenta

        "w": [1, 1, 1],  # white
        "k": [0, 0, 0],  # black
    }

or composed with palettes


palette
-------
Create a color palette

.. code-block:: clj

    (palette my-palette colors)
    (my-palette index alpha)  ; index is in [0 1]

Example:

.. code-block:: clj

    (palette hsv "rgbr")
    (hsv 0.33 1)  ; green, full alpha
 

Layers
======

draw
----
Draw a layer, layers are defined with `on`

.. code-block:: clj

    (draw my-layer)


on
--
Define a layer and draw stuff on it

Example:

.. code-block:: clj

    (on my-layer
      (fx [(scale 0.9)]
          (draw my-other-layer)
          (pwired 4 (grey 0.5))))
