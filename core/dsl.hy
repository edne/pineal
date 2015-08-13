(defmacro fx [name parameters
              &rest body]
  `(apply ~name
     (+ [(fn [] ~@body)]
        ~parameters)))


(defmacro draw [name]
  `(draw-layer (str '~name)))


(defmacro on [name &rest body]
  `(fx on-layer [(str '~name)]
       ~@body))
