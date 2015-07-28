#!/usr/bin/env hy

(import
  [eye [Eye]]
  [ear [Ear]]
  [coder [Coder]]
  [core.conf [get-config]]
  [core.logger [new-logger]])


(defmain [args]
  "Run program parts as threads,
  and wait KeyboardInterrupt"
  (setv config (get-config args))
  (setv log (new-logger --name-- config))
  (setv ths [(Ear config)
             (Eye config)
             (Coder config)])

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
