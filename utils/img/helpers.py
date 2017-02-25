import os

import numpy as np
from PIL import Image
from shapely.geometry import Polygon, MultiPolygon

import config
from utils.dataset.annotations import annotations_iter, get_rect_from_annotation
from utils.geo.coordinate import Coordinate


def crop_rect(im_src, x, y, width, height, dest_path=None):
    try:
        box = get_coord_from_rect_box(x, y, width, height)
        im = Image.new(im_src.mode, (width, height))
        cropped_region = im_src.crop(box)
        im.paste(cropped_region, (0, 0))

        if dest_path is not None:
            if not os.path.exists(dest_path):
                im.save(dest_path, 'JPEG')
            else:
                print('%s already exists' % dest_path)
        return im
    except Exception as e:
        print(e)
        raise e


def get_coord_from_rect_box(x, y, width, height):
    return map(int, [x, y, x + width, y + height])


def get_polygon_from_rect_box(x, y, height, width):
    return Polygon([
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y + height)
    ])


def crop_annotated_region(im_src, annotation, path):
    x, y, width, height = get_rect_from_annotation(annotation)
    crop_rect(im_src, x, y, width, height, path)


def crop_negative_samples(im_src, annotations, samples_per_image, basename, samples_dir):
    boxes = [get_rect_from_annotation(annotation) for annotation in annotations_iter(annotations)]
    annotated_regions = get_multipolygon_from_boxes(boxes)

    z = int(basename.split('_')[-1])
    tiles_count = Coordinate.get_tiles_count(z)
    n_samples = 0

    # width, height = boxes[0][-2:]
    width, height = 140, 140

    while True:
        x, y = np.random.randint(0, im_src.size[0], (2,))
        rect = get_polygon_from_rect_box(x, y, width, height)

        if not rect.intersects(annotated_regions):
            if 0 <= x <= tiles_count[0] * 256 - width and 0 <= y <= tiles_count[1] * 256 - height:
                path = os.path.join(samples_dir, '%s_%d.jpg' % (basename, n_samples))
                crop_rect(im_src, x, y, width, height, path)
                n_samples += 1

                boxes.append([x, y, width, height])
                annotated_regions = get_multipolygon_from_boxes(boxes)

                if n_samples >= samples_per_image:
                    break


def get_multipolygon_from_boxes(boxes):
    return MultiPolygon([get_polygon_from_rect_box(*box) for box in boxes])


def crop_positive_sample_windows(im_src, annotation, basename, window_res=(48, 48), step_size=12):
    positive_samples_dir = os.path.join(config.positive_samples_dir)
    # positive_samples_dir = os.path.join(config.positive_samples_dir, str(window_res[0]))
    x, y, width, height = get_rect_from_annotation(annotation)

    if not os.path.exists(positive_samples_dir):
        os.makedirs(positive_samples_dir)

    if width < window_res[0]:
        diff = window_res[0] - width

        width_offset = diff
        x_offset = - diff / 2

        width += width_offset
        x += x_offset

        if x + width > im_src.size[0]:
            diff = x + width - im_src.size[0]
            x -= diff

        if x < 0:
            diff = x
            x -= diff

    if height < window_res[1]:
        diff = window_res[1] - height

        height_offset = diff
        y_offset = - diff / 2

        height += height_offset
        y += y_offset

        if y + height > im_src.size[1]:
            diff = y + height - im_src.size[1]
            y -= diff

        if y < 0:
            diff = y
            y -= diff

    im = crop_rect(im_src, x, y, width, height)

    for x_w, y_w, img in sliding_window(np.asarray(im), window_res, step_size):
        if img.shape[0] == window_res[0] and img.shape[1] == window_res[1]:
            filename = '%s_%d_%d.jpg' % (basename, x_w, y_w)
            path = os.path.join(positive_samples_dir, filename)

            im_window = Image.fromarray(img)
            im_window.save(path, 'JPEG')


def crop_negative_sample_windows(im_src, annotations, basename, samples_per_image, window_res=(48, 48)):
    negative_samples_dir = os.path.join(config.negative_samples_dir)
    # negative_samples_dir = os.path.join(config.negative_samples_dir, str(window_res[0]))
    boxes = [get_rect_from_annotation(annotation) for annotation in annotations_iter(annotations)]
    annotated_regions = MultiPolygon([get_polygon_from_rect_box(*box) for box in boxes])
    n_samples = 0

    if not os.path.exists(negative_samples_dir):
        os.makedirs(negative_samples_dir)

    while True:
        x, y = np.random.randint(0, im_src.size[0], (2,))
        rect = get_polygon_from_rect_box(x, y, *window_res)

        if not rect.intersects(annotated_regions) and 0 <= x <= 768 - window_res[0] and 0 <= y <= 768 - window_res[0]:
            path = os.path.join(negative_samples_dir, '%s_%d.jpg' % (basename, n_samples))
            crop_rect(im_src, x, y, window_res[0], window_res[1], path)
            n_samples += 1

        if n_samples >= samples_per_image:
            break


def sliding_window(image, window_res, step_size):
    # slide a window across the image
    for y in range(0, image.shape[0], step_size):
        for x in range(0, image.shape[1], step_size):
            # yield the current window
            yield (x, y, image[y:y + window_res[1], x:x + window_res[0]])


