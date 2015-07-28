#!/usr/bin/env hy

(import
  [eye [Eye]]
  [ear [Ear]]
  [coder [Coder]]
  [core.conf [get-config]])

(require core.macros)


(defmain [args]
  "Run program parts as threads,
  and wait KeyboardInterrupt"
  (setv conf (get-config args))
  (setv log (new-logger conf))
  (setv ths [(Ear conf)
             (Eye conf)
             (Coder conf)])

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
