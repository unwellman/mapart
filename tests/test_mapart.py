from mapart import Mapart, Palette
import numpy as np
from PIL import Image as img

COLOR_TABLE_FP = "res/map_colors_1.21.csv"

def test_palette_blocks ():
    palette = Palette(COLOR_TABLE_FP)

    # Test case to check proper string splitting, verified for 1.21 color data
    test_str = "birch (planks, log (vertical), stripped log, wood, stripped wood, sign, pressure plate, trapdoor, stairs, slab, fence gate, fence, door)"
    assert palette.frame["Blocks"][2][2] == test_str

def test_palette_rgb ():
    palette = Palette(COLOR_TABLE_FP)
    assert np.allclose(palette.frame["RGB"][1], [127, 178, 56])

def test_palette_shades_stairs ():
    palette = Palette(COLOR_TABLE_FP, mode="stairs")
    assert palette.colors.shape == (61*3, 3)
    assert np.allclose(palette.ids[0:4], np.array([4, 5, 6, 8]))
    assert np.allclose(palette.colors[1], 220/255*np.array([127, 178, 56]))

def test_palette_shades_flat ():
    palette = Palette(COLOR_TABLE_FP, mode="flat")
    assert palette.colors.shape == (61, 3)
    assert palette.ids[3] == 17
    assert np.allclose(palette.colors[1], 220/255*np.array([247, 233, 163]))

def test_palette_shades_tool ():
    palette = Palette(COLOR_TABLE_FP, mode="tool")
    assert palette.colors.shape == (61*4, 3)
    assert np.allclose(palette.ids[0:4], np.array([4, 5, 6, 7]))
    assert np.allclose(palette.colors[1], 220/255*np.array([127, 178, 56]))

def test_direct ():
    palette = Palette(COLOR_TABLE_FP, mode="tool")
    art = Mapart("res/nozomap128.jpg", scheme="direct")
    im = art.generate(palette.colors)
    im[255]
    im = img.fromarray(np.floor(im/255))
    im.save("tmp/nozotest.jpg")


