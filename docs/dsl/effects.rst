=======
Effects
=======

fx
--
Apply an effect chain, from the inner one to the outer

.. code-block:: clj

    (fx [effects] drawings)

Example:

.. code-block:: clj

    (fx [(scale 0.5)
         (rotate (/ pi 6))]

        (draw my-layer)
        (pwired 3 (grey 0.5)))

Here the drawings are first rotated, then scaled.


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
