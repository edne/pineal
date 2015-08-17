(osc-source amp  "/amp")
(osc-source bass "/bass")
(osc-source high "/high")


(stroke-weight 4)

(on my-layer

    (fx [(scale (+ 1 (amp)))]
        (draw my-layer))

    (fx [(scale (amp 4))]
        (pwired 4 [0 1 1 1])
        (psolid 4 [0 0 0 0.1]))

    (fx [(scale (bass 2))]
        (pwired 4 [0 1 0 1])
        (psolid 4 [0 0 0 0.1]))

    (fx [(scale (high 4))]
        (pwired 4 [1 1 1 1])
        (psolid 4 [0 0 0 0.1])))

(draw my-layer)
