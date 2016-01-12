(defmacro loop [&rest body]
  "
  Outermost s-expression
  the body is executed every frame
  (loop
    (window ...))
  "
  `(try
     (do
       (import pineal)
       (while true 
         ~@body))
     (catch [KeyboardInterrupt]
       nil)))


(defmacro color [&rest values]
  "
  Color signal (4d)
  r g b a -> r g b a
  r g b   -> r g b 1
  x a     -> x x x a
  x       -> x x x 1
  "
  `(pineal.Color ~@values))


(defmacro/g! window [name &rest body]
  "
  Create and update a window called `name`
  the body should be a sequence of drawable entities
  (window main-window
          (polygon ...)
          (group ...))
  "
  `(do
     (setv ~g!window (-> '~name
                       str pineal.Window.memo))

     (when (.is-open ~g!window)
       (.render ~g!window
                (group [~@body])))))


(defmacro set-attributes [entity &rest attributes]
  `(for [attr [~@attributes]]
     (let [[name   (-> attr first str)]
           [values (rest attr)]
           [signal (apply pineal.Signal values)]]
       (.attribute ~entity name signal))))


(defmacro/g! group [entities &rest attributes]
  "
  Group of drawable entities
  forward attributes
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
  act like a group
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
  "
  `(do
     (setv ~g!entity (pineal.Polygon ~n))
     (set-attributes ~g!entity ~@attributes)
     ~g!entity))
