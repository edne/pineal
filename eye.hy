#!/usr/bin/env hy2

(import [time [sleep]]
        [sys]
        [hy.lex [tokenize]]
        [lib.runner [Runner]]
        [lib.windows [Renderer Overview]]
        [lib.osc [listener]]
        [lib.pyexec [pyexec]]
        [config [OSC_EAR OSC_EYE]])


(defclass Visual []
  [ [__init__ (fn [self name]
      (setv self.name (get (.split name "/") -1))
      (setv self.stack [])

      (defclass Box []
        [ [draw (fn [self])]])
      (setv self.box (Box))

      (.load self)
      None)]

    [load (fn [self]
      (print "loading:" self.name)
      (setv filename (% "visuals/%s" self.name))
      (with [[f (open filename)]]
        (setv code (.read f))
        (try
          (pyexec code self.box.__dict__)
          (except [e Exception]
            (print self.name e))
          (else
            (.append self.stack code)))))]

    [iteration (fn [self]
      (try
        (.draw self)
        (except [e Exception]
          (print self.name self.name e)
          (.pop self.stack)
          (if self.stack
            (do
              (setv code (get self.stack -1))
              (pyexec code self.box.__dict__))
            (print self.name "BROKEN!")))))]

    [draw (fn [self]
      (.draw self.box))]])


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

      (setv renderer (Renderer self.visuals))
      (setv overview (Overview))

      (.iteration self (fn []
        (.update renderer)
        (.update overview renderer.texture)
        (sleep (/ 1 60))))

      (print "\rstopping eye.hy")
      (.stop listener))]

    [created (fn [self path args]
      (setv [name] args)
      (unless (in name (self.visuals.keys))
        (assoc self.visuals name (Visual name))))]

    [modified (fn [self path args]
      (setv [name] args)
      (.load self (get self.visuals name)))]

    [load (fn [self visual]
      (.load visual))]])


(defmain [args]
  (.run (Eye)))
