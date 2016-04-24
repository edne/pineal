(defmacro --header-- []
  "Things to do outside the --draw-- function"
  '(do
     (import [core [*]])
     (import [math [*]])
     (import [time [time :as --time--]])

     (def 2pi (* 2 pi))
     (value time --time--)
     (value amp rms)))


(defmacro value [name x]
  "Define a function that return the value and optionally takes a scale and a
  offset factor"
  `(defn ~name [&rest args]
     (setv [scale offset] [1 0])

     (when (> (len args) 0)
       (setv scale (get args 0)))

     (when (> (len args) 1)
       (setv offset (get args 1)))

     (-> (~x) (* scale) (+ offset))))


(defmacro change [entity &rest actions] `(change_c ~entity [~@actions]))

; TODO: (defmacro varadic ...)
(defmacro group     [&rest xs] `(group_c     [~@xs]))
(defmacro compose   [&rest xs] `(compose_c   [~@xs]))
(defmacro branch    [&rest xs] `(branch_c    [~@xs]))

(defmacro color     [&rest xs] `(color_c     [~@xs]))

(defmacro scale     [&rest xs] `(scale_c     [~@xs]))
(defmacro translate [&rest xs] `(translate_c [~@xs]))


(defmacro group-for [item-iterator &rest entities]
  (setv [item iterator] item-iterator)
  `(group_c (list (map (fn [~item]
                          (group_c [~@entities]))
                     ~iterator))))


(defmacro branch-for [item-iterator &rest actions]
  (setv [item iterator] item-iterator)
  `(branch_c (list (map (fn [~item]
                          (compose_c [~@actions]))
                     ~iterator))))


(defmacro osc [path default]
  `(osc-value (str '~path) ~default))


(defmacro text [font s]
  `(text_c (str ~font) (str ~s)))


(defmacro beat [n entity pos dur]
  `(~entity (at-beat [~n ~pos ~dur])))


(defmacro seq [n &rest args]
  `(do
     (setv clips [])

     (for [[pos e dur] [~@args]]
       (setv a (at-beat [~n pos dur]))
       (.append clips (change e a)))

     (group_c clips)))

