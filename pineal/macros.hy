(defmacro runner [name args &rest body]
  (with-gensyms [inner
                  stopped
                  classname
                  running-body]

    `(defn ~name []
       (defn ~inner ~args
         (import [threading [Thread]])
         (setv ~stopped [false])

         (defn stopped? []
           (car ~stopped))

         (defmacro running [&rest ~running-body]
           `(try (while (not (stopped?))
                   ~@~running-body)
              (catch [KeyboardInterrupt]
                None)))

         (defclass ~classname [Thread]
           [[run
              (fn [self]
                ~@body)]

            [stop
              (fn [self]
                (setv (car ~stopped) true))]])

         (~classname))
       (~inner))))
