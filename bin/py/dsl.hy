(defmacro loop [&rest body]
  `(do
     (import [math [*]])
     (import [core [background]])

     (defn --loop-- []
       ~@body)))


(defmacro/g! osc-value [name path]
  `(defn ~name [&rest args]
     (setv ~g!mult (if args           (first args)  1))
     (setv ~g!add  (if (slice args 1) (second args) 0))

     ;; TODO handle multidimensional messages
     (setv ~g!value (first (.get --osc--
                                 (str '~path) [0.0])))
     (setv ~g!value
       (try (float ~g!value)
         (catch [] 0.0)))

     (-> ~g!value
       (* ~g!mult) (+ ~g!add))))


(defmacro/g! osc-send [value path]
  `(do
     (import liblo)
     (liblo.send --target-- (str '~path) ~value)))
