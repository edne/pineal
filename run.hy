#!/usr/bin/env hy
(import time)
(import [pineal.eye   [eye-runner]])
(import [pineal.ear   [ear-runner]])
(import [pineal.coder [coder-runner]])


(defmain [&rest args]
  "Run program parts as threads,
  and wait KeyboardInterrupt"

  (setv eye   (eye-runner))
  (setv ear   (ear-runner))
  (setv coder (coder-runner))

  (.start eye)
  (.start ear)
  (.start coder)

  (try
    (while true
      (time.sleep 1))
    (catch [KeyboardInterrupt] nil))

  (.stop eye)
  (.stop ear)
  (.stop coder))
