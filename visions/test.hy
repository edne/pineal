(osc-source amp "/amp")


(stroke-weight 4)

(on my-layer
    (fx [(scale (amp 4))]
        (pwired 4 [0 1 1 1])
        (psolid 4 [0 0 0 0.1]))
    (fx [(scale 1.1)
         (rotate (time2rad 0.0))]
        (draw my-layer)))

(draw my-layer)
