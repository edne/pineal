#!/usr/bin/env hy2

(import [time [sleep]]
        [sys]
        [hy.lex [tokenize]]
        [lib.runner [Runner]]
        [lib.windows [Renderer Master Overview]]
        [lib.osc [listener]]
        [lib.pyexec [pyexec]]
        [config [OSC_EAR OSC_EYE]])


(defclass Visual []
  [ [__init__ (fn [self name code]
      (.setName self name)
      (setv self.stack [])

      (defclass Box []
        [ [draw (fn [self])]])
      (setv self.box (Box))

      (.update self code)
      None)]

    [setName (fn [self name]
      (setv self.name (get (.split name "/") -1)))]

    [update (fn [self code]
      (print "\rloading:" self.name)
      (setv filename (% "visuals/%s" self.name))
      (try
        (pyexec code self.box.__dict__)
        (except [e Exception]
          (print self.name e))
        (else
          (.append self.stack code))))]

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

      (.listen listener "/visual/coder" self.coder)
      (.listen listener "/visual/moved" self.moved)
      ;(.listen listener "/visual/deleted" self.deleted)

      (.start listener)

      (setv renderer (Renderer self.visuals))
      (setv master (Master))
      (setv overview (Overview))

      (.iteration self (fn []
        (.update renderer)
        (.update overview renderer.texture)
        (.update master renderer.texture)
        (sleep (/ 1 60))))

      (print "\rstopping eye.hy")
      (.stop listener))]

    [coder (fn [self path args]
      (setv [name code] args)
      (if (in name (self.visuals.keys))
        (.update (get self.visuals name) code)
        (assoc self.visuals name (Visual name code))))]

    [moved (fn [self path args]
      (setv [oldname newname] args)
      (if (in oldname (self.visuals.keys))
        (do
          (.setName (get self.visuals oldname) newname)
          (assoc self.visuals newname (.pop self.visuals oldname)))))]
    ])


(defmain [args]
  (.run (Eye)))
