(osc-source amp  "/amp")
(osc-source bass "/bass")
(osc-source high "/high")


(stroke-weight 4)

(on my-layer
    (fx [(scale (amp 1 1))]
        (draw my-layer))

    (fx [(scale (amp 4))]
        (pwired 4 "c")
        (psolid 4 (rgba 0 0 0 0.1)))

    (fx [(scale (bass 2))]
        (pwired 4 "g")
        (psolid 4 (rgba 0 0 0 0.1)))

    (fx [(scale (high 4))]
        (pwired 4 "w")
        (psolid 4 (rgba 0 0 0 0.1))))

(draw my-layer)
