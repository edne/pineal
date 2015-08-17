#!/usr/bin/env hy

(import
  [time [sleep]]
  [core.audio [hear]]
  [numpy :as np]
  [scipy.signal [iirfilter lfilter]]
  [core.osc [osc-sender]])


(require core.macros)


(runner Ear [conf log]
        (log.info "starting ear.hy")

        (setv osc-send (osc-sender conf.OSC_EYE))
        (setv out-dict {})

        (defn hz [f]
          "0Hz -> 0, Nyquist/2 -> 1"
          (setv ny/2 (/ conf.RATE 2))
          (/ f ny/2))

        (setv (, lp-b lp-a)
          (iirfilter 4 [(hz 1) (hz 1000)]))

        (setv (, hp-b hp-a)
          (iirfilter 4 [(hz 10000) (hz 20000)]))

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
                 (assoc out-dict (.format "/{0}/{1}"
                                          ch name)
                   (get values ch)))

               (assoc out-dict (.format "/{}" name)
                 (np.mean (.values values))))

             (analyze "amp"
                      (fn [xs]
                        (-> xs np.abs np.mean )))

             (analyze "bass"
                      (fn [xs]
                        (-> (lfilter lp-b lp-a xs)
                          np.abs np.mean )))

             (analyze "high"
                      (fn [xs]
                        (-> (lfilter hp-b hp-a xs)
                          np.abs np.mean ))))

           "body"
           (fn []
             (running
               (for [(, key val) (.items out-dict)]
                 (osc-send key val))
               (sleep (/ 1 60))))

           "jack_client" "Pineal"
           "channels" (len conf.CHANNELS)
           "rate"     conf.RATE})

        (log.info "stopping ear.hy"))


(defmain [args]
  (.run (Ear)))
