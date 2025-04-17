import numpy as np
import PIL

class img_proc:
    # Courtesy of Wikipedia: convert brightness to hue/saturation
    perception_matrix = np.array([[0.2126, 0.7512, 0.0722],
                                  [1.0, -0.5, -0.5],
                                  [0.0, np.sqrt(3)/2, -np.sqrt(3)/2]])

    @staticmethod
    def chroma (rgb):
        """Compute luma and chrome from rgb values
        """
        r, c, b = rgb.shape
        assert b == 3
        ret = np.reshape(rgb, (r*c, b))
        ret = perception_matrix @ ret
        return np.reshape(ret, (r, c, b))

    def rgb (chroma):
        """Compute luma and chrome from rgb values
        """
        r, c, b = chroma.shape
        assert b == 3
        mat = np.linalg.inv(perception_matrix)
        ret = np.reshape(chroma, (r*c, b))
        ret = mat @ ret
        return np.reshape(ret, (r, c, b))
