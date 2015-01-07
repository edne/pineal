#!/usr/bin/env hy2

(import [time [sleep]]
        [importlib [import_module]]
        [hy.lex [tokenize]]
        [lib.runner [Runner]]
        [lib.windows [Window]]
        [lib.osc [listener]]
        [config [OSC_EAR OSC_EYE]])


(defclass Visual []
  [ [__init__ (fn [self name code]
      (setv self.name (get (.split name "/") -1))
      (.load self)
      None)]

    [load (fn [self]
      (setv modulename (get (.split self.name ".") 0))
      ;try
      (setv module (__import__ (% "visuals.%s" modulename)))
      (.update self.__dict__ module.test.__dict__))]

    [iteration (fn [self]
      ;try
      (.draw self))]

    [draw (fn [self])]])


(defclass Eye [Runner]
  [ [__init__ (fn [self]
      (.__init__ Runner self)
      (setv self.visuals {})
      (.sender listener OSC_EAR)
      (.reciver listener OSC_EYE))]

    [run (fn [self]
      (print "starting eye.hy")

      (.listen listener "/visual/created" self.created)
      (.listen listener "/visual/modified" self.modified)
      (.start listener)

      (setv self.output (Window self.visuals))

      (.iteration self (fn []
        (.update self.output)
        (sleep (/ 1 60))))

      (print "\rstopping eye.hy")
      (.stop listener))]

    [created (fn [self path args]
      (setv [name] args)
      (with [[f (open name)]]
        (setv code (.read f)))
      (assoc self.visuals name (Visual name code)))]

    [modified (fn [self path args]
      (print args))]])


(defmain [args]
  (.run (Eye)))
