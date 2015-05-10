#!/usr/bin/env hy2

(import
  [glob [glob]]
  [time [sleep]]
  [watchdog.observers [Observer]]
  [watchdog.events [FileSystemEventHandler]]
  [lib.runner [Runner]]
  [config [OSC_EYE]]
  [lib.osc [Osc]]
  os)

(require lib.runner)


(defmacro last [l]
  `(get ~l -1))


(defmacro handler-method [check action]
  `(fn [self event]
         (when ~check
           ~action)))


(defn get-code [filename]
  (with [[f (open filename)]]
        (.read f)))


(defn get-name [filename]
  (-> filename
      .lower
      (.split "/") last
      (.split ".") first))


(defn valid? [path]
  (.endswith path ".py"))


(defmacro osc-send [path data]
  `(.send self.osc
          ~path
          ~data
          OSC_EYE))


(defclass Coder [Runner]
  "
  Waits for changes in `visions/`

  Sends to Eye:
  * `/eye/code    [filename code]`
  * `/eye/delete  [filename]`
  * `/eye/move    [oldname newname]`
  "
  [[run
     (fn [self]
         (print "starting coder.hy")

         (setv self.osc (Osc))
         (.sender self.osc OSC_EYE)

         (for [filename (glob "visions/*.py")]
              (osc-send "/eye/code"
                        [(get-name filename)
                         (get-code filename)]))

         (setv handler (Handler))
         (setv handler.osc self.osc)

         (setv observer (Observer))
         (.schedule observer handler "visions" False)
         (.start observer)

         (running (sleep (/ 1 60)))

         (print "\rstopping coder.hy")
         (.stop observer)
         (.join observer))]])


(defclass Handler [FileSystemEventHandler]
  [[on-created
     (handler-method (valid? event.src-path)
                     (osc-send "/eye/code"
                               [(get-name event.src-path)
                                (get-code event.src-path)]))]

   [on-deleted
     (handler-method (valid? event.src-path)
                     (osc-send "/eye/delete"
                               [(get-name event.src-path)]))]

   [on-moved
     (handler-method (valid? event.dest-path)
                     (osc-send "/eye/move"
                               [(get-name event.src-path)
                                (get-name event.dest-path)]))]

   [on-modified
     (handler-method (valid? event.src-path)
                     (osc-send "/eye/code"
                               [(get-name event.src-path)
                                (get-code event.src-path)]))]])


(defmain [args]
  (.run (Coder)))
