import json

import config


def load_annotations_nodes(annotations_file=None):
    if annotations_file is None:
        annotations_file = config.annotations_file

    with open(annotations_file, 'rb') as f:
        nodes = json.load(f)
    return nodes


def count_annotated_images(annotations_file=None):
    nodes = load_annotations_nodes(annotations_file)

    count = 0

    for node in nodes:
        if 'annotations' in node and len(node['annotations']) > 2:
            count += 1

    return count


def annotations_iter(annotations):
    for annotation in annotations:
        if annotation['class'] == 'tower':
            yield annotation


def count_annotations(annotations_file=None):
    nodes = load_annotations_nodes(annotations_file)

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
    return x, y, width, height


if __name__ == '__main__':
    print(count_annotations())
