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
       (setv ~g!group (pineal.Group))

       (for [e [~@body]]
         (.add ~g!group e))

       (.render ~g!window ~g!group))))


(defmacro/g! polygon [n &rest attributes]
  "
  Regular polygon with `n` sides
  "
  `(do
     (setv ~g!entity (pineal.Polygon ~n))
     (for [attr [~@attributes]]
       (let [[name   (-> attr first str)]
             [values (rest attr)]
             [s      (apply pineal.Signal values)]]
         (.attribute ~g!entity name s)))
     ~g!entity))
