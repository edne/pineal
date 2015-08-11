(defmacro effect [name parameters
                  &rest body]
  `(apply ~name
     (+ [(fn [] ~@body)]
        ~parameters)))
