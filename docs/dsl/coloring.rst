========
Coloring
========

background
----------
Color the background

.. code-block:: clj

    (background r g b)


color
-----
Apply a color

.. code-block:: clj

    (color r g b a)
    (color r g b)
    (color grey alpha)
    (color grey)

Example, a blue cube:

.. code-block:: clj

    (-@> (cube 1)
         (color 0 0 1))


fill
----
Fill with color (default)

.. code-block:: clj

    (-@> (cube 1)
         (fill)
         (color 0 0 1))


no-fill
-------
Draw only the lines


.. code-block:: clj

    (-@> (cube 1)
         (no-fill)
         (color 0 0 1))
