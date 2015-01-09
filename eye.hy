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
      (setv self.stack [])
      (.load self)
      None)]

    [load (fn [self]
      (print "loading:" self.name)
      (setv modulename (get (.split self.name ".") 0))
      (try
        (do
          (setv module (__import__ (% "visuals.%s" modulename)))
          (.pop modules (% "visuals.%s" modulename)))  ; remove from sys.modules
        (catch [e Exception]
          (do
            (print e)
            (if self.stack
              (setv module (get self.stack -1))
              (print "BROKEN"))))
        (else
          (.append self.stack module)))
      (print "stack" (len self.stack))
      (.update self.__dict__ (. module __dict__ [modulename] __dict__)))]

    [iteration (fn [self]
      (if self.stack  ; if is not broken
        (try
          (.draw self)
          (catch [e Exception]
            (do
              (print e)
              (.pop self.stack)  ; WHY HERE CAN BE EMPTY???
              (if self.stack
                (do
                  (setv modulename (get (.split self.name ".") 0))
                  (setv module (get self.stack -1))
                  (.update self.__dict__ (. module __dict__ [modulename] __dict__)))
                (print "BROKEN")))))))]

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
