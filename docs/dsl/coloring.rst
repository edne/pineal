========
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
