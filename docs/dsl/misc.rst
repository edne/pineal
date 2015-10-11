====
Misc
====

osc-source
----------
Define a function returning the latest value of an osc
signal

.. code-block:: clj

    (osc-source name osc-path)
    (name mult add)

Example:

.. code-block:: clj

    ; at the beginning:
    (osc-source amp "/amp")

    ; and then, later in your code:
    (amp 2 0.5)  ; returns (value of /amp) * 2 + 0.5


stroke-weight
-------------
OpenGL lines width, in pixels

.. code-block:: clj

    (stroke-weight w)


time
----
Time in seconds, scales and translated

.. code-block:: clj

    (time mult add)

time-rad
--------
Like time, but the output spins inside ther interval [0, 2·pi]

.. code-block:: clj

    (time-rad mult add)
