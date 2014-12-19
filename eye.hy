#!/usr/bin/env hy2

(import [time [sleep]])
(import [hy.lex [tokenize]])
(import [lib.runner [Runner]])
(import [lib.windows [Window]])
(import [lib.osc [Osc]])
(import [config [OSC_EYE]])
(import [visual [Visual]])


(defclass Visual []
  [ [__init__ (fn [self name code]
      (setv self.name name)
      (setv self._stack [])
      (setv self.entities [])
      (.load self code))]

    [load (fn [self code]
      (try
        (do
          (setv self.entities (->
            (+
              "(do"
              "(setv entities [])"
              code
              "entities)")
            tokenize first eval))
          (.append self._stack code))
        (catch [e Exception]
          (print e))))]

    [iteration (fn [self]
      (if self._stack
        (try
          (do
            (for [entity self.entities] (entity.draw)))
        (catch [e Exception]
          (print e)
          (setv self._stack (slice self._stack 0 -1))
          (if self._stack
            (.iteration self)
            (print "BROKEN"))))))]])


(defclass Eye [Runner]
  [ [__init__ (fn [self]
      (.__init__ Runner self)
      (setv self.visuals {})
      (setv self.osc (Osc))
      (.reciver self.osc OSC_EYE))]

    [run (fn [self]
      (print "starting eye.hy")

      (.listen self.osc "/ear" self.audio)
      (.listen self.osc "/visual/new" self.new)
      (.start self.osc)

      (setv self.output (Window self.visuals))

      (.iteration self (fn []
        (.update self.output)
        (sleep (/ 1 60))))

      (print "\rstopping eye.hy")
      (.stop self.osc))]

    [audio (fn [self path args]
      (for [v (.values self.visuals)]
        '(setv
          (get v.box.__dict__ (get args 0))
          (get args 1))))]

    [new (fn [self path args]
      (setv [name code] args)
      (setv (get self.visuals name) (Visual name code)))]])


(defmain [args]
  (.run (Eye)))
