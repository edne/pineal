(import
  [pineal [conf]]
  [liblo])

(require pineal.macros)


(def nerve-cbs {})  ; visible from eye


(defn osc-receiver []

  (defn callback [path args tags]
    (for [k (.keys nerve-cbs)]
      (if (.startswith path k)
        ((get nerve-cbs k) path args))))

  (setv server (liblo.ServerThread (second conf.OSC-EYE)))
  (.add-method server nil nil callback)

  server.start)

(setv nerve-start (osc-receiver))

(defn nerve-cb! [key cb]
  (assoc nerve-cbs key cb))


(def memo-source {})

(defn get-source [name]
  (unless (in name memo-source)
    (setv container [0])

    (nerve-cb! name
               (fn [path args]
                 (setv [(car container)] args)))

    (assoc memo-source
      name (fn [] (car container))))

  (get memo-source name))
