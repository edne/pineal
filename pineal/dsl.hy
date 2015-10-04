(defmacro osc-source [name path]
  "
  Define a function returning the latest value of an osc
  signal
  (osc-source name osc-path)
  (name mult add)

  Example:
  (osc-source amp \"/amp\")
  and then:
  (amp 2 0.5)  ; -> (value of /amp) * 2 + 0.5
  "
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
  "
  Create a color palette
  (palette my-palette colors)
  (my-palette index alpha)  ; index is in [0 1]

  Example:
  (palette hsv \"rgbr\")
  (hsv 0.33 1)  ; green, full alpha
  "
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
  "
  Apply an effect chain
  (fx [effects] drawings)

  Example:
  (fx [(scale 0.5)
       (rotate (/ pi 6))]

      (draw my-layer)
      (pwired 3 (grey 0.5)))
  "
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
  "
  Draw a layer, layers are defined with `on`
  (draw my-layer)
  "
  `(draw-layer (str '~name)))


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
