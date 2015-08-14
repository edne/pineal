(osc-source amp "/eye/audio/amp")


(stroke-weight 4)

(on my-layer
    (fx scale [(amp 8)]
        (pwired 4 [0 1 1 1])
        (psolid 4 [0 0 0 0.1])
        (fx scale [(amp 4)]
            (draw my-layer))))

(draw my-layer)
