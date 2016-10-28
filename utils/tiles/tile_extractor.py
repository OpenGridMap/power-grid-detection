import os

from PIL import Image


def extract_image_from_tiles(coord, files_dir, zoom=18):
    res = 256
    xs = []
    ys = []
    tiles = coord.get_tiles(zoom)

    for tile in tiles:
        x, y = tile[0], tile[1]
        xs.append(x)
        ys.append(y)

    x_min = min(xs)
    y_min = min(ys)

    xs = [x - x_min for x in xs]
    ys = [y - y_min for y in ys]

    x_n = max(xs) + 1
    y_n = max(ys) + 1

    im = Image.new('RGB', (x_n * res, y_n * res))

    for i in range(x_n):
        for j in range(y_n):
            filename = "{}_{}_{}.jpg".format(i + x_min, j + y_min, zoom)
            file_path = os.path.join(files_dir, filename)

            if os.path.exists(file_path):
                tile_im = Image.open(file_path)
                im.paste(tile_im, (i * res, j * res))
            else:
                print('Image not found : %s' % file_path)

    im.show()

    bbox = coord.get_bbox()
    w_d = abs(bbox[0] - bbox[2])
    h_d = abs(bbox[1] - bbox[3])

    pitch_w = 2 * w_d / (res * 3)
    pitch_h = 2* h_d / (res * 3)

    deviation_x = (coord.longitude - ((bbox[0] + bbox[2]) / 2.)) / pitch_w
    deviation_y = (coord.latitude - ((bbox[1] + bbox[3]) / 2.)) / pitch_h

    print(deviation_x, deviation_y)

    img_cropped = Image.new('RGB', (res, res))
    crop = im.crop((res - deviation_x, res - deviation_y, 2 * res - deviation_x, 2 * res - deviation_y))
    # crop = im.crop((res, res, 2 * res, 2 * res))
    img_cropped.paste(crop)

    img_cropped.show()
