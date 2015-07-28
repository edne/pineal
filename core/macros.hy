(defmacro new-logger [conf]
  `(do
     (import [logging])

     (setv numeric-level
       (getattr logging
                (.upper (. ~conf LOG-LEVEL))
                None))

     (unless (isinstance numeric-level
                         int)
       (raise (ValueError "Invalid log level")))

     (apply logging.basicConfig
       [] {"level" numeric-level})

     (logging.getLogger --name--)))


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
       (import sys)
       (import [core.conf [get-config]])
       (setv conf (get-config sys.argv))
       (setv log (new-logger conf))
       (~inner conf log))))
