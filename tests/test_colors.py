from tools.colors import from_palette

def test_palette():
    pal = [[0, 0, 1, 1],
           [1, 0, 1, 0.5]]
    result = from_palette(pal, 0.5)
    print(result)
    assert result == [0.5, 0, 1, 0.75]
