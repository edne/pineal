(osc-source amp  "/amp")
(osc-source bass "/bass")
(osc-source high "/high")


(stroke-weight 4)

(on my-layer
    (fx [(scale (amp 1 1))]
        (draw my-layer))

    (fx [(scale (amp 4))]
        (pwired 4 (rgb  0 1 1))
        (psolid 4 (rgba 0 0 0 0.1)))

    (fx [(scale (bass 2))]
        (pwired 4 (rgb  0 1 0))
        (psolid 4 (rgba 0 0 0 0.1)))

    (fx [(scale (high 4))]
        (pwired 4 (rgb  1 1 1))
        (psolid 4 (rgba 0 0 0 0.1))))

(draw my-layer)
