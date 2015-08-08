#!/usr/bin/env hy

(import
  [time [sleep]]
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

           "body"
           (fn []
             (running (sleep (/ 1 60))))

           "jack_client" "Pineal"
           "channels" conf.CHANNELS
           "rate"     conf.RATE})

        (log.info "stopping ear.hy"))


(defmain [args]
  (.run (Ear)))
