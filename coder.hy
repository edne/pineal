#!/usr/bin/env hy

(import
  [glob [glob]]
  [time [sleep]]
  [watchdog.observers [Observer]]
  [watchdog.events [FileSystemEventHandler]]
  [config [OSC_EYE]]
  [core.osc [osc-sender]])

(require core.runner)


(runner Coder [self]
        "
        Waits for changes in `visions/`

        Sends to Eye:
        * `/eye/code    [filename code]`
        * `/eye/delete  [filename]`
        * `/eye/move    [oldname newname]`
        "
        (print "starting coder.hy")

        (setv observer (Observer))
        (.schedule observer (new-handler) "visions" false)
        (.start observer)

        (running (sleep (/ 1 60)))
        (print "\rstopping coder.hy")

        (.stop observer)
        (.join observer))


(defmacro last [l]
  `(get ~l -1))


(defn valid? [path] (.endswith path ".py"))


(defmacro handle [check path data]
  `(fn [self event]
     (when ~check (osc-send ~path ~data))))


(defn get-code [filename]
  (with [[f (open filename)]]
    (.read f)))


(defn get-name [filename]
  (-> filename
    .lower
    (.split "/") last
    (.split ".") first))


(defmacro valid-src?  [] '(valid? event.src-path))
(defmacro valid-dest? [] '(valid? event.dest-path))

(defmacro src-name    [] '(get-name event.src-path))
(defmacro src-code    [] '(get-code event.src-path))
(defmacro dest-name   [] '(get-name event.dest-path))


(defn new-handler []
  (setv osc-send (osc-sender OSC_EYE))

  (for [filename (glob "visions/*")]
    (when (valid? filename)
      (osc-send "/eye/code"
                [(get-name filename)
                 (get-code filename)])))

  ; is inside the scope where defined osc
  (defclass Handler [FileSystemEventHandler]
    [[on-created  (handle (valid-src?)
                          "/eye/code" [(src-name) (src-code)])]

     [on-deleted  (handle (valid-src?)
                          "/eye/delete" [(src-name)])]

     [on-moved    (handle (valid-dest?)
                          "/eye/move" [(src-name) (dest-name)])]

     [on-modified (handle (valid-src?)
                          "/eye/code" [(src-name) (src-code)])]])
  (Handler))


(defmain [args]
  (.run (Coder)))
