=============
DSL Reference
=============

.. toctree::
   :maxdepth: 2

   primitives
   transformations
   coloring


alias
-----
Create an alias to a function and its first parameters

Example:

.. code-block:: clj

    (alias bg background)
    (alias black-bg bg 0 0 0)

    ; now:
    (bg)       ; is like (background)
    (black-bg) ; is like (background 0 0 0)


value
-----
Wrap a value with a function taking a scale and an offset argument.

.. code-block:: clj

    (value name something)
    ; and then
    (name scale offset)

Is equivalent to:

.. code-block:: clj

    (+ (* something scale) offset)
    ; or
    (-> something (* scale) (+ offset))

-@>
---
Threading wrapping macro, used to apply properties, effects and transformations
to entities.

.. code-block:: clj

    (-@> (cube 1)
         (fill)
         (color 1 0.5 0)
         (translate 0.2))


\@
--
Group macro, wrap entities together before using them in `-@>`

Example, two red cubes with differt size:

.. code-block:: clj

    (-@> (@ (cube 1)
            (cube 0.5))
         (color 1 0 0))
