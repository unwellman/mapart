from mapart import *
from PIL import Image as img
import sys
import os

COLOR_TABLE_FP = "res/map_colors_1.21.csv"

def main():
    # Basic, basic single argument usage
    fp = sys.argv[1]
    assert os.path.isfile(fp)
    name = os.path.splitext(os.path.basename(fp))[0]
    palette = Palette(COLOR_TABLE_FP, mode="stairs")
    weights = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    luma_weights = [0.1, 0.5, 1.0, 2.0, 10.0]
    for w in weights:
        for l in luma_weights:
            art = Mapart(fp, scheme="dither", dither_weight=w)
            art.rgb = chroma(art.rgb)
            art.rgb[:, :, 0] *= l
            img.fromarray(art.rgb.astype(np.uint8)).save("tmp/wtf.jpg")
            colors = chroma(palette.colors)
            colors[:, 0] *= l
            _, idx = art.generate(colors)
            im = palette.get_image_index(idx)
            out_fp = f"tmp/{name}_fs{w}_lc{l}.jpg"
            im.save(out_fp)
            print(f"Wrote {out_fp}")

if __name__ == "__main__":
    main()

