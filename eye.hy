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


(defn eval-str [s]
  (import [hy.lex [tokenize]])
  (eval `(do ~@(tokenize s))))


(defmacro eye-loop [fps]
  `(do
     (import [pyglet])
     (.schedule_interval pyglet.clock
                         (fn [dt]
                           (when (stopped?)
                             (.exit pyglet.app)))
                         (/ 1 ~fps))
     (try
       (.run pyglet.app)
       (catch [KeyboardInterrupt]
         nil))) )


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
                       ((get visions name) code)
                       (assoc visions
                         name
                         (new-vision name code)))))

        (setv nerve-stop (nerve-start))

        (eye-loop 120)

        (log.info "stopping eye.hy")
        (nerve-stop))


(defn new-vision [name code]
  (setv log (new-logger))  ; TODO pass name

  ; stack here the loaded codes,
  ; so when everything explodes, we can
  ; always restore the last (hopefully) working vision
  (setv stack ["" code])

  (defn load [code]
    (log.info (% "loading: %s" name))
    (.append stack code))

  (defn draw []
    (try
      (do
        (eval-str (+ "(import [tools [*]])\n"
                     "(require core.dsl)\n\n"
                     (last stack)))
        :working)
      (except [e Exception]
        (log.error (+ name " " (str e)))
        (.pop stack)
        :broken)))

  (fn [&optional code]
    (if code (load code) (draw))))


(defmain [args]
  (.run (Eye)))
