======
Values
======

The code sent to `/run-code` is run just once and the resulting entity is
immutable. Values are the way to change its appearance in time (they are
functions called drawing each frame) and can be passed as parameter when creating
entities and actions.


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



LFO
---

Low Frequency Oscillators, used to change parameters.
All the lfo arguments are optional and can be values themselves.

.. code-block:: clj

    (lfo-sin freq amp offset phase)
    (lfo-saw freq amp offset phase)
    (lfo-pwm pwm freq amp offset phase)


Defaults arguments:
 - `freq`: 1 Hz
 - `amp`:  0.5 (range from -0.5 to 0.5)
 - `offset`: 0.5 (so the range becomes from 0 to 1)
 - `phase`: 0 (id always as pure number where 1 is a period, not radiants, also
   in sin)
 - `pwm`: 0.5
