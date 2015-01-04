(import [lib.graphic [polygon]]
        [lib.audio :as audio]
        [time [time]]
        [math [sin]])


(setv amp (audio.source "AMP"))
(setv pol (polygon 4))


(defn draw []
  (setv pol.side (* 16 (amp)))
  (.draw pol))
