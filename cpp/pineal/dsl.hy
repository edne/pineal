(defmacro loop [&rest body]
  "
  Outermost s-expression
  executed every frame

  Example:
  (loop
    (window ...))
  "
  `(defn loop []
     (import pineal)
     ~@body))


(defmacro color [&rest values]
  "
  Generate a color
  return a 4d signal

  r g b a -> r g b a
  r g b   -> r g b 1
  x a     -> x x x a
  x       -> x x x 1

  Example:
  (color 1 0.5)
  "
  `(pineal.Color ~@values))


(defmacro/g! window [name &rest body]
  "
  Create and update a window called `name`
  the body should be a sequence of drawable entities

  Example:
  (window main-window
          (polygon ...)
          (group ...)
          ...)
  "
  `(do
     (setv ~g!window (-> '~name
                       str pineal.Window.memo))

     (when (.is-open ~g!window)
       (.render ~g!window
                (group [~@body])))))

(defmacro/g! layer [name &rest body]
  "
  Offscreen drawing
  draw on an layer

  Example:
  (layer layer-1
         something ...)
  "
  `(.render (-> '~name
              str pineal.Layer.memo)
            (group [~@body])))

(defmacro/g! draw [name &rest attributes]
  "
  Draw a layer
  "
  `(do
     (setv ~g!layer (-> '~name
                      str pineal.Layer.memo))
     (set-attributes ~g!layer ~@attributes)
     ~g!layer))

(defmacro set-attributes [entity &rest attributes]
  "
  Set entity attributes
  internal
  "
  `(for [attr [~@attributes]]
     (let [[name   (-> attr first str)]
           [values (rest attr)]
           [signal (apply pineal.Signal values)]]
       (.attribute ~entity name signal))))


(defmacro/g! group [entities &rest attributes]
  "
  Group of drawable entities
  forward attributes, innermost ones are setted after

  Example:
  (group [(polygon ...)
          (group ...)
          ...]

         [\"fill\" 1 0 1]
         [...])
  "
  `(do
     (setv ~g!group (pineal.Group))
     (setv ~g!entities [~@entities])

     (for [e ~g!entities]
       (.add ~g!group e))

     (set-attributes ~g!group ~@attributes)

     ~g!group))


(defmacro/g! transform [entities &rest attributes]
  "
  Apply transformation to enitites
  unmatched attributes are forwarded just like a group

  Attributes:
  - [translate x y]
  - [rotate rad]
  - [scale r]
  - [scale x y]

  Example:
  (transform [(polygon ...)
              (group ...)]

             [\"scale\" 0.5]
             [\"transate 0 1\"])
  "
  `(do
     (setv ~g!transform (pineal.Transform))
     (setv ~g!entities [~@entities])

     (for [e ~g!entities]
       (.add ~g!transform e))

     (set-attributes ~g!transform ~@attributes)

     ~g!transform))


(defmacro/g! polygon [n &rest attributes]
  "
  Regular polygon with `n` sides

  Attributes:
  - [line w] stroke width
  - [rotation rad]
  - [radius r]
  - [position x y z]
  - [fill color]
  - [stroke color]

  Example:
  (polygon 4
           [\"radius\" 2]
           [\"stroke\" (color 0.5 0 0)])
  "
  `(do
     (setv ~g!entity (pineal.Polygon ~n))
     (set-attributes ~g!entity ~@attributes)
     ~g!entity))
