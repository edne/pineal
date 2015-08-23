(osc-source amp  "/amp")
(osc-source bass "/bass")
(osc-source high "/high")

(palette grey "bw")
(palette hsv "rygcbmr")

(stroke-weight 4)

(on my-layer

    (fx [(scale (amp 4 0.2))]
        (psolid 4 (hsv (time))))

    (fx [(scale (bass 2))]
        (psolid 4 "k")
        (psolid 4 (rgba 0 0 0 0.1)))

    (fx [(scale (high 4))]
        (psolid 4 "w"))

    (fx [(scale (amp 1 0.5))
         (rotate (/ pi 4))]
        (draw my-layer)))

(draw my-layer)
