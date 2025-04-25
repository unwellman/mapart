import numpy as np
import PIL

# Courtesy of Wikipedia: convert rgb to brightness/hue/saturation
perception_matrix = np.array([[0.299, 0.587, 0.114],
                              [1.0, -0.5, -0.5],
                              [0.0, np.sqrt(3)/2, -np.sqrt(3)/2]])
perception_matrix_inv = np.linalg.inv(perception_matrix)

def nearest (color, palette, norm="lstsq"):
    """ Return the value and index of the nearest color in palette to color
    """
    color = np.asarray(color)
    palette = np.asarray(palette)
    assert norm in ["lstsq", "sam"]
    if norm == "lstsq":
        norms = np.linalg.norm(palette - color, axis=1)
        i = np.argmin(norms)
        return palette[i], i
    if norm == "sam":
        palette_norm = palette / np.linalg.norm(palette, axis=1)
        color_norm = color / np.linalg.norm(color)
        cosines = color_norm.T @ palette_norm
        i = np.argmin(np.acos(cosines))
        return palette[i], i
        
def chroma (rgb, axis=-1):
    """ Convert an array of rgb vectors to luma and chroma vectors
    """
    rgb = np.asarray(rgb)
    if np.ndim(rgb) < 2:
        return perception_matrix @ rgb
    shp = rgb.shape
    assert shp[-1] == 3
    ret = np.reshape(rgb, (np.prod(shp[0:-1]), 3))
    ret = perception_matrix @ ret.T
    return np.reshape(ret.T, shp)

def rgb (chroma):
    """Compute rgb from luma and chroma values
    """
    rgb = np.asarray(chroma)
    if np.ndim(rgb) < 2:
        return perception_matrix_inv @ rgb
    shp = rgb.shape
    assert shp[-1] == 3
    ret = np.reshape(rgb, (np.prod(shp[0:-1]), 3))
    ret = perception_matrix_inv @ ret.T
    return np.reshape(ret.T, shp)
