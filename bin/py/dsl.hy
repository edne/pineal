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
  `(defn ~name [&rest g!args]
     (apply (pValue ~x) g!args)))


(defmacro osc [path default]
  `(osc-value (str '~path) ~default))


(defmacro/g! clip [name entity]
  `(defn ~name [&rest actions]
     (setv ~g!entity ~entity)
     (if actions
       (group [~g!entity] (list actions))
       ~g!entity)))


(defmacro beat [n entity pos dur]
  `(~entity (at-beat [~n ~pos ~dur])))


(defmacro seq [n &rest args]
  `(do
    (setv clips [])

    (for [[pos e dur] [~@args]]
      (setv a (at-beat [~n pos dur]))
      (.append clips (group [e] [a])))

    (group clips [])))
 
