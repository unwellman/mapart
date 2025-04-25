import PIL
from PIL import Image as img
import numpy as np
import pandas as pd

from mapart import img_proc

class Mapart:
    """ Methods specific to Minecraft map art
    """
    
    def __init__ (self, fp, scheme="dither", dither_weight=1.0, luma_weight=None):
        """ Initializer
        Load image with PIL and store with numpy array
        """
        assert scheme in ["direct", "dither"]
        self.scheme = scheme
        self.dither_weight = dither_weight
        with img.open(fp) as im:
            self.rgb = np.array(im, dtype="float64")

    def generate (self, palette):
        """ Generate a map art based on the state of the object
        """
        if self.scheme == "dither":
            rows, cols, b = self.rgb.shape
            self._rgb = np.zeros((rows+1, cols+2, b), dtype="float64")
            self._rgb[0:rows, 1:cols+1] = self.rgb
            ret = np.zeros_like(self.rgb)
            idx = np.empty((rows, cols), dtype=np.int32)
            for r in range(rows):
                for c in range(1, cols+1):
                    nearest, i = img_proc.nearest(self._rgb[r, c, :], palette)
                    ret[r, c-1] = nearest
                    idx[r, c-1] = i
                    self.__dither(r, c, nearest)
        else: # self.scheme == "direct"
            self._rgb = np.copy(self.rgb)
            ret = np.zeros_like(self._rgb)
            rows, cols, b = self._rgb.shape
            idx = np.empty((rows, cols), dtype=np.int32)
            for r in range(rows):
                for c in range(cols):
                    nearest, i = img_proc.nearest(self._rgb[r, c, :], palette)
                    ret[r, c] = nearest
                    idx[r, c] = i
        return ret.astype(np.uint8), idx

    def __dither (self, r, c, nearest):
        err = self._rgb[r, c, :] - nearest
        err *= self.dither_weight
        self._rgb[r    , c + 1, :] += 7/16*err;
        self._rgb[r + 1, c - 1, :] += 3/16*err;
        self._rgb[r + 1, c    , :] += 5/16*err;
        self._rgb[r + 1, c + 1, :] += 1/16*err;


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

    def get_image_index (self, idx):
        """ Turn an np.array of indices into a PIL image
        """
        assert idx.ndim == 2
        ret = np.empty((*(idx.shape), 3), dtype="float64")
        for r in range(idx.shape[0]):
            for c in range(idx.shape[1]):
                ret[r, c, :] = self.colors[idx[r, c]]
        return img.fromarray(ret.astype(np.uint8))

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


