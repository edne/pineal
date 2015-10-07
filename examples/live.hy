(osc-source amp  "/amp")
(osc-source bass "/bass")
(osc-source high "/high")

(palette grey "kw")
;(palette hsv "rgbr")
(palette hsv "rgbr")
;(palette hsv "rgkgbkbr")
(palette pal "crbkyg")

(stroke-weight 4)




(on outer
    (fx [(scale (amp 1 1.1))]
        (draw inner)
        ;(draw outer)
        )

    (on inner
        (fx [(scale 2)]
            ;(psolid 4 (grey (time 1) (high 4 0.5)))
            (psolid 4 (grey 0 (high 4 0.5)))
            )




        (fx [(scale (bass 8 0.1))
             ;(rotate (time-rad 0.2))
             (turnaround 2)
             (rotate (time-rad 0.1 (bass 1 1)) 1 0 0)
             (turnaround 4)
             ;(rotate (time-rad -0))
             (translate (amp 8 1))
             (scale (bass 16 0.0))
             ;(rotate (time-rad -3))
             ]
            ;(psolid 4 (pal (time) (high 4 1)))
            (psolid 4 (grey (time) (high 4 2)))
            (pwired 4 (pal (time 3 (bass))))
            (fx [
                 (rotate (time-rad 0.1) 1 0 0)
                 (turnaround 2)
                 (scale (sqrt 2))
                 ;(scale (bass 1 1))
                 (scale 0.5)
                 ;(rotate (/ pi 4))
                 ;(rotate (time-rad -5))
                 ]
                (draw inner))
            )
        )

    (fx [;(rotate (time-rad 0))
         (scale (bass 1 (sqrt 2)))
         ;(scale (bass 0 (sqrt 2)))
         ]
        (draw inner))

    )

(on out2
    (fx [(scale (bass -1 1))]
        (draw outer)))

(draw out2)



'(on outer
     (on inner
         (fx [(scale 1)]
             (psolid 4 (grey 0.0 0.05)))

         ;(draw inner)

         (fx [(scale (bass 8 0.0))
              (turnaround 4)
              ;(rotate (time-rad -0))
              (translate (amp 8 (bass)))
              ]
             (psolid 4 (grey 1 0.1))
             (pwired 3 (hsv (time 0.2)))
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
