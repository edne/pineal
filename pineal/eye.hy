(import
  [pineal.windows [new-renderer new-master new-overview]]
  [pineal.nerve [nerve-cb! nerve-start]]
  [pyglet]
  [logging]
  [threading [Thread]])


(def log (logging.getLogger --name--))


(defn eval-str [s namespace]
  (import
    [hy.lex [tokenize]]
    [hy.importer [hy-eval]])
  (hy-eval `(do ~@(tokenize s)) namespace --name--))


(defn eye []
  "
  Handles and draws the vision
  "
  (log.info "starting eye.hy")

  (let [[vision   (new-vision "")]
        [renderer (new-renderer vision
                                [800 800])]]
    (new-master   renderer)
    (new-overview renderer)
    (nerve-cb! "/eye/code"
               (fn [path [code]] (vision code))))

  (nerve-start)
  (.schedule_interval pyglet.clock
                      (fn [dt] nil)
                      (/ 1 120))
  (.run pyglet.app))


(defn new-vision [code]
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
