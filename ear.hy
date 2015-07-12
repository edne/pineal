#!/usr/bin/env hy2

(import
  [sys [exit]]
  [time [sleep]]
  [hy.lex [tokenize]]
  [pyo]
  [config [OSC_EYE OSC_EAR BACKEND]]
  [lib.osc [osc-receiver osc-sender]])


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

        (setv osc-send (osc-sender OSC_EYE))

        (defn code-cb [path args]
          (setv [cmd] args)
          (assoc self.units
            cmd
            (Ugen self.src cmd)))

        (setv osc-receiver-start
          (osc-receiver OSC_EAR
                        {"/ear/code" code-cb}))
        (setv osc-receiver-stop
          (osc-receiver-start))

        (setv amp (Ugen self.src "AMP"))
        (setv bass (Ugen self.src "(LPF 100) AMP"))
        (setv high (Ugen self.src "(HPF 10000) AMP"))

        (running
                 (for [cmd (.keys self.units)]
                   (osc-send (+ "/eye/audio/" cmd)
                             [(-> self.units
                                (get cmd) .get
                                float)]))
                 (osc-send "/eye/audio/amp"  (float (.get amp)))
                 (osc-send "/eye/audio/bass" (float (.get bass)))
                 (osc-send "/eye/audio/high" (float (.get high)))
                 (sleep (/ 1 30)))

        (print "\rstopping ear.hy")
        (osc-receiver-stop)
        (.stop pyo-server)
        (del pyo-server))


(defmain [args]
  (.run (Ear)))
