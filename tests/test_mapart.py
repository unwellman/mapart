from mapart import Mapart, Palette
import numpy as np

def test_palette_blocks ():
    palette = Palette("res/map_colors_1.21.csv")

    # Test case to check proper string splitting, verified for 1.21 color data
    test_str = "birch (planks, log (vertical), stripped log, wood, stripped wood, sign, pressure plate, trapdoor, stairs, slab, fence gate, fence, door)"
    assert palette.frame["Blocks"][2][2] == test_str

def test_palette_rgb ():
    palette = Palette("res/map_colors_1.21.csv")
    assert np.allclose(palette.frame["RGB"][1], [127, 178, 56])



