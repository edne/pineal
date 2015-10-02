#!/usr/bin/env hy
(require pineal.core)
(import time)


(defmain [&rest args]
  "Run program parts as threads,
  and wait KeyboardInterrupt"
  (start-pineal)

  (try
    (while true
      (time.sleep 1))
    (catch [KeyboardInterrupt] nil))

  (stop-pineal))
