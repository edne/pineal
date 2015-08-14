(osc-source amp "/amp")


(stroke-weight 4)

(on my-layer
    (fx [(rotate (time2rad))
         (turnaround 4)
         (translate (+ 0.0 (amp 4)))
         (scale (amp 8))
         (rotate (time2rad -1))]

        (pwired 4 [0 1 1 1])
        (psolid 4 [0 0 0 0.5])

        (fx [(scale 0.8)]
            (draw my-layer))
        ))

(draw my-layer)
