(import
  [pineal.windows [new-renderer new-master new-overview]]
  [pineal.lang [pineal-eval]]
  [pineal.osc :as osc]
  [pyglet]
  [logging]
  [threading [Thread]])


(def log (logging.getLogger --name--))


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
    (osc.add-callback "/eye/code"
                      (fn [path [code]] (vision code))))

  (osc.start-server)
  (.schedule_interval pyglet.clock
                      (fn [dt] nil)
                      (/ 1 120))
  (.run pyglet.app))


(defn new-vision [code]
  ; stack here the loaded codes,
  ; so when everything explodes, we can
  ; always restore the last (hopefully) working vision
  (setv stack ["" code])
  (setv namespace {"draw" (fn [])})

  (defn eval-code [code]
    (log.info "evaluating code")
    (if code (pineal-eval code namespace)))

  (defn load [code]
    (log.info "loading vision")
    (eval-code code)
    (.append stack code))

  (defn draw []
    (if-not (get namespace "draw")
      (eval-code (last stack)))
    ((get namespace "draw"))
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
