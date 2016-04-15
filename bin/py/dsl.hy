(defmacro --header-- []
  "Things to do outside the --draw-- function"
  '(do
     (import [core [*]])
     (import [math [*]])
     (import [time [time :as --time--]])

     (def 2pi (* 2 pi))
     (value time (--time--))
     (value amp (rms))))


(defmacro/g! value [name x]
  "Define a function that return the value and optionally takes a scale and a
  offset factor"
  ; TODO: pValue type, castable to int and callable (returning an other pValue)
  `(defn ~name [&rest g!args]
     (setv [g!mult g!add]
       (cond
         [(=  (len g!args) 0) [1 0]]
         [(=  (len g!args) 1) [(first g!args) 0]]
         [(>= (len g!args) 2) [(first g!args) (second g!args)]]))
     (-> ~x (* g!mult) (+ g!add))))


(defmacro osc [path default]
  `(osc-value (str '~path) ~default))


(defmacro symbol [name]
  `(pValue (str '~name)))
