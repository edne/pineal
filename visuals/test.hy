(import [lib.graphic [Polygon]]
        [time [time]]
        [math [sin]])

(audio amp "AMP")

(setv p (Polygon 3))
(setv p.side (fn [] (+ (amp) 1)))

(entities [p])
