#!/usr/bin/env hy2

(import [time [sleep]])
(import [hy.lex [tokenize]])
(import [lib.runner [Runner]])
(import [lib.windows [Window]])
(import [lib.osc [Osc]])
(import [config [OSC_EAR OSC_EYE]])


(defmacro entities [es]
  `(setv __entities__ ~es))


(defmacro audio [var code]
  `(do
    (import [config [OSC_EAR]])
    (.send self.osc "/ear/code" [self.name (name '~var) ~code] OSC_EAR)
    (assoc __audio__ (name '~var) 0)
    (setv ~var (fn [] (get __audio__ (name '~var))))))


(defclass Visual []
  [ [__init__ (fn [self name code osc]
      (setv self.name name)
      (setv self.osc osc)
      (setv self.__entities__ [])
      (setv self.__audio__ [])
      (.listen self.osc (+ "/eye/audio/" self.name) self.callback)
      (.load self code)
      None)]

    ; PUT TRY HERE! (maybe with a macro inside?)
    [load (fn [self code]
      (setv [self.__entities__ self.__audio__]
        (->
          (+
            "(do"
            "(setv __entities__ [])"
            "(setv __audio__ {})"
            code
            "[__entities__ __audio__])")
        tokenize first eval)))]

    [callback (fn [self path args]
      (setv [k v] args)
      (assoc self.__audio__ k v))]

    [iteration (fn [self]
            (for [entity self.__entities__] (entity.draw)))]])


(defclass Eye [Runner]
  [ [__init__ (fn [self]
      (.__init__ Runner self)
      (setv self.visuals {})
      (setv self.osc (Osc))
      (.sender self.osc OSC_EAR)
      (.reciver self.osc OSC_EYE))]

    [run (fn [self]
      (print "starting eye.hy")

      (.listen self.osc "/visual/new" self.new)
      (.start self.osc)

      (setv self.output (Window self.visuals))

      (.iteration self (fn []
        (.update self.output)
        (sleep (/ 1 60))))

      (print "\rstopping eye.hy")
      (.stop self.osc))]

    [new (fn [self path args]
      (setv [fullname code] args)
      (setv name (get (.split fullname "/") -1))
      (assoc self.visuals name (Visual name code self.osc)))]])


(defmain [args]
  (.run (Eye)))
