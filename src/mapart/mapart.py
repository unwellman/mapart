import PIL
from PIL import Image as img
import numpy as np
import pandas as pd

from mapart import img_proc

class Mapart:
    """ Methods specific to Minecraft map art
    """
    
    def __init__ (self, fp):
        """ Initializer
        Load image with PIL and store with numpy array
        """
        with img.open(fp) as im:
            self.rgb = np.asarray(im)
        self.lc = img_proc.chroma(self.rgb)

class Palette:
    """ Contain Minecraft block palette info including block names, slopes, and
    their respective colors
    """
    def __init__ (self, fp):
        """ fp: a CSV containing block color data (courtesy of minecraft.wiki)
        """
        frm = pd.read_csv(fp, sep=',', encoding='utf8')
        assert tuple(frm.keys()) == ("ID", "Color", "RGB", "Blocks")
        frm = frm.drop(0) # Delete transparent line
        self.frame = self.__format_frame(frm)

    def __format_frame (self, frame):
        frame.pop("Color") # Empty column

        rgb = [list(map(float, color.split(','))) for color in frame.pop("RGB")]
        frame.insert(1, "RGB", rgb)

        block_lists = [self.__split_blocks(s) for s in frame.pop("Blocks")]
        frame.insert(2, "Blocks", block_lists)

        return frame

    @staticmethod
    def __split_blocks (blocks, sep=', '):
        starts = [0]
        open_paren = 0
        for i, c in enumerate(blocks):
            if c == '(':
                open_paren += 1
            elif c == ')':
                open_paren -= 1
            if open_paren == 0 and blocks[i:].startswith(sep):
                starts.append(i)
            assert open_paren >= 0

        starts.append(len(blocks))
        return [blocks[i:j].strip(sep) for i, j in zip(starts, starts[1:])]


