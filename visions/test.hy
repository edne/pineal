(osc-source amp  "/amp")
(osc-source bass "/bass")
(osc-source high "/high")

(palette grey "kw")
(palette hsv "rgbr")

(stroke-weight 4)

(on my-layer
    (fx [(scale 4)]
        (psolid 4 "k"))

    (fx [(scale (bass 4 0.0))]
        (psolid 4 (grey 0 0.1))
        (pwired 4 (hsv (time 0.1)))
        )
    )

(draw my-layer)
