(require core.macros)
(require eye)


(defn test-vision []
  (import [eye [new-vision]])
  (setv vision (new-vision "tested-vision" "failing code"))
  (assert (= (vision) :broken))
  (assert (= (vision) :working))
  (assert (= (vision) :working)))


(defn test-eval-str []
  (import [eye [eval-str]])
  (assert (= (eval-str "1") 1))
  (assert (= (eval-str "(+ 1 2)") 3))
  (assert (= (eval-str "(setv x 1) (+ x 1)") 2)))


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
