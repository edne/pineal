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


(defn attrs-from-args [args]
  "
  Split args from attributes, using the : separator
  return the [args attrs] tuple
  "
  (if (in ': args)
    (let [[i     (.index args ':)]
          [attrs (rest (drop i args))]
          [args*       (take i args)]]
      [args* attrs])
    [args []]))


(defmacro/g! window [name &rest args]
  "
  Create and update a window called `name`
  the body should be a sequence of drawable entities

  Example:
  (window main-window
          (polygon ...)
          (group ...)
          ...)
  "
  (setv [body attrs] (attrs-from-args args))
  `(do
     (setv ~g!window (-> '~name
                       str pineal.Window.memo))

     (when (.is-open ~g!window)
       (.render ~g!window
                (group ~@body : ~@attrs)))))


(defmacro/g! layer [name &rest args]
  "
  Offscreen drawing
  draw on an layer

  Example:
  (layer layer-1
         something ...)

  And then:
  (layer-1)
  "
  (setv [body attrs] (attrs-from-args args))
  `(do
     (.render (-> '~name
                str pineal.Layer.memo)
              (group ~@body : ~@attrs))

     (defn ~name []
       (setv ~g!layer (-> '~name
                        str pineal.Layer.memo))
       ~g!layer)))


(defmacro/g! group [&rest args]
  "
  Group of drawable entities and apply transformation
  unmatched attributes are forwarded

  Attributes:
  - [translate x y]
  - [rotate rad]
  - [scale r]
  - [scale x y]

  Example:
  (group (polygon ...)
         (group ...)
         :
         scale     0.5
         translate [0 1]
         fill      (color 1 0 1))
  "
  (setv [body attrs] (attrs-from-args args))
  `(do
     (setv ~g!group (pineal.Group))
     (setv ~g!entities [~@body])

     (for [e ~g!entities]
       (.add ~g!group e))

     (set-attributes ~g!group ~@attrs)

     ~g!group))


(defmacro/g! alias [name &rest args]
  "
  Alias to an entity

  Example:
  (alias red-square
         (polygon 4
                  :
                  fill (color 1 0 0)))

  And then:
  (red-square)
  "
  (setv [body attrs] (attrs-from-args args))
  `(do
     (setv ~g!entity (group ~@body : ~@attrs))
     (defn ~name [&rest args]
       ~g!entity)))


(defmacro/g! polygon [n &rest args]
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
           :
           radius 2
           stroke (color 0.5 0 0))
  "
  (setv [args* attrs] (attrs-from-args args))
  `(do
     (setv ~g!entity (pineal.Polygon ~n))
     (set-attributes ~g!entity ~@attrs)
     ~g!entity))
