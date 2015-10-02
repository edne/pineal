(osc-source amp  "/amp")
(osc-source bass "/bass")
(osc-source high "/high")

(palette grey "kw")
(palette hsv "rgbr")

(stroke-weight 4)

(on layer
    (fx [(scale 4)]
        (psolid 4 (grey 0 0.01)))

    '(fx [(scale (bass 8 0.6))]
         (psolid 4 (grey 0 0.1))
         (pwired 4 (hsv (amp 4)))
         (fx [(scale (bass 1 0.99))]
             (draw layer)))

    (fx [(scale (bass 8 0.8))
         (rotate (/ pi 6))]
        (pwired 3 (hsv (amp 4)))
        (fx [(scale (bass 1 0.8))
             (rotate (/ pi 4))
             ]
            (draw layer))
        )
    )

(draw layer)
