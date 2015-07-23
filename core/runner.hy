(defmacro runner [name args &rest body]
  `(defn ~name []

     (import [threading [Thread]])

     (defclass Class [Thread]
       [[__init__
         (fn ~args
           (.__init__ Thread self)
           (setv self._stop false)
           None)]

        [run (fn [self] ~@body)]

        [stop
         (fn [self]
           (setv self._stop true))]])

     (Class)))


(defmacro running [&rest body]
  `(try (while (not self._stop)
          ~@body)
     (catch [KeyboardInterrupt]
       None)))
