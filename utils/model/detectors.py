import os
import json

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import patches
from skimage.util import view_as_windows
from sklearn.metrics import precision_recall_curve
from keras.models import Model, Sequential
from keras.utils import np_utils

from helpers import get_model_from_json
from utils.img.collection import ImageCollection
from utils.dataset.helpers import get_image_collection
from utils.dataset.annotations import load_annotations, annotations_iter, get_rect_from_annotation
from utils.img.helpers import get_polygon_from_coord, get_polygon_from_rect_box


# Malisiewicz et al.
def non_max_suppression_fast(boxes, overlapThresh):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # initialize the list of picked indexes
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
                                               np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked using the
    # integer data type
    return boxes[pick].astype("int")


def get_box(d):
    w = (140, 140)
    s = 35


class TowerDetector(object):
    def __init__(self, model, weights, window_size=(140, 140, 3), stride=35):
        if isinstance(model, Model) or isinstance(model, Sequential):
            self.model = model
        elif isinstance(model, str):
            self.model = get_model_from_json(model)

        self.model.load_weights(weights)

        # self.model.evaluate_generator()

        self.window_size = window_size
        self.stride = stride

    def detect_in_image(self, img):
        if len(img.shape) == 2:
            window_size = (self.window_size[0], self.window_size[1], 1)
            img = img.reshape((img.shape[0], img.shape[1], 1))
        else:
            window_size = self.window_size

        windows = view_as_windows(img, window_size, self.stride)
        windows_shape = windows.shape

        windows = windows.reshape((windows_shape[0] * windows_shape[1], windows_shape[3], windows_shape[4], 3))

        predictions = self.model.predict(windows, batch_size=32, verbose=1)

        y = np_utils.categorical_probas_to_classes(predictions)
        y = y.reshape(windows_shape[0], windows_shape[1])

        detections = zip(*np.where(y == 1))

        # print(detections)
        # print(predictions)

        bxs = []

        for c, r in detections:
            # print(p)
            bxs.append([
                r * self.stride,
                c * self.stride,
                r * self.stride + window_size[0],
                c * self.stride + window_size[1],
            ])

        bxs = non_max_suppression_fast(np.asarray(bxs), 0.1)
        # bxs = zip(*bxs)
        # print('Boxes :', bxs)

        return bxs

    def evaluate_network(self, annotations_file, n, threshold):
        nodes = load_annotations(annotations_file)
        y_truth = []
        y_pred = []

        TP = 0
        FP = 0
        FN = 0

        for i in range(n):
            tp = 0
            fp = 0
            fn = 0
            node = nodes[i]
            filename = node['filename']

            img = ImageCollection.load_image(filename)
            detections = self.detect_in_image(img)

            detection_polygons = []
            annotation_polygons = []

            # fig, ax = plt.subplots(1, 1, squeeze=True, figsize=(10, 10))
            # ax.axis('off')
            #
            # ax.imshow(img)
            # ax.set_adjustable('box-forced')

            for d in detections:
                detection_polygons.append(get_polygon_from_coord(*d))

                # patch = patches.Rectangle(
                #     (d[0], d[1]),
                #     d[2] - d[0],
                #     d[3] - d[1],
                #     fill=False,
                #     edgecolor="red"
                # )
                #
                # ax.add_patch(patch)

            for annotation in node['annotations']:
                rect = get_rect_from_annotation(annotation)
                annotation_polygons.append(get_polygon_from_rect_box(*rect))

                # patch = patches.Rectangle(
                #     (rect[0], rect[1]),
                #     rect[2],
                #     rect[3],
                #     fill=False,
                #     edgecolor="blue"
                # )
                #
                # ax.add_patch(patch)

            print('\nND :', len(detection_polygons))
            print('NA :', len(annotation_polygons))

            for annotation in annotation_polygons:
                if len(detection_polygons) == 0:
                    fn += 1

                    y_truth.append(1)
                    y_pred.append(0)
                else:
                    matches = 0
                    for detection in detection_polygons:
                        if annotation.intersects(detection):
                            intersection = annotation.intersection(detection)

                            intersection_area = intersection.area
                            union_area = annotation.area + detection.area - intersection.area

                            iou = intersection_area / union_area

                            print('IOU :', iou)

                            if iou > threshold:
                                tp += 1

                                y_pred.append(1)
                                y_truth.append(1)

                                matches += 1
                        # else:
                        #     fp += 1
                        #
                        #     y_pred.append(1)
                        #     y_truth.append(0)

                    if matches == 0:
                        fn += 1

                        y_truth.append(1)
                        y_pred.append(0)

            if tp < len(detection_polygons):
                fp += len(detection_polygons) - tp
                # fp += 1

                for _ in range(len(detection_polygons) - tp):
                    y_pred.append(1)
                    y_truth.append(0)

            # if len(annotation_polygons) == 0 and len(detection_polygons) > 0:
            #     for _ in range(len(detection_polygons)):
            #         fp += 1
            #
            #         y_truth.append(0)
            #         y_pred.append(1)

            print('TP :', tp)
            print('FP :', fp)
            print('FN :', fn)
            plt.show()

            TP += tp
            FP += fp
            FN += fn
        print('TP :', TP)
        print('FP :', FP)
        print('FN :', FN)
        print('Precision :', 1. * TP / (TP + FP))
        print('Recall :', 1. * TP / (TP + FN))


