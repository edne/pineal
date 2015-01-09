(import [lib.graphic [Polygon]]
        [lib.audio :as audio])


(setv amp (audio.source "AMP"))
(setv pol (Polygon 4))


(defn draw []
  (setv pol.fill [1 1 1 0.5])
  (.draw pol))
