(import [sys [exit]])
(import [time [sleep]])
(import [utils.runner [Runner]])
(import [hy.lex [tokenize]])
(import pyo)
(import [config [OSC_CORE OSC_EAR BACKEND]])
(import [utils.osc [Osc]])

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
      (def self.osc (Osc))
      (.reciver self.osc OSC_EAR)
      (.sender self.osc OSC_CORE)

      (def self.s
        (apply pyo.Server [] {
          "audio" BACKEND
          "jackname" TITLE
          "nchnls" 2}))

      (if (= BACKEND "jack")
        (.setInputOffset self.s 2)))]

    [run (fn [self]
      (print "staritng pineal.ear")
      (.boot self.s)
      (.start self.s)

      (try (do
        (def self.src
          (apply pyo.Input [] {"chnl" [0 1]}))
        (print "Pyo is working properly!\n"))
      (catch [pyo.PyoServerStateException]
        (print "Pyo is not working")
        (exit 1)))

      (def self.units {})

      ;(def self._pitch (pyo.Yin src))
      ;(def self._note 0)

      (.listen self.osc "/ear/code" self.code)
      (.start self.osc)

      (.iteration self (fn []
        (.update self)
        (sleep (/ 1 30))))

      (.stop self.osc)
      (.stop self.s)
      (del self.s))]

    [update (fn [self]
      (for [k (.keys self.units)]
        (.send self.osc "/ear"
          [k (-> self.units (get k) .get float)])))]

    [code (fn [self path args]
      (def [key cmd] args)
      (def (get self.units key) (RUN self.src cmd)))]])
