#!/usr/bin/env hy

(import
  [hear [hear]]
  [numpy :as np]
  [core.osc [osc-sender]])


(require core.macros)


(runner Ear [conf log]
        (log.info "starting ear.hy")

        (setv osc-send (osc-sender conf.OSC_EYE))

        (apply hear
          []
          {"callback"
           (fn [data]
             (osc-send "/eye/audio/amp"
                       (-> (get data 0)
                         np.mean np.abs)))

           "jack_client" "Pineal"
           "channels" conf.CHANNELS
           "rate"     conf.RATE})

        (log.info "stopping ear.hy"))


(defmain [args]
  (.run (Ear)))
