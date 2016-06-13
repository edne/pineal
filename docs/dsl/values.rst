======
Values
======


get-osc-f
---------

.. code-block:: clj

    (get-osc-f "/some/path" default-value)

Subscribe for a given OSC path and return the received float values, if none
give the default.

**TODO:**
 - Type checking on OSC inputs.
 - Sweeter syntax.


time
----

.. code-block:: clj

    (time)
    (time scale)
    (time scale offset)

Return time in seconds, eventually scaled and translated.

The value is taken from the `/time` OSC path.


amp
---

.. code-block:: clj

    (amp)
    (amp scale)
    (amp scale offset)

Return audio amplitude, eventually scaled and translated.

The value is taken from the `/amp` OSC path.

**TODO:**
 - More audio analysis features.
