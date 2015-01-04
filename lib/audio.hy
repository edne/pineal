(import [lib.osc [listener]]
        [config [OSC_EAR]])


; counts the sources created
(def id 0)


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

  (global id)
  (.send listener "/ear/code" [(str id) code] OSC_EAR)
  (.listen listener (+ "/eye/audio/" (str id)) status.cb)
  (+= id 1)

  status.getv)
