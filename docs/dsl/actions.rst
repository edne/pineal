===============
Transformations
===============


hide
----

.. code-block:: clj

    (hide)


scale
-----

.. code-block:: clj

    (scale x y z)
    (scale x y)
    (scale r)


translate
---------

.. code-block:: clj

    (translate x y z)
    (translate x y)
    (translate x)


rotate-x
--------

.. code-block:: clj

    (rotate-x radiants)


rotate-y
--------

.. code-block:: clj

    (rotate-y radiants)


rotate-z
--------

.. code-block:: clj

    (rotate-z radiants)


color
-----

.. code-block:: clj

    (color some-color)

Apply a color to the entity.


fill
----

.. code-block:: clj

    (fill)

Completely color an entity, active by default.


no-fill
-------

.. code-block:: clj

    (no-fill)

Draw wire-frame.


render
------

.. code-block:: clj

    (render)
    (render size)

Render the entity, on a square buffer of `size` pixels, by default 1366.
Resulting a square image of side 1 centered in the origin.


on-layer
--------

.. code-block:: clj

    (on-layer "layer-name")
    (on-layer "layer-name" size)

Render to a named Frambuffer Object, to display it use the `layer` entity.
