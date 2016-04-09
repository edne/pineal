(defmacro --header-- []
  "Things to do outside the --draw-- function"
  '(do
     (import [core [*]])
     (import [math [*]])
     (import [time [time :as --time--]])

     (def 2pi (* 2 pi))
     (value time (--time--))
     (value amp (rms))))


(defmacro alias [name &rest body]
  "Define simple macros to replace name and first parameters"
  `(defmacro ~name [&rest args]
     `(~@'~body ~@args)))


(defmacro/g! value [name x]
  "Define a function that return the value and optionally takes a scale and a
  offset factor"
  `(defn ~name [&rest g!args]
     (setv [g!mult g!add]
       (cond [(=  (len g!args) 0) [1 0]]
         [(=  (len g!args) 1) [(first g!args) 0]]
         [(>= (len g!args) 2) [(first g!args) (second g!args)]]))
     (-> ~x (* g!mult) (+ g!add))))


(defmacro change [entity &rest actions]
  ; TODO: C++ function
  (if-not actions
    entity
    (let [[a (first actions)]
          [actions* (rest actions)]]
      `(change (~a ~entity)
               ~@actions*))))

(defmacro draw-changes [entity &rest actions]
  `(draw (change ~entity ~@actions)))


(defmacro group [&rest body]
  `(group-c [~@body]))


(defmacro at-event [event &rest body]
  ; TODO: take and return pEntities
  `(if ~event (do ~@body)))


(defmacro osc [path default]
  `(osc-value (str '~path) ~default))
