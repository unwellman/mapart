import numpy as np
from PIL import Image as img
from mapart import img_proc

def test_chroma ():
    test = np.array([[255.0, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 255.0]])
    exp = np.array([76.245, 255, 0])
    assert np.allclose(img_proc.chroma(test)[0], exp)
    assert np.allclose(img_proc.chroma(test)[3], [255.0, 0, 0])

def test_rgb ():
    test = np.array([76.245, 255.0, 0.0])
    exp = np.array([255.0, 0, 0])
    assert np.allclose(img_proc.rgb(test), exp)

def test_chroma_rgb ():
    with img.open("res/nozomap128.jpg") as im:
        rgb = np.asarray(im)
    assert np.allclose(rgb, img_proc.rgb(img_proc.chroma(rgb)))
