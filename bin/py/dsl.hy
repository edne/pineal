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


(defmacro -@> [head &rest tail]
  "Threading wrapping macro, like `->` but wraps the head with a lambda"
  (if-not tail 
    head
    (let [[next (first tail)]]
      `(-@> (~(first next) (fn [] ~head)
                           ~@(rest next))
            ~@(rest tail)))))


(defmacro compose [name &rest actions]
  "Compose actions, cannot be anonymous because the implementation of -@>"
  `(defn ~name [f]
     (-@> (f)
          ~@actions)))


(defmacro @ [&rest body]
  "Group macro, wrap more entities in a single expression"
  `((fn [] ~@body)))


(defmacro on [name &rest body]
  "Define a layer an draw on it, then call the layer to blit it"
  `(do
     (on-layer (fn [] ~@body) (str '~name))

     (defn ~name []
       "Draw the layer as an image"
       (draw-layer (str '~name)))))


(defmacro at [event &rest body]
  "Draw something at an event"
  `(if ~event (@ ~@body)))


(defmacro/g! recursion [max-depth entity &rest branches]
  "Recursion macro, experimantal"
  `(do
     (defn recursion* [depth entity actions]
       (when depth
         (entity)
         (for [a actions]
           (recursion* (dec depth)
                       (fn [] (a entity)) actions))))

     (recursion* ~max-depth
                 (fn [] ~entity)
                 [~@(map (fn [b]
                           `(fn [f] (~(first b) f ~@(rest b))))
                      branches)])))
