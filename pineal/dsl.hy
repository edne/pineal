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
    (let [[ef (car efs)]]
      `(~ef (fn [] ~@body)))))
