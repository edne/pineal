(import
  [osc [nerve-send nerve-cb!]]
  [config [OSC_EAR]])


(defn source [code]
  "Permits to get audio signals in the livecoding part"
  (defclass Status []
    [[__init__
       (fn [self]
           (setv self.v 0)
           None)]

     [cb
       (fn [self path args]
           (setv [self.v] args))]

     [getv
       (fn [self]
           self.v)]])

  (setv status (Status))

  (nerve-send "/ear/code" [code])

  (nerve-cb! (+ "/eye/audio/" code)
             status.cb)

  status.getv)
