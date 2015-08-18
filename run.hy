#!/usr/bin/env hy

(import
  [pineal.eye [Eye]]
  [pineal.ear [Ear]]
  [pineal.coder [Coder]])

(require pineal.macros)


(defmain [args]
  "Run program parts as threads,
  and wait KeyboardInterrupt"
  (setv log (new-logger))
  (setv ths [(Ear)
             (Eye)
             (Coder)])

  (for [t ths]
    (.start t))

  (log.info "started pineal")
  (try
    (while true
      (for [t ths]
        (.join t 1)))
    (catch [KeyboardInterrupt]
      None))

  (for [t ths]
    (.stop t)))
