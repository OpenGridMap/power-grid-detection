from keras.layers import Input, Convolution2D, MaxPooling2D, Flatten, Dense
from keras.models import Model


def VGG10(weights=None, input_shape=(128, 128, 3)):
    input_img = Input(shape=input_shape)

    x = Convolution2D(32, 3, 3, activation='relu', border_mode='same', name='B1_C1')(input_img)
    x = Convolution2D(32, 3, 3, activation='relu', border_mode='same', name='B1_C2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='B1_MP1')(x)

    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', name='B2_C1')(x)
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', name='B2_C2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='B2_MP1')(x)

    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', name='B3_C1')(x)
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', name='B3_C2')(x)
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', name='B3_C3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='B3_MP1')(x)

    x = Flatten(name='F')(x)
    x = Dense(1024, activation='relu', name='D1')(x)
    x = Dense(1024, activation='relu', name='D2')(x)
    x = Dense(2, activation='sigmoid', name='O')(x)

    model = Model(input=input_img, output=x)

    if weights is None:
        # TODO handle trained model
        pass

    return model
