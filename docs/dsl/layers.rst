======
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
