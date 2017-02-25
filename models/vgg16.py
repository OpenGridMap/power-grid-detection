from keras.layers import Input, Convolution2D, MaxPooling2D, Activation, Flatten, Dense
from keras.models import Model


def vgg(input_shape, weights=None, classes=2):

    img_input = Input(shape=input_shape)

    # Block 1
    x = Convolution2D(64, 3, 3, border_mode='same', name='block1_conv1')(img_input)
    x = Activation('relu')(x)
    x = Convolution2D(64, 3, 3, border_mode='same', name='block1_conv2')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = Convolution2D(128, 3, 3, border_mode='same', name='block2_conv1')(x)
    x = Activation('relu')(x)
    x = Convolution2D(128, 3, 3, border_mode='same', name='block2_conv2')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = Convolution2D(256, 3, 3, border_mode='same', name='block3_conv1')(x)
    x = Activation('relu')(x)
    x = Convolution2D(256, 3, 3, border_mode='same', name='block3_conv2')(x)
    x = Activation('relu')(x)
    x = Convolution2D(256, 3, 3, border_mode='same', name='block3_conv3')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = Convolution2D(512, 3, 3, border_mode='same', name='block4_conv1')(x)
    x = Activation('relu')(x)
    x = Convolution2D(512, 3, 3, border_mode='same', name='block4_conv2')(x)
    x = Activation('relu')(x)
    x = Convolution2D(512, 3, 3, border_mode='same', name='block4_conv3')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = Convolution2D(512, 3, 3, border_mode='same', name='block5_conv1')(x)
    x = Activation('relu')(x)
    x = Convolution2D(512, 3, 3, border_mode='same', name='block5_conv2')(x)
    x = Activation('relu')(x)
    x = Convolution2D(512, 3, 3, border_mode='same', name='block5_conv3')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)

    # Classification block
    x = Flatten(name='flatten')(x)
    x = Dense(4096, name='fc1')(x)
    x = Activation('relu')(x)
    x = Dense(4096, name='fc2')(x)
    x = Activation('relu')(x)
    x = Dense(classes, name='predictions')(x)
    x = Activation('softmax')(x)

    # Create model.
    model = Model(img_input, x, name='vgg16')

    return model
