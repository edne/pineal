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

(defmacro osc-send [path data]
  `(.send self.osc ~path ~data OSC_EYE))


(defn valid? [path] (.endswith path ".py"))


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

         (setv path "visions")
         (setv self.osc (Osc))
         (.sender self.osc OSC_EYE)

         (for [filename (glob (+ path "/*"))]
              (when (valid? filename)
                (osc-send "/eye/code"
                          [(get-name filename)
                           (get-code filename)])))

         (setv handler (Handler))
         (setv handler.osc self.osc)

         (setv observer (Observer))
         (.schedule observer handler path false)
         (.start observer)

         (running (sleep (/ 1 60)))
         (print "\rstopping coder.hy")

         (.stop observer)
         (.join observer))]])


;-- HANDLER

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


(defclass Handler [FileSystemEventHandler]
  [[on-created  (handle (valid-src?)
                        "/eye/code" [(src-name) (src-code)])]

   [on-deleted  (handle (valid-src?)
                        "/eye/delete" [(src-name)])]

   [on-moved    (handle (valid-dest?)
                        "/eye/move" [(src-name) (dest-name)])]

   [on-modified (handle (valid-src?)
                        "/eye/code" [(src-name) (src-code)])]])


(defmain [args]
  (.run (Coder)))
