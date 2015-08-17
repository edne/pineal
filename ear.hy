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
             (defn analyze [name operation]
               (setv values {})

               (for [(, i ch) (enumerate conf.CHANNELS)]
                 (assoc values ch
                   (operation (get data i))))

               (for [ch conf.CHANNELS]
                 (osc-send (.format "/{0}/{1}"
                                    ch name)
                           (get values ch)))

               (osc-send (.format "/{}" name)
                         (np.mean (.values values))))

             (analyze "amp"
                      (fn [xs]
                        (-> xs np.abs np.mean ))))

           "body"
           (fn []
             (running (sleep (/ 1 60))))

           "jack_client" "Pineal"
           "channels" (len conf.CHANNELS)
           "rate"     conf.RATE})

        (log.info "stopping ear.hy"))


(defmain [args]
  (.run (Ear)))
