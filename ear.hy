#!/usr/bin/env hy

(import
  [sys [exit]]
  [time [sleep]]
  [hy.lex [tokenize]]
  [pyo]
  [core.osc [osc-sender]])


(require core.macros)


(defn AMP [src]
  (pyo.Follower src))

(defn LPF [src f]
  (apply pyo.Biquad [src f] {"type" 0}))

(defn HPF [src f]
  (apply pyo.Biquad [src f] {"type" 1}))


(runner Ear [conf]
        (print "starting ear.hy")

        (setv pyo-server
          (apply pyo.Server
            []
            {"audio" conf.BACKEND
             "jackname" "(pineal)"
             "nchnls" 2}))

        (if (= conf.BACKEND "jack")
          (.setInputOffset pyo-server 2))

        (.boot pyo-server)
        (.start pyo-server)

        (try (do
               (setv src
                 (apply pyo.Input
                   []
                   {"chnl" [0 1]}))
               (print "Pyo is working properly!\n"))
          (catch [pyo.PyoServerStateException]
            (print "Pyo is not working")
            (exit 1)))

        (setv osc-send (osc-sender conf.OSC_EYE))

        (setv amp  (-> src AMP))
        (setv bass (-> src (LPF 100) AMP))
        (setv high (-> src (HPF 10000) AMP))

        (running (osc-send "/eye/audio/amp"
                           (float (.get amp)))

                 (osc-send "/eye/audio/bass"
                           (float (.get bass)))

                 (osc-send "/eye/audio/high"
                           (float (.get high)))

                 (sleep (/ 1 30)))

        (print "\rstopping ear.hy")
        (.stop pyo-server)
        (del pyo-server))


(defmain [args]
  (.run (Ear)))
