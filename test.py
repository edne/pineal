from pineal.core import polygon, layer, on_layer

with on_layer('master'):
    polygon(4, [0, 0, 0]).scale(4).draw()  # TODO: clean_layer() primitive

    polygon(4, [1, 1, 1], fill=False).draw()
    layer('master').scale(0.5).draw()

layer('master').draw()
