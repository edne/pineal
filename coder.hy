(import os)
(import [glob [glob]])
(import [time [sleep]])
;(import [watchdog.observers [Observer]])
;(import [watchdog.events [FileSystemEventHandler]])
(import [utils.runner [Runner]])
(import [config [OSC_EAR OSC_EYE]])
(import [utils.osc [Osc]])


(defclass Coder [Runner]
[ [__init__ (fn [self]
      (.__init__ Runner self)
      (def self.osc (Osc))
      (.sender self.osc OSC_EAR)
      (.sender self.osc OSC_EYE)

      (for [filename (glob "visuals/*.py")]
        (with [[f (open filename)]]
          (.send self.osc "/visual/new" [filename (.read f)] OSC_EYE)))

      (.send self.osc "/ear/code" ["amp" "AMP"] OSC_EAR)
      (.send self.osc "/ear/code" ["bass" "(LPF 110) AMP"] OSC_EAR)
      (.send self.osc "/ear/code" ["high" "(HPF 1000) AMP"] OSC_EAR)

      None)]

    [run (fn [self]
      (.iteration self (fn []
        (sleep (/ 1 60))))

      (.stop self.osc))]])
