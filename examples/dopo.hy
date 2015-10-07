(osc-source amp  "/amp")
(osc-source bass "/bass")
(osc-source high "/high")
(import [random [gauss]])

(palette grey "kw")
;(palette hsv "rgbr")
(palette hsv "rgbr")
;(palette hsv "rgkgbkbr")
(palette pal "kw")

;(palette pal "kbywkcg")
(palette pal "kbgyk")

(stroke-weight 2)


(on inner
    (fx [(scale 2)]
        (psolid 4 (grey 0 (high))))

    '(fx [(scale (bass 16))]
        (pwired 4 "b"))

    '(fx [(scale (high 4 1.1))
         (rotate (time-rad 0.1))
         (scale (amp 8))
         ]
        (draw inner))

    (fx [(scale (bass 2))
         (turnaround 3)
         (rotate (time-rad))
         (translate (amp 6 (gauss 1 0.1)))]
        (pwired 4 (pal (time)))
        '(fx [(scale (sqrt 2))
             (rotate (/ pi 4))]
            (draw inner)))

    '(fx [(rotate (time-rad 0))
         (scale (bass 2 (sqrt 2)))
         ]
        (draw inner))
    )

(fx [(scale 1)
     ;(rotate (time-rad 0.1))
     ;(rotate 0.3 0 1 0)
     (scale (high -1 (bass -4 1)))
     ]
    (draw inner))

(fx [(scale 1)
     ;(rotate (time-rad 0.1))
     ;(rotate 0.3 0 1 0)
     (scale (high -1 (bass 4 1)))
     ]
    (draw inner))


'(fx [(scale (high 4 1.1))
      ;(rotate (time-rad 0.1))
      (rotate 0.3 0 1 0)
      (translate 0 0 0.5)
      (scale (bass 8))
      ]
     (draw inner))



















'(on outer
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

'(draw outer)
