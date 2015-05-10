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

   ; TODO replace everywhere with running macro
   [while-not-stopped (fn [ self
                            &optional [action (fn [] None)]]
                            (while (not self._stop)
                                   (action)))]

   [stop
     (fn [self]
         (setv self._stop True))]])


(defmacro running [action]
  `(while (not self._stop)
          ~action))
