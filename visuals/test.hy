(import [lib.graphic [polygon]]
        [lib.audio :as audio]
        [lib.osc :as osc]
        [time [time]]
        [math [sin]])


(setv amp (audio.source "AMP"))
(setv osc1 (osc.source "/test/value"))
(setv pol (polygon 4))


(defn draw []
  (setv pol.side (+ 0.5 (* 16 (amp))))
  (.draw pol))
