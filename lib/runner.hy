(import
  [threading [Thread]])


(defclass Runner [Thread]
  "
  A Thread class with a .stop method and a .while-not-stopped loop that
  handle keyboard interrupts
  "
  [[__init__
     (fn [self]
         (.__init__ Thread self)
         (setv self._stop False)
         None)]

   [while-not-stopped (fn [ self
                            &optional [action (fn [] None)]]
                          (try
                            (while (not self._stop)
                                   (action))
                            (catch [KeyboardInterrupt]
                                   None)))]

   [stop
     (fn [self]
         (setv self._stop True))]])
