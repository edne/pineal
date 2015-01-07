(import [lib.graphic [Polygon]]
        [lib.audio :as audio]
        [lib.osc :as osc]
        [time [time]]
        [math [sin]])


(setv amp (audio.source "AMP"))
(setv osc1 (osc.source "/test/value"))
(setv pol (Polygon 4))
(setv tri (Polygon 3))


(defn draw []
  (setv tri.stroke [0 1 1 1])
  (setv tri.fill [1 1 1 0.5])
  (setv pol.r (+ 0.5 (* 16 (amp))))
  (setv pol.fill [0 1 0 (* 20 (amp))])
  (.draw tri)
  (.draw pol))
