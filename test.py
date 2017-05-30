from pineal.lang import polygon, scale, apply_effect


p = polygon(4, [1, 1, 1])
p = apply_effect(p, scale, 0.5)
p.draw()
