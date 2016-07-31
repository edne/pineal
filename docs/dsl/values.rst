======
Values
======


osc
---

.. code-block:: clj

    (osc "/some/path")
    (osc "/some/path" scale)
    (osc "/some/path" scale offset)

Subscribe for a given OSC path and return the received float values,
eventually scaled and translated.

**TODO:**
 - Type checking on OSC inputs.


time
----

.. code-block:: clj

    (time)
    (time scale)
    (time scale offset)

Return time in seconds.

The value is taken from the `/time` OSC path.


amp
---

.. code-block:: clj

    (amp)
    (amp scale)
    (amp scale offset)

Return audio amplitude.

The value is taken from the `/amp` OSC path.

**TODO:**
 - More audio analysis features.
