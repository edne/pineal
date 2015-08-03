#!/usr/bin/env hy

(import
  [sys [exit]]
  [time [sleep]]
  [hy.lex [tokenize]]
  [hear [hear]]
  [numpy :as np]
  [core.osc [osc-sender]])


(require core.macros)


(runner Ear [conf log]
        (log.info "starting ear.hy")

        (setv _osc-send (osc-sender conf.OSC_EYE))
        (setv osc-send
          (fn [path val]
            (log.debug (+ path " " (str val)))
            (_osc-send path val)))

        (setv amp [0 0])

        (apply hear
          []
          {"callback"
           (fn [data]
             (setv (car amp)
               (-> (car data) np.mean np.abs)))

           "body"
           (fn []
             (running (osc-send "/eye/audio/amp"
                                (float (car amp)))

                      (sleep (/ 1 30))))})

        (log.info "stopping ear.hy"))


(defmain [args]
  (.run (Ear)))
