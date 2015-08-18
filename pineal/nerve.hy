(import
  [pineal [conf]]
  [pineal.osc [osc-receiver
               osc-sender]])

(def nerve-cbs {})  ; visible from eye

(setv nerve-start (osc-receiver conf.OSC_EYE
                                nerve-cbs))

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
