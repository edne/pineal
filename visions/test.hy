(osc-source amp "/amp")
(osc-source r   "/r/amp")
(osc-source l   "/l/amp")


(stroke-weight 4)

(on my-layer
    (fx scale [(amp 8)]
        (pwired 4 [0 1 1 1])
        (psolid 4 [0 0 0 0.1])
        (fx scale [(amp 4)]
            (draw my-layer))))

(draw my-layer)
