(osc-source amp  "/amp")
(osc-source bass "/bass")
(osc-source high "/high")

(palette grey "kw")
;(palette hsv "rgbr")
(palette hsv "rgbr")
;(palette hsv "rgkgbkbr")

(palette pal "kywgkrcb")

(stroke-weight 2)


(on outer
    (on inner
        (fx [(scale 4)]
             (psolid 4 (grey 0.0 0.01)))

        ;(draw inner)

        (fx [(turnaround 7)
             (rotate (* (/ pi 2) (amp 4)))
             (translate (high 10))
             (scale (bass 3))
             ;(turnaround 4)
             (rotate (time-rad 0.1))
             ;(translate (amp 1 ))
             (rotate (/ pi 2))
             ]
            ;(psolid 6 (pal (time 0.6) 0.2))
            (pwired 3 (pal (time 0.5)))
            (fx [
                 ;(scale (sqrt 2))
                 (scale 1)
                 (rotate (/ pi 4))]
                (draw inner))
            )
        )

    (fx [(rotate (time-rad 0))
         (scale (bass 1 (sqrt 2)))
         ]
        (draw inner))

    )

(draw outer)
