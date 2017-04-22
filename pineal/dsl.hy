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
     (import [pineal.osc [get-source]])

     (let [[mult (if args       (car args)   1)]
           [add  (if (cdr args) (get args 1) 0)]
           [src  (get-source ~path)]]

       (->> (src) (* mult) (+ add)))))


(defmacro palette [name pal]
  "
  Create a color palette
  (palette my-palette colors)
  (my-palette index alpha)  ; index is in [0 1]

  Example:
  (palette hsv \"rgbr\")
  (hsv 0.33 1)  ; green, full alpha
  "
  `(defn ~name [index &optional in-alpha]
     (let [[[r g b a]
            (from-palette (map color ~pal) 
                          index)]]
       (if (nil? in-alpha)
         [r g b a]
         [r g b in-alpha]))))


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
