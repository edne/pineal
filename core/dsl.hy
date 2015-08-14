(defmacro/g! osc-source [name path]
  `(defn ~name [&optional [mult 1]]
     (setv ~g!source
       (get-source ~path))

     (* mult
       (~g!source))))


(defmacro fx [efs &rest body]
  (setv ef (car efs))
  (if (cdr efs)
    `(fx [~ef]
         (fx [~@(cdr efs)]
             ~@body))
    ; else:
    (let [[name (car ef)]
          [args (list
                  (cdr ef))]]
      `(apply ~name
         (+ [(fn [] ~@body)]
            ~args)))))


(defmacro draw [name]
  `(draw-layer (str '~name)))


(defmacro on [name &rest body]
  `(fx [(on-layer (str '~name))]
       ~@body))
