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


(defmacro window [name &rest body]
  "
  Create and update a window called `name`
  the body should be a sequence of drawable entities
  (window main-window
          (polygon ...)
          (group ...))
  "
  `(do
     (setv w (-> '~name
               str pineal.Window.memo))

     (when (.is-open w)
       (setv g (pineal.Group))

       (for [e [~@body]]
         (.add g e))

       (.render w g))))


(defmacro polygon [n &rest attributes]
  "
  Regular polygon with `n` sides
  "
  `(do
     (setv e (pineal.Polygon ~n))
     (for [attr [~@attributes]]
       (let [[name   (-> attr first str)]
             [values (rest attr)]
             [s      (apply pineal.Signal values)]]
         (.attribute e name s)))
     e))
