(defmacro runner [name args &rest body]
  `(defn ~name ~args

     (import [threading [Thread]])
     (setv _stop [false])

     (defclass Class [Thread]
       [[run
         (fn [self]
           ~@body)]

        [stop
         (fn [self]
           (setv (car _stop) true))]])

     (Class)))


(defmacro running [&rest body]
  `(try (while (not (car _stop))
          ~@body)
     (catch [KeyboardInterrupt]
       None)))
