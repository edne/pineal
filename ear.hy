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
             (setv amps {})

             (for [(, i ch) (enumerate conf.CHANNELS)]
               (assoc amps ch
                 (-> (get data i) np.mean np.abs)))

             (for [ch conf.CHANNELS]
               (osc-send (.format "/{}/amp" ch)
                         (get amps ch)))

             (osc-send "/amp"
                       (np.mean (.values amps))))

           "body"
           (fn []
             (running (sleep (/ 1 60))))

           "jack_client" "Pineal"
           "channels" (len conf.CHANNELS)
           "rate"     conf.RATE})

        (log.info "stopping ear.hy"))


(defmain [args]
  (.run (Ear)))
