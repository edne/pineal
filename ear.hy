#!/usr/bin/env hy

(import
  [sys [exit]]
  [time [sleep]]
  [hy.lex [tokenize]]
  [pyo]
  [config [OSC_EYE OSC_EAR BACKEND]]
  [lib.osc [Osc]])


(require lib.runner)


; A small DSL for audio analysis:
(defmacro AMP [src]
  `(pyo.Follower ~src))

(defmacro LPF [src f]
  `(apply pyo.Biquad [~src ~f] {"type" 0}))

(defmacro HPF [src f]
  `(apply pyo.Biquad [~src ~f] {"type" 1}))

; examples:
;   "AMP"             volume
;   "(LPF 100) AMP"   volume of low-passed signal @ 100 Hz
;   "(HPF 10000) AMP" volume of high-passed signal @ 10 kHz

; and the macro to "interpreter" it and generate audio units:
(defmacro Ugen [src cmd]
  `(-> (+ "(do
             (import pyo)
             (-> " '~src " " ~cmd "))")
       tokenize first eval))


(runner Ear [self]
         (print "starting ear.hy")

          (setv osc (Osc))
          (.receiver osc OSC_EAR)
          (.sender osc OSC_EYE)

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

          (setv self.units {})

          (.listen osc "/ear/code"
                   (fn [path args]
                       (setv [cmd] args)
                       (assoc self.units
                              cmd
                              (Ugen self.src cmd))))
          (.start osc)

          (running
            (for [cmd (.keys self.units)]
                 (.send osc
                        (+ "/eye/audio/" cmd)
                        [(-> self.units
                             (get cmd) .get
                             float)]))
            (sleep (/ 1 30)))

          (print "\rstopping ear.hy")
          (.stop osc)
          (.stop pyo-server)
          (del pyo-server))


(defmain [args]
  (.run (Ear)))
