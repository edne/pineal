(defmacro/g! osc-source [name path]
  `(defn ~name [&optional [mult 1]]
     (setv ~g!source
       (get-source ~path))

     (* mult
       (~g!source))))


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
