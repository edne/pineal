#!/usr/bin/env hy2

(import [os]
        [glob [glob]]
        [time [sleep]]
        [watchdog.observers [Observer]]
        [watchdog.events [FileSystemEventHandler]]
        [lib.runner [Runner]]
        [config [OSC_EAR OSC_EYE]]
        [lib.osc [Osc]])


(defn getCode [filename]
  (with [[f (open filename)]]
    (setv code (.read f)))
  code)


(defclass Coder [Runner]
[ [__init__ (fn [self]
      (.__init__ Runner self)
      (setv self.osc (Osc))
      (.sender self.osc OSC_EYE)

      (for [filename (glob "visuals/*.py")]
          (.send self.osc "/visual/coder" [filename (getCode filename)] OSC_EYE))

      (setv handler (Handler self.osc))
      (setv self.observer (Observer))
      (.schedule self.observer handler "visuals" False)

      None)]

    [run (fn [self]
      (print "starting coder.hy")
      (.start self.observer)

      (.iteration self (fn []
        (sleep (/ 1 60))))

      (print "\rstopping coder.hy")
      (.stop self.observer)
      (.join self.observer)

      (.stop self.osc))]])


(defn valid [path]
  (or (.endswith path ".hy") (.endswith path ".py")))


(defclass Handler [FileSystemEventHandler]
  [ [__init__ (fn [self osc]
      (.__init__ FileSystemEventHandler self)
      (setv self.osc osc)
      None)]

    [on_created (fn [self event]
      (if (valid event.src_path)
        (.send
          self.osc "/visual/coder"
          [event.src_path (getCode event.src_path)]
          OSC_EYE)))]

    [on_deleted (fn [self event]
      (if (valid event.src_path)
        (.send self.osc "/visual/deleted" [event.src_path] OSC_EYE)))]

    [on_moved (fn [self event]
      (if (valid event.dest_path)
        (.send self.osc 
          "/visual/moved"
          [event.src_path event.dest_path] OSC_EYE)))]

    [on_modified (fn [self event]
      (if (valid event.src_path)
        (.send
          self.osc "/visual/coder"
          [event.src_path (getCode event.src_path)]
          OSC_EYE)))]])


(defmain [args]
  (.run (Coder)))
