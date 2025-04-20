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
    def __init__ (self, fp, mode="tool"):
        """ Initialize the object and load the color palette
        Parameters:
            fp: a CSV containing block color data (courtesy of minecraft.wiki)
            mode: a string matching "stairs", "flat", or "tool", affecting how
            many shades can be accessed
        """
        assert mode in ["stairs", "flat", "tool"]
        frm = pd.read_csv(fp, sep=',', encoding='utf8')
        assert tuple(frm.keys()) == ("ID", "Color", "RGB", "Blocks")

        frm = frm.drop(0) # Delete transparent line

        self.frame = self.__format_frame(frm)
        self.ids, self.colors = self.__init_palette(mode)

    def __format_frame (self, frame):
        frame.pop("Color") # Empty column

        rgb = [list(map(float, color.split(','))) for color in frame.pop("RGB")]
        frame.insert(1, "RGB", rgb)

        block_lists = [self.__split_blocks(s) for s in frame.pop("Blocks")]
        frame.insert(2, "Blocks", block_lists)

        return frame

    def __init_palette (self, mode):
        """ Return Minecraft color ID's and RGB color palette

        Note that +1 is added to the ID's to accomodate the 4 transparent colors
        """
        # Weird hack to keep types in order
        base = np.array([list(row) for row in self.frame["RGB"]])
        r, c = base.shape

        if mode == "flat":
            ids = 4*np.arange(r) + 1
            return ids + 4, np.array(220.0/255.0*base)

        elif mode == "stairs":
            colors = np.empty((3*r, c))
            colors[0::3] = np.array(180.0/255.0*base)
            colors[1::3] = np.array(220.0/255.0*base)
            colors[2::3] = np.array(255.0/255.0*base)
            ids = np.empty(3*r, dtype="int64")
            ids[0::3] = 4*np.arange(r) + 0
            ids[1::3] = 4*np.arange(r) + 1
            ids[2::3] = 4*np.arange(r) + 2
            return ids + 4, colors

        else: # mode == "tool"
            num_shades = 4
            ids = np.arange(r*4, dtype="int64")
            colors = np.empty((4*r, c))
            colors[0::4] = np.array(180.0/255.0*base)
            colors[1::4] = np.array(220.0/255.0*base)
            colors[2::4] = np.array(255.0/255.0*base)
            colors[3::4] = np.array(135.0/255.0*base)
            return ids + 4, colors

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


