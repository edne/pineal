#!/usr/bin/env hy

(import
  [sys [exit]]
  [time [sleep]]
  [lib.runner [Runner]]
  [hy.lex [tokenize]]
  [pyo]
  [config [OSC_EYE OSC_EAR BACKEND]]
  [lib.osc [Osc]])


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


(defclass Ear [Runner]
  "
  Does the analysis on the audio input

  Recives from Eye:
  * `/ear/code  [cmd]` to generate the audio units

  Sends to Eye:
  * `/eye/audio/[cmd]  [value]`
  "
  [[__init__
      (fn [self]
          (.__init__ Runner self)
          (setv self.osc (Osc))
          (.receiver self.osc OSC_EAR)
          (.sender self.osc OSC_EYE)

          (setv self.s
                (apply pyo.Server
                       []
                       {"audio" BACKEND
                       "jackname" "(pineal)"
                       "nchnls" 2}))

          (if (= BACKEND "jack")
            (.setInputOffset self.s 2)))]

   [run
     (fn [self]
         (print "starting ear.hy")
         (.boot self.s)
         (.start self.s)

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

         (.listen self.osc "/ear/code" self.code)
         (.start self.osc)

         (.while-not-stopped self
                             (fn []
                                 (.update self)
                                 (sleep (/ 1 30))))

         (print "\rstopping ear.hy")
         (.stop self.osc)
         (.stop self.s)
         (del self.s))]

   [code
     (fn [self path args]
         (setv [cmd] args)
         (assoc self.units
                cmd
                (Ugen self.src cmd)))]

   [update
     (fn [self]
         (for [cmd (.keys self.units)]
              (.send self.osc
                     (+ "/eye/audio/" cmd)
                     [(-> self.units
                          (get cmd) .get
                          float)])))]])


(defmain [args]
  (.run (Ear)))
