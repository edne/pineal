========
Keywords
========

draw
----

.. code-block:: clj

    (draw entity)

Draw an entity on the screen.


group
-----

.. code-block:: clj

    (group entity
           entity
           ...)

Group many entities returning a new one.


change
------

.. code-block:: clj

    (change entity
            transformation
            ...)

Apply one or more transformations to an entity, return a new,
transformed, entity.


compose
-------

.. code-block:: clj

    (compose transformation
             transformation
             ...)

Combine transformations "in series", return a new one.

**TODO**
- a picture to explain the idea


branch
------

.. code-block:: clj

    (branch transformation
            transformation
            ...)

Combine transformations "in parallel", return a new one.

**TODO**
- a picture also here



group-for
---------

.. code-block:: clj

    (group-for [i iterator]
               ; entity with i as parameter
               )

Create a group of entities using parameters from a (Python)
iterator.

Example:

.. code-block:: clj

    (group-for [i (range 4)]
               (change (cube)
                       (scale (* 0.1 i))))


branch-for
----------

.. code-block:: clj

    (group-for [i iterator]
               ; transformations with i as parameter
               )

Compose the transformations and create a branch for each iteration.
