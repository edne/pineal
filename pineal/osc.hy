(import
  [config :as conf]
  [liblo])


(def callbacks {})
(def sources {})


(defn dispatcher [path args tags]
  (for [k (.keys callbacks)]
    (if (.startswith path k)
      ((get callbacks k) path args))))


(defn osc-receiver []
  (setv server (liblo.ServerThread (second conf.OSC-EYE)))
  (.add-method server nil nil dispatcher)

  server.start)

(setv start-server (osc-receiver))


(defn add-callback [key cb]
  (assoc callbacks key cb))


(defn get-source [name]
  (unless (in name sources)
    (setv container [0])

    (add-callback name
                  (fn [path args]
                    (setv [(car container)] args)))

    (assoc sources
      name (fn [] (car container))))

  (get sources name))
