(defmacro osc-source [name path]
  `(defn ~name [&rest args]
     (import [pineal.nerve [get-source]])

     (setv mult
       (if args (car args) 1))
     (setv add
       (if (cdr args) (get args 1) 0))

     (setv source
       (get-source ~path))

     (+ add
        (* mult
          (source)))))


(defmacro palette [name &rest pal]
  `(defn ~name [index &optional alpha]
     (setv pal [~@pal])
     (if (and
           (= (len pal) 1)
           (string? (car pal)))
       (setv pal (-> pal car list)))

     (setv out (from_palette (list (map color pal)) 
                             index))
     (if-not (nil? alpha)
       (+ (slice out 0 3) [alpha])
       out)))


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
