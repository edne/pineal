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

  And then:
  (layer-1)
  "
  `(do
     (.render (-> '~name
                str pineal.Layer.memo)
              (group [~@body]))

     (defn ~name []
       (setv ~g!layer (-> '~name
                        str pineal.Layer.memo))
       ~g!layer)))


(defmacro set-attributes [entity &rest attributes]
  "
  Set entity attributes
  internal
  "
  (when attributes
    `(let [[name   (str '~(first attributes))]
           [value  ~(second attributes)]
           [signal (apply pineal.Signal (flatten [value]))]]
       (.attribute ~entity name signal)
       (set-attributes ~entity ~@(slice attributes 2)))))


(defmacro/g! group [entities &rest attributes]
  "
  Group of drawable entities and apply transformation
  unmatched attributes are forwarded

  Attributes:
  - [translate x y]
  - [rotate rad]
  - [scale r]
  - [scale x y]

  Example:
  (group [(polygon ...)
          (group ...)]

         scale     0.5
         translate [0 1]
         fill      (color 1 0 1))
  "
  `(do
     (setv ~g!group (pineal.Group))
     (setv ~g!entities [~@entities])

     (for [e ~g!entities]
       (.add ~g!group e))

     (set-attributes ~g!group ~@attributes)

     ~g!group))


(defmacro/g! alias [name &rest body]
  "
  Alias to an entity

  Example:
  (alias red-square
         (polygon 4
                  fill (color 1 0 0)))

  And then:
  (red-square)
  "
  `(do
     ;; avoid improper *Group -> Group casts
     (setv ~g!entity (group [~@body]))
     (defn ~name [&rest args]
       ~g!entity)))


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
           radius 2
           stroke (color 0.5 0 0))
  "
  `(do
     (setv ~g!entity (pineal.Polygon ~n))
     (set-attributes ~g!entity ~@attributes)
     ~g!entity))
