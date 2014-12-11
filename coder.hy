(import [runner [Runner]])
(import [pineal.config [OSC_EAR]])
(import [osc [Osc]])

(def OUT_ADDR ["localhost" 1421])

(defclass Coder [Runner]
[ [__init__ (fn [self]
      (.__init__ Runner self)
      (def self.osc (Osc))
      (.sender self.osc OSC_EAR)

      (.send self.osc "/ear/code" ["amp" "AMP"])
      (.send self.osc "/ear/code" ["bass" "(LPF 110) AMP"])
      (.send self.osc "/ear/code" ["high" "(HPF 1000) AMP"])

      None)]

    [run (fn [self]
      (.iteration self)
      (.stop self.osc))]])
