(stroke-weight 4)

(effect on-layer ["main"]
        (effect scale [(* 8 (amp))]
                (pwired 4 [0 1 1 1])
                (psolid 4 [0 0 0 0.1])
                (effect scale [(* 4 (amp))]
                        (draw-layer "main"))
                ))

(draw-layer "main")
