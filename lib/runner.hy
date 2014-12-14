(import [threading [Thread]])

(defclass Runner [Thread]
  [ [__init__ (fn [self]
      (.__init__ Thread self)
      (def self._stop False)
      None)]

    [iteration (fn [self &optional [action (fn [] None)]]
      (try
        (while (not self._stop)
          (action))
      (catch [KeyboardInterrupt] None)))]

    [stop (fn [self]
      (def self._stop True))]])
