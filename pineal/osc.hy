(import
  [liblo]
  [atomos.atomic [AtomicFloat]]
  [config])


(def callbacks {})
(def sources {})


(defn dispatcher [path args tags]
  (for [k (.keys callbacks)]
    (if (.startswith path k)
      ((get callbacks k) path args))))


(defn osc-receiver []
  (setv server (liblo.ServerThread (second config.OSC-EYE)))
  (.add-method server nil nil dispatcher)

  server.start)

(setv start-server (osc-receiver))


(defn add-callback [key cb]
  (assoc callbacks key cb))


(defn get-source [name]
  (unless (in name sources)
    (setv container (AtomicFloat))

    (add-callback name
                  (fn [path [value]]
                    (.set container value)))

    (assoc sources name container.get))

  (get sources name))
