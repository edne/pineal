===============
Transformations
===============


scale
-----
.. code-block:: clj

    (scale ratio)
    (scale x y)
    (scale x y z)


translate
---------
.. code-block:: clj

    (translate x)
    (translate x y)
    (translate x y z)


rotate
------
.. code-block:: clj

    (rotate-x angle)
    (rotate-y angle)
    (rotate-z angle)

Where `x y z` are the rotation axis


turn
----
Redraws the content `n` times rotating, in order to dispose the image at the
vertexes of a regular polygon.

.. code-block:: clj

    (turn-x n)
    (turn-y n)
    (turn-z n)

Where `x y z` are the rotation axis
