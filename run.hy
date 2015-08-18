#!/usr/bin/env hy
(require pineal.core)


(defmain [args]
  "Run program parts as threads,
  and wait KeyboardInterrupt"
  (start-pineal)

  (try
    (while true nil)
    (catch [KeyboardInterrupt] nil))

  (stop-pineal))
