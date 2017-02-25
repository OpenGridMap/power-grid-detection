import os
import json

import config

from utils.geo.coordinate import Coordinate
from utils.dataset.nodes import get_nodes_df, to_csv
from utils.tiles.adapters import get_adapter_class


def load_annotations(annotations_file):
    # if annotations_file is None:
    #     annotations_file = config.current_annotations_file
    with open(annotations_file, 'rb') as f:
        annotations = json.load(f)

    return annotations


def save_annotations(annotations, annotations_file, append=False, overwrite=False):
    if os.path.exists(annotations_file) and append:
        annotations = load_annotations(annotations_file) + annotations

    if not os.path.exists(annotations_file) or overwrite:
        with open(annotations_file, 'wb') as f:
            json.dump(annotations, f, sort_keys=True, indent=4)
            f.flush()

        return True
    else:
        print('Annotation file %s already exists.' % annotations_file)

        return False


def count_annotated_images(annotations_file=None):
    nodes = load_annotations(annotations_file)

    count = 0

    for node in nodes:
        if 'annotations' in node and len(node['annotations']) > 0:
            for annotation in node['annotations']:
                if annotation['class'] == 'tower':
                    count += 1
                    break

    return count


def annotations_iter(annotations):
    for annotation in annotations:
        if annotation['class'] == 'tower':
            yield annotation


def count_annotations(annotations_file=None):
    nodes = load_annotations(annotations_file)

    count = 0

    for node in nodes:
        annotations = node['annotations']

        for annotation in annotations_iter(annotations):
            count += 1

    return count


def get_rect_from_annotation(annotation):
    width = int(annotation['width'])
    height = int(annotation['height'])
    x = int(annotation['x'])
    y = int(annotation['y'])

    return map(int, [x, y, width, height])


def get_coord_from_annotation(annotation, tile):
    rect = get_rect_from_annotation(annotation)
    return Coordinate.from_rect(rect, tile)


def get_osm_id_from_annotation(annotation):
    if 'osm_id' in annotation:
        return str(int(annotation['osm_id']))

    return None


def initialize_sloth_annotations(zoom=18, annotations_file=None, crop_res=(140., 140.), crop_x_offset=0,
                                 crop_y_offset=0):
    if annotations_file is None:
        annotations_file = config.annotations_file

    if os.path.exists(annotations_file):
        print('File already exists :  %s' % annotations_file)
        return

    image_annotations = {}
    nodes, n = get_nodes_df()
    tiles_dir = config.affixed_tiles_dir

    for node in nodes.iterrows():
        # coord = Coordinate(lat=node[1]['lat'], lon=node[1]['lon'])
        # filepath = os.path.abspath(os.path.join(tiles_dir, str(int(node[1]['osm_id'])) + '.jpg'))

        coord = Coordinate.from_transnet_node(node)
        filepath = os.path.join(tiles_dir, get_adapter_class().get_filename(coord.get_tile(zoom)))

        if os.path.exists(filepath):
            crop_box = coord.get_crop_box(zoom=zoom, crop_size=crop_res, crop_x_offset=crop_x_offset,
                                          crop_y_offset=crop_y_offset)

            image_annotation = {
                "class": "tower",
                "type": "rect",
                "height": crop_res[0],
                "width": crop_res[1],
                "x": crop_box[0],
                "y": crop_box[1],
                "osm_id": int(node[1]['osm_id'])
            }

            if filepath in image_annotations:
                image_annotations[filepath].append(image_annotation)
            else:
                image_annotations[filepath] = [image_annotation]

                # properties = {
                #     'annotations': [
                #         {
                #             "class": "tower",
                #             "type": "rect",
                #             "height": crop_res,
                #             "width": crop_res,
                #             "x": crop_box[0],
                #             "y": crop_box[1]
                #         }
                #     ],
                #     'class': 'image',
                #     'filename': filepath
                # }

                # image_annotations.append(properties)

    # print(image_annotations)
    annotations = []

    for k in image_annotations:
        properties = {
            'annotations': image_annotations[k],
            'class': 'image',
            'filename': k
        }
        annotations.append(properties)

    save_annotations(annotations, annotations_file)

    # with open(annotations_file, 'wb') as f:
    #     json.dump(annotations, f, sort_keys=True, indent=4)
    #     f.flush()


def update_corrected_annotations(annotation_file, x=281279, y=171693, zoom=19, final_annotations_file=None,
                                 pending_annotations_file=None, final_transnet_nodes_file=None):
    """
    :param annotation_file: annotation file with the corrected annotations
    :param x: last annotated tile's x coordinate, for e.g. 123 in 123_456_18.jpg
    :param y: last annotated tile's y coordinate, for e.g. 456 in 123_456_18.jpg
    :param zoom: zoom level of the image, for e.g. 18 in 123_456_18.jpg
    :param final_annotations_file: file to save the corrected annotations in.
    :param pending_annotations_file: file to save the pending annotations
    :param final_transnet_nodes_file: file to save corrected transnet nodes
    :return: filtered list of corrected annotations
    """
    file_format = '{}_{}_{}.jpg'
    n_files = 0
    n_samples = 0
    n_pending = 0
    corrected_annotations = []
    pending_annotations = []
    corrected_nodes = []
    pending = False

    filename = file_format.format(x, y, zoom)
    nodes = load_annotations(annotation_file)

    if final_annotations_file is None:
        final_annotations_file = config.final_annotations_file

    if pending_annotations_file is None:
        pending_annotations_file = config.pending_annotations_file

    if final_transnet_nodes_file is None:
        final_transnet_nodes_file = config.nodes_corrected

    for i, node in enumerate(nodes):
        if 'filename' in node and 'annotations' in node:
            node_filename = os.path.basename(node['filename'])

            if not pending:
                for annotation in node['annotations']:
                    osm_id = None
                    tile = tuple(map(int, node_filename.split('.')[0].split('_')))

                    if 'osm_id' in annotation:
                        osm_id = annotation['osm_id']

                    coord = get_coord_from_annotation(annotation, tile)
                    transnet_node = coord.get_transnet_node(osm_id)
                    corrected_nodes.append(transnet_node)

                n_samples += len(node['annotations'])
                corrected_annotations.append(node)
            else:
                pending_annotations.append(node)
                n_pending += 1

            if filename == node_filename:
                print('Current annotation : %d' % (i + 1))
                n_files = i + 1
                pending = True
                # break

    if n_files == 0:
        print('Last annotated file %s not found.' % filename)
        return []
    else:
        print('%d annotations in %d images' % (n_samples, n_files))
        print('%d images pending to be annotated' % n_pending)

        last_annotation_meta = dict(x=tile[0], y=tile[1], z=tile[2])
        save_annotations(last_annotation_meta, os.path.join(config.dataset_dir, 'annotations-final.meta'),
                         overwrite=True)

        save_annotations(corrected_annotations, final_annotations_file, False, True)
        save_annotations(pending_annotations, pending_annotations_file, False, True)
        to_csv(corrected_nodes, final_transnet_nodes_file)

    return corrected_annotations


if __name__ == '__main__':
    update_corrected_annotations(config.corrected_annotations_file, 281279, 171693, 19)

    # print(count_annotations())
    # print(count_annotated_images(config.current_annotations_file))
