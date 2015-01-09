#!/usr/bin/env hy2

(import [time [sleep]]
        [importlib [import_module]]
        [sys]
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
      (setv modulekey (get (.split self.name ".") 0))
      (setv modulename (% "visuals.%s" modulekey))
      (setv module (import_module modulename))
      (.pop sys.modules (% "visuals.%s" modulekey))
      (.update self.__dict__ module.__dict__))]

    ; TODO check the code @ import stage
    [iteration (fn [self]
      (try
        (.draw self)
        (except [e Exception]
          (print self.name "drawing:" e))))]

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
      (.load self (get self.visuals name)))]

    [load (fn [self visual]
      (try
        (.load visual)
        (except [e Exception]
          (print e))))]])


(defmain [args]
  (.run (Eye)))
