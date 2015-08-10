(require core.macros)
(require eye)


(defn test-vision []
  (import [eye [new-vision]])
  (setv vision (new-vision "tested-vision" "failing code"))
  (assert (= (vision) :broken))
  (assert (= (vision) :working))
  (assert (= (vision) :working)))


(defn test-empty-eye []
  (import
    [core.windows [new-renderer new-master new-overview]])

  (runner Eye [conf log]
          (setv renderer (new-renderer {}
                                       conf.RENDER-SIZE))
          (new-master renderer)
          (new-overview renderer)

          (eye-loop 120))

  (let [[eye (Eye)]]
    (import [time [sleep]])
    (.start eye)
    (sleep 1)
    (.stop eye)))
