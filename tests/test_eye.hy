(require core.macros)
(require eye)


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
