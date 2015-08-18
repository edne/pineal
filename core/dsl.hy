(defmacro/g! osc-source [name path]
  `(defn ~name [&rest args]
     (setv mult
       (if args (car args) 1))
     (setv add
       (if (cdr args) (get args 1) 0))

     (setv ~g!source
       (get-source ~path))

     (+ add
        (* mult
          (~g!source)))))


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
