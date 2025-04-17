import PIL
from PIL import Image as img
import numpy as np

class Mapart:
    """ Methods specific to 
    """
    
    def __init__ (self, fp):
        """ Initializer
        Load image with PIL and store with numpy array
        """
        with img.open(fp) as im:
            self.rgb = np.asarray(im)


