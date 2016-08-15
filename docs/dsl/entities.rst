========
Entities
========


cube
----

.. code-block:: clj

    (cube)


polygon
-------

.. code-block:: clj

    (polygon n)

Regular polygon with `n` sides, centered in the origin with
radius 1.


text
----

.. code-block:: clj

    (text font s)


Text `s`, `font` has to be the file name of a font present in
data folder.

.. code-block:: clj

    (text "monaco.ttf" "Some Text")


osc-text
--------

.. code-block:: clj

    (osc-text font "/some/path")

Like `(text)` but takes the text from an OSC path.


layer
-----

.. code-block:: clj

    (layer "layer-name")

Draw the content of the layer, to generate it use the `on-layer` action.
(You can draw a layer on itself ;) )

*TODO:*
- Tutorial on framebuffer feedback
