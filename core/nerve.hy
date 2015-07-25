(import
  [core [conf]]
  [core.osc [osc-receiver
             osc-sender]])

(def nerve-cbs {})  ; visible from eye

(setv nerve-start (osc-receiver conf.OSC_EYE
                                nerve-cbs))

(defn nerve-cb! [key cb]
  (assoc nerve-cbs key cb))
