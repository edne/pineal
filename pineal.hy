#!/usr/bin/env hy2

(import [eye [Eye]])
(import [ear [Ear]])
(import [coder [Coder]])

(defmain [args]
  (setv ths [(Eye) (Ear) (Coder)])

  (for [t ths] (.start t))

  (try
    (while True
      (for [t ths] (.join t 1)))
  (catch [KeyboardInterrupt]
    None))

  (for [t ths] (.stop t)))
