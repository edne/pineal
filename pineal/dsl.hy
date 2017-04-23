(defmacro fx [efs &rest body]
  "
  Apply an effect chain
  (fx [effects] drawings)

  Example:
  (fx [(scale 0.5)
       (rotate (/ pi 6))]

      (draw my-layer)
      (pwired 3 (grey 0.5)))
  "
  (defn unroll [ef efs]
    `(fx [~ef]
         (fx [~@efs]
             ~@body)))

  (if (cdr efs)
    (unroll (car efs)
            (cdr efs))
    (let [[ef (car efs)]
          [name (car ef)]
          [args (cdr ef)]]
      `(~name (fn [] ~@body)
              ~@args))))


(defmacro on [name &rest body]
  "
  Define a layer and draw stuff on it

  Example:
  (on my-layer
      (fx [(scale 0.9)]
          (draw my-other-layer)
          (pwired 4 (grey 0.5))))
  "
  `(fx [(on-layer (str '~name))]
       ~@body))
