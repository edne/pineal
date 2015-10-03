(require pineal.macros)

; update impure config
(let [[conf (get-config)]]
  (import [pineal [conf :as impure-conf]])
  (setv impure-conf.RENDER-SIZE conf.RENDER-SIZE)
  (setv impure-conf.OSC-EYE     conf.OSC-EYE))

(import
  [pineal.windows [new-renderer new-master new-overview]]
  [pineal.nerve [nerve-cb! nerve-start]])


(defn eval-str [s namespace]
  (import
    [hy.lex [tokenize]]
    [hy.importer [hy-eval]])
  (hy-eval `(do ~@(tokenize s)) namespace --name--))


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


(runner eye-runner [conf log]
        "
        Handles and draws the vision
        "
        (log.info "starting eye.hy")

        (let [[vision   (new-vision "")]
              [renderer (new-renderer vision
                                      conf.RENDER-SIZE)]]
          (new-master   renderer)
          (new-overview renderer)
          (nerve-cb! "/eye/code"
                     (fn [path [code]] (vision code))))

        (setv nerve-stop (nerve-start))

        (eye-loop 120)

        (log.info "stopping eye.hy")
        (nerve-stop))


(defn new-vision [code]
  (setv log (new-logger))

  ; stack here the loaded codes,
  ; so when everything explodes, we can
  ; always restore the last (hopefully) working vision
  (setv stack ["" code])
  (setv namespace {"box_draw" nil})

  (defn eval-code [code]
    (log.info "evaluating code")
    (eval-str (+ "(import [tools [*]])"
                "(require pineal.dsl)"
                "(defn box-draw []"
                code
                ")")
              namespace))

  (defn load [code]
    (log.info "loading vision")
    (eval-code code)
    (.append stack code))

  (defn draw []
    (if-not (get namespace "box_draw")
      (eval-code (last stack)))
    ((get namespace "box_draw"))
    :working)

  (fn [&optional code]
    (try
      (if code (load code) (draw))
      (except [e Exception]
        (log.error (str e))
        (when stack
          (.pop stack)
          (eval-code (last stack)))
        :broken))))
