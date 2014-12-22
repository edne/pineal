(import [lib.graphic [Square]])
(import [time [time]])
(import [math [sin]])

(setv square (Square))
(setv square.side (fn [] (-> (time) sin)))

;(def __entities__ [square])
(entities [square])
