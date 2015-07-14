#!/usr/bin/env hy

(import
  [sys [exit]]
  [time [sleep]]
  [hy.lex [tokenize]]
  [pyo]
  [config [OSC_EYE BACKEND]]
  [lib.osc [osc-sender]])


(require lib.runner)


(defn AMP [src]
  (pyo.Follower src))

(defn LPF [src f]
  (apply pyo.Biquad [src f] {"type" 0}))

(defn HPF [src f]
  (apply pyo.Biquad [src f] {"type" 1}))


(runner Ear [self]
        (print "starting ear.hy")

        (setv pyo-server
          (apply pyo.Server
            []
            {"audio" BACKEND
             "jackname" "(pineal)"
             "nchnls" 2}))

        (if (= BACKEND "jack")
          (.setInputOffset pyo-server 2))

        (.boot pyo-server)
        (.start pyo-server)

        (try (do
               (setv self.src
                 (apply pyo.Input
                   []
                   {"chnl" [0 1]}))
               (print "Pyo is working properly!\n"))
          (catch [pyo.PyoServerStateException]
            (print "Pyo is not working")
            (exit 1)))

        (setv osc-send (osc-sender OSC_EYE))

        (setv amp  (-> self.src AMP))
        (setv bass (-> self.src (LPF 100) AMP))
        (setv high (-> self.src (HPF 10000) AMP))

        (running (osc-send "/eye/audio/amp"  (float (.get amp)))
                 (osc-send "/eye/audio/bass" (float (.get bass)))
                 (osc-send "/eye/audio/high" (float (.get high)))
                 (sleep (/ 1 30)))

        (print "\rstopping ear.hy")
        (.stop pyo-server)
        (del pyo-server))


(defmain [args]
  (.run (Ear)))
