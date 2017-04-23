(def amp  (osc-in "/amp"))
(def bass (osc-in "/bass"))
(def high (osc-in "/high"))

(def grey (palette "kw"))
(def hsv (palette "rgbr"))

(stroke-weight 4)

(on-layer "master"
          (fn []
            (fx [(scale 4)]
                ((psolid 4 (grey 0 0.01))))

            (fx [(scale (bass 8 0.8))
                 (rotate (/ pi 6))]
                ((pwired 3 (hsv (amp 4))))
                (fx [(scale (bass 1 0.8))
                     (rotate (/ pi 4))
                     ]
                    (draw "master")))) )

(draw "master")
