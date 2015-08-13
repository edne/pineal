(stroke-weight 4)

(on main
    (fx scale [(* 8 (amp))]
        (pwired 4 [0 1 1 1])
        (psolid 4 [0 0 0 0.1])
        (fx scale [(* 4 (amp))]
            (draw main))))

(draw main)
