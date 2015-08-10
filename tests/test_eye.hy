(require core.macros)
(require eye)


(defn test-broken-vision []
  (import [eye [new-vision]])
  (setv vision (new-vision "asd" "failing code"))
  (try
      (vision)
    (except [Exception]
      (assert true))
    (else (assert false)))) 


(defn test-empty-eye []
  (import
    [core.windows [new-renderer new-master new-overview]])

  (runner eye [conf log]
          (setv renderer (new-renderer {}
                                       conf.RENDER-SIZE))
          (new-master renderer)
          (new-overview renderer)

          (eye-loop 120))

  (.run (eye)))
