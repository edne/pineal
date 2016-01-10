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
     (setv g (pineal.Group))

     (for [e [~@body]]
       (.add g e))

     (.render w g)))


(defmacro polygon [n]
  `(pineal.Polygon ~n))
