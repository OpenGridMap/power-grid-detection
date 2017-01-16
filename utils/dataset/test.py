import config
from utils.dataset.helpers import load_dataset_from_pickle, get_image_collection
from keras.applications import VGG16

def info(x, y):
    print(x.shape)
    print(y.shape)
    print('{0:.2f} GB\n'.format((x.nbytes + y.nbytes) / (1024.0 ** 3)))


def test_load_data():
    (X_train, y_train), (X_validation, y_validation), (X_test, y_test) = load_dataset_from_pickle()
    print('Training data')
    info(X_train, y_train)
    print('Validation data')
    info(X_validation, y_validation)
    print('Test data')
    info(X_test, y_test)


if __name__ == '__main__':
    test_load_data()
    # images = get_image_collection(config.positive_samples_dir)
    #
    # print(images[0].shape)
