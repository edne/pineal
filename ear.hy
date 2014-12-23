#!/usr/bin/env hy2

(import [sys [exit]])
(import [time [sleep]])
(import [lib.runner [Runner]])
(import [hy.lex [tokenize]])
(import pyo)
(import [config [OSC_EYE OSC_EAR BACKEND]])
(import [lib.osc [Osc]])

(def TITLE "pineal.hear")

(defmacro AMP [src]
  `(pyo.Follower ~src))

(defmacro LPF [src f]
  `(apply pyo.Biquad [~src ~f] {"type" 0}))

(defmacro HPF [src f]
  `(apply pyo.Biquad [~src ~f] {"type" 1}))

(defmacro RUN [src cmd]
  `(->
    (+
     "(do
        (import pyo)
        (-> " '~src " " ~cmd "))")
    tokenize first eval))


(defclass Ear [Runner]
  [ [__init__ (fn [self]
      (.__init__ Runner self)
      (setv self.osc (Osc))
      (.reciver self.osc OSC_EAR)
      (.sender self.osc OSC_EYE)

      (setv self.s
        (apply pyo.Server [] {
          "audio" BACKEND
          "jackname" TITLE
          "nchnls" 2}))

      (if (= BACKEND "jack")
        (.setInputOffset self.s 2)))]

    [run (fn [self]
      (print "starting ear.hy")
      (.boot self.s)
      (.start self.s)

      (try (do
        (setv self.src
          (apply pyo.Input [] {"chnl" [0 1]}))
        (print "Pyo is working properly!\n"))
      (catch [pyo.PyoServerStateException]
        (print "Pyo is not working")
        (exit 1)))

      (setv self.units {})

      ;(setv self._pitch (pyo.Yin src))
      ;(setv self._note 0)

      (.listen self.osc "/ear/code" self.code)
      (.start self.osc)

      (.iteration self (fn []
        (.update self)
        (sleep (/ 1 30))))

      (print "\rstopping ear.hy")
      (.stop self.osc)
      (.stop self.s)
      (del self.s))]

    [update (fn [self]
      (for [[visual var] (.keys self.units)]
        (.send self.osc (+ "/eye/audio/" visual)
          [var (-> self.units (get (tuple [visual var])) .get float)])))]

    [code (fn [self path args]
      (setv [visual var cmd] args)
      (assoc self.units (tuple [visual var]) (RUN self.src cmd)))]])


(defmain [args]
  (.run (Ear)))
