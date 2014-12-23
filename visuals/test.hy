(import [lib.graphic [Square]])
(import [time [time]])
(import [math [sin]])

(audio amp "AMP")

(setv square (Square))
;(setv square.side (fn [] (-> (time) sin)))
(setv square.side amp)
;(setv square.side (fn [] (* (bass) 2)))  ; if I want apply sometying (USE A MACRO!)

;(def __entities__ [square])
(entities [square])
