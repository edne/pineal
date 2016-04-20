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


(defmacro group [&rest entities]
  `(group_c [~@entities]))


(defmacro change [entity &rest actions]
  `(change_c ~entity [~@actions]))


(defmacro compose [&rest actions]
  `(compose_c [~@actions]))


(defmacro osc [path default]
  `(osc-value (str '~path) ~default))


(defmacro beat [n entity pos dur]
  `(~entity (at-beat [~n ~pos ~dur])))


(defmacro seq [n &rest args]
  `(do
     (setv clips [])

     (for [[pos e dur] [~@args]]
       (setv a (at-beat [~n pos dur]))
       (.append clips (change e a)))

     (group_c clips)))

