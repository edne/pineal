#!/usr/bin/env hy2

(import [time [sleep]]
        [importlib [import_module]]
        [hy.lex [tokenize]]
        [lib.runner [Runner]]
        [lib.windows [Window]]
        [lib.osc [listener]]
        [config [OSC_EAR OSC_EYE]])


(defclass Visual []
  [ [__init__ (fn [self fullname code]
      (setv self.name (get (.split fullname "/") -1))
      (.load self fullname)
      None)]

    [load (fn [self fullname]
      (setv modulename (get (.split self.name ".") 0))
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

      (.listen listener "/visual/new" self.new)
      (.start listener)

      (setv self.output (Window self.visuals))

      (.iteration self (fn []
        (.update self.output)
        (sleep (/ 1 60))))

      (print "\rstopping eye.hy")
      (.stop listener))]

    [new (fn [self path args]
      (setv [fullname] args)
      (with [[f (open fullname)]]
        (setv code (.read f)))
      (assoc self.visuals name (Visual fullname code)))]])


(defmain [args]
  (.run (Eye)))
