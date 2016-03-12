=====
Audio
=====

at
--
Draw entities at event

.. code-block:: clj

    (at (beat) (cube) ...)

Equivalent to:

.. code-block:: clj

    (if (beat)
      (@ (cube)
         ...))

beat
----
Beat event

.. code-block:: clj

    (beat)
    (beat n)
    (beat n t)

Triggered every `n` beats (default 1) and active for `t` beats (default 1).

onset
-----
Onset event

.. code-block:: clj

    (onset)
    (onset t)

Last for `t` beats (if omitted for just one frame)

amp
---
Root mean square value of the audio input.

.. code-block:: clj

    (amp scale offset)
