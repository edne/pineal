#!/usr/bin/env hy

(require core.macros)

; update impure config
(let [[conf (get-config)]]
  (import [core [conf :as impure-conf]])
  (setv impure-conf.RENDER-SIZE conf.RENDER-SIZE)
  (setv impure-conf.OSC-EYE     conf.OSC-EYE))

(import
  [core.windows [new-renderer new-master new-overview]]
  [core.nerve [nerve-cb! nerve-start]])


(runner Eye [conf log]
        "
        Handles and draws the different visions

        Recives from Coder:
        * `/eye/code    [filename code]`
        * `/eye/delete  [filename]` (not yet implemented)
        * `/eye/move    [oldname newname]`

        Recives from Ear:
        * `/eye/audio/[cmd]  [value]`
        "
        (log.info "starting eye.hy")

        (setv visions {})

        (setv renderer (new-renderer visions
                                     conf.RENDER-SIZE))
        (new-master renderer)
        (new-overview renderer)

        (nerve-cb! "/eye/code"
                   (fn [path args]
                     (setv [name code] args)
                     (if (in name (visions.keys))
                       (.load (get visions name)
                              code)
                       (assoc visions
                         name
                         (new-vision name code)))))

        (setv nerve-stop (nerve-start))

        (import [pyglet])
        (.schedule_interval pyglet.clock
                            (fn [dt]
                              (when (stopped?)
                                (.exit pyglet.app)))
                            (/ 1 120))
        (try
          (.run pyglet.app)
          (catch [KeyboardInterrupt]
            None))

        (log.info "stopping eye.hy")
        (nerve-stop))


(defn new-vision [path code]
  (setv name
    (get (.split path "/") -1))

  (setv log (new-logger))  ; TODO pass name

  ; stack here the loaded codes,
  ; so when everything explodes, we can
  ; always restore the last (opefully) working vision
  (setv stack [])

  (defclass Box []
    "A small sandbox where to run the livecoded part"
    [[draw
      (fn [self])]])

  (setv box (Box))

  (defclass Vision []
    "
    The vision instance
    "
    [[load
      (fn [self code]
        (log.info (% "loading: %s" name))
        (import [core.pyexec [pyexec]])
        (try
          (pyexec code box.__dict__)
          (except [e Exception]
            (log.error (+ name " "
                          (str e))))
          (else
            (.append stack code))))]

     [iteration
      (fn [self]
        (try
          (.draw box)
          ; if there is an error and stack is empty
          ; the FIRST loaded vision is broken
          (except [e Exception]
            (log.error (+ name " "
                          (str e)))
            (.pop stack)

            (if stack
              (.load self (get stack -1))
              (log.error "BROKEN!")))))]])

  (setv vision (Vision))
  (.load vision code)
  vision)


(defmain [args]
  (.run (Eye)))