if __name__ == '__main__':
    from models.cnn3 import cnn_regularized
    import config

    ic = get_image_collection(config.affixed_tiles_dir)

    m = cnn_regularized(input_shape=(140, 140, 3))
    m.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy', 'precision', 'recall'])
    # Good one
    # w = '/home/tanuj/Workspace/power-grid-detection/training/cnn_140_rgb_corrected_full_lr_0.005000_sgd_he_normal__l1_0.000010_l2_0.000010_dropout_0.500000_r_training_weights_current.hdf5'

    # Ok
    # w = '/home/tanuj/Workspace/power-grid-detection/training/saved weights/cnn_140_rgb_corrected_full_lr_0.005000_sgd_he_normal__l1_0.000010_l2_0.000010_dropout_0.500000_r_training_weights_current.hdf5'

    # Best one
    w = '/home/tanuj/Workspace/power-grid-detection/training/cnn_140_rgb_corrected_full_finetune_decay_lr_0.050000_sgd_he_normal__l1_0.000010_l2_0.000010_dropout_0.500000_r_training_weights_best.hdf5'
    m = TowerDetector(m, weights=w)

    m.evaluate_network(config.corrected_annotations_file, 2000, 0.2)

    # ws = m.model.get_weights()
    # print(len(ws))
    # print(ws[0][:, :, :, 0].shape)

    # fig, ax = plt.subplots(8, 16, sharey='all', sharex='all', squeeze=True)

    # p = 0
    # for i in range(8):
    #     for j in range(16):
    #         ax[i, j].imshow(ws[0][:, :, :, p])
    #         p += 1

    # plt.show()

    # l1 = m.model.get_layer('activation_3')
    #
    # mo = Model(m.model.input, l1.output)
    #
    # im = ic[100][:140, :140, :]
    # res = mo.predict(im.reshape((1, 140, 140, 3)))
    #
    # print(res.shape)
    #
    # for i in range(res.shape[-1]):
    #     fig, (ax1, ax2) = plt.subplots(1, 2)
    #     ax1.imshow(im)
    #     ax2.imshow(res[0, :, :, i])
    #     plt.savefig('out_3/ex_%d.png' % i)
    #     plt.clf()
    #     print(i)


    # for i in ic:
    #     m.detect_in_image(i)

    # m.detect_in_image(ImageCollection.load_image(
    #     '/home/tanuj/Workspace/power-grid-detection/data/cache/google-maps/3x3_tiles/271124_175971_19.jpg'))
