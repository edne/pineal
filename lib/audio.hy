(import [lib.osc [listener]]
        [config [OSC_EAR]])


(defn source [code]
  (defclass Status []
    [ [__init__ (fn [self]
        (setv self.v 0)
        None)]

      [cb (fn [self path args]
        (setv [self.v] args))]

      [getv (fn [self]
        self.v)]])

  (setv status (Status))

  (.send listener "/ear/code" [code] OSC_EAR)
  (.listen listener (+ "/eye/audio/" code) status.cb)

  status.getv)
