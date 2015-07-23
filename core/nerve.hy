(import
  [config [OSC_EAR OSC_EYE]]
  [core.osc [osc-receiver
             osc-sender]])

(def nerve-cbs {})  ; visible from eye

(setv nerve-start (osc-receiver OSC_EYE
                                nerve-cbs))

(def nerve-send
  (osc-sender OSC_EAR))

(defn nerve-cb! [key cb]
  (assoc nerve-cbs key cb))
