import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.patches import Rectangle
from skimage import io
from skimage.util import view_as_windows

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

# from models.mlp_5 import mlp_5
from models.cnn3_with_normalization import cnn_w_normalization

import config


def get_images(files_dir=None):
    if files_dir is None:
        files_dir = config.affixed_tiles_dir

    # return io.imread_collection(files_dir + '/*.jpg', conserve_memory=True)
    return io.imread_collection('/home/tanuj/tmp/tmp/*.jpg', conserve_memory=True)


def plot_results(img, result, threshold=0.1):
    res_0 = result[:, :, 0]
    res_1 = result[:, :, 1]

    print(res_1.shape)

    # res_0[res_0 < 0.5] = 0
    # res_1[res_1 < 0.5] = 0

    sns.set_style("white")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=False, sharey='row', squeeze=True, figsize=(15, 15))
    # plt.axis('scaled')

    ax1.set_title("Original Image")
    ax1.imshow()

    ax2.set_title("Image with detections")
    ax2.imshow(img)

    for j in range(21):
        for k in range(21):
            p = res_1[j, k].tolist()

            # print(type(p))
            # print(p)

            if p > threshold:
                # print(j, k)
                ax2.add_patch(Rectangle((k * 12, j * 12), 128, 128, fill=None, alpha=1, color='red'))
            else:
                print(p)
                print('haw')
                #     print(type(p))

    ax3.set_title("Result for non tower")
    sns.heatmap(res_0, ax=ax3)
    # ax3.clim(0., 1.)

    ax4.set_title("Result for tower")
    sns.heatmap(res_1, ax=ax4)
    # ax4.clim(0., 1.)

    plt.show()


# model = mlp_5()
print('loading model...')
model = cnn_w_normalization(input_shape=(128, 128, 1))
print('compiling model...')
model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['binary_accuracy'])

model.summary()

print('loading model weights...')
# model.load_weights('3ccn_w_n_a1_1o_weights_best.hdf5')
model.load_weights('/home/tanuj/Workspace/power-grid-detection/models/3ccn_weights_best.hdf5')

print('loading images...')
images = get_images()

# window_shape = (48, 48, 3)
window_shape = (128, 128, 1)
# stride = 12
stride = 32

i = 0

for image in images:
    print(image.shape)
    # image = image.reshape((image.shape[0], image.shape[1], 1))
    print(image.shape)
    windows = view_as_windows(image, (128, 128), stride)
    w_shape = windows.shape

    print(w_shape)

    windows = windows.reshape((w_shape[0] * w_shape[1], 128, 128, 1))

    print(windows.shape)

    res = model.predict(windows, batch_size=1)

    print(res.shape)

    # res = res.reshape((w_shape[0], w_shape[1], res.shape[1]))
    res = res.reshape((w_shape[0], w_shape[1], res.shape[1]))

    plot_results(image, res)

    # break

    # res_0 = res[:, :, 0]
    # res_1 = res[:, :, 1]
    # print('-----------')
    # print(res.shape)
    # print(res_0.shape)
    # print(res_1.shape)
    # print(res[0])
    # print(res_0[0])
    # print(res_1[0])

    # i += 1
    #
    # if i > 0:
    #     break
