import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.patches import Rectangle
from skimage import io
from skimage.util import view_as_windows

from models.mlp_5 import mlp_5

import config


def get_images(files_dir=None):
    if files_dir is None:
        files_dir = config.affixed_tiles_dir

    return io.imread_collection(files_dir + '/*.jpg', conserve_memory=True)


def plot_results(img, result, threshold=0.8):
    res_0 = result[:, :, 0]
    res_1 = result[:, :, 1]

    # res_0[res_0 < 0.5] = 0
    # res_1[res_1 < 0.5] = 0

    sns.set_style("white")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=False, sharey=False, squeeze=True, figsize=(15, 15))

    ax1.set_title("Original Image")
    ax1.imshow(img)

    ax2.set_title("Image with detections")
    ax2.imshow(img)

    for i in range(61):
        for j in range(61):
            p = result[i, j, :]

            # argmax = np.argmax(p)

            if p[1] > threshold:
                ax2.add_patch(Rectangle((i * 12, i * 12), 48, 48, fill=None, alpha=1, color='red'))

    ax3.set_title("Result for non tower")
    sns.heatmap(res_0, ax=ax3)

    ax4.set_title("Result for tower")
    sns.heatmap(res_1, ax=ax4)

    plt.show()


model = mlp_5()
model.compile(optimizer='sgd', loss='binary_crossentropy', metrics=['binary_accuracy', 'binary_crossentropy'])
model.load_weights('/home/tanuj/Workspace/power-grid-detection/models/mlp_5_a1_weights_best.hdf5')

images = get_images()

window_shape = (48, 48, 3)
stride = 12

i = 0

for image in images:
    windows = view_as_windows(image, window_shape, stride)
    w_shape = windows.shape

    windows = windows.reshape((w_shape[0] * w_shape[1], 48, 48, 3))

    res = model.predict(windows, batch_size=windows.shape[0])

    res = res.reshape((w_shape[0], w_shape[1], res.shape[1]))

    plot_results(image, res)

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
