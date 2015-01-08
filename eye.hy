#!/usr/bin/env hy2

(import [time [sleep]]
        ;[importlib [import_module]]
        [sys [modules]]
        [hy.lex [tokenize]]
        [lib.runner [Runner]]
        [lib.windows [Window]]
        [lib.osc [listener]]
        [config [OSC_EAR OSC_EYE]])


(defclass Visual []
  [ [__init__ (fn [self name]
      (setv self.name (get (.split name "/") -1))
      (.load self)
      None)]

    [load (fn [self]
      (print "loading:" self.name)
      (setv modulename (get (.split self.name ".") 0))
      ;try, push module on a stack
      (setv module (__import__ (% "visuals.%s" modulename)))
      (.update self.__dict__ module.test.__dict__)
      (.pop modules (% "visuals.%s" modulename)))]

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
      (assoc self.visuals name (Visual name)))]

    [modified (fn [self path args]
      (setv [name] args)
      (.load (get self.visuals name)))]])


(defmain [args]
  (.run (Eye)))
