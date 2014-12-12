(import os)
(import [glob [glob]])
(import [time [sleep]])
;(import [watchdog.observers [Observer]])
;(import [watchdog.events [FileSystemEventHandler]])
(import [runner [Runner]])
(import [pineal.config [OSC_CORE VISUALS_PATH]])
(import [osc [Osc]])


(defclass Watcher [Runner]
[ [__init__ (fn [self]
      (.__init__ Runner self)

      (def self.osc (Osc))
      (.sender self.osc OSC_CORE)

      (for [filename (glob "visuals/*.py")]
        (with [[f (open filename)]]
          (.send self.osc "/watcher/new" [filename (.read f)])))

      None)]

    [run (fn [self]
      (.iteration self (fn []
        (sleep 1)))

      (.stop self.osc))]])
