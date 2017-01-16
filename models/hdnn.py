from __future__ import print_function
from __future__ import absolute_import

from keras.models import Sequential, Model
from keras.layers import Input, K, Convolution2D, MaxPooling2D, Activation, Dense
from keras.layers.core import Merge
from keras.preprocessing.image import ImageDataGenerator


def conv2d_block(input_tensor, nb_filter, kernel_size, stage, block, activation_fn='relu', stride=(2, 2),
                 pool_size=(2, 2), pool_stride=(2, 2)):
    conv_name = 'C%d_%d' % (stage, block)
    mp_name = 'M%d_%d' % (stage, block)
    print('Compiling conv2d layer: stage %d block %d...' % (stage, block))

    x = Convolution2D(nb_filter, kernel_size[0], kernel_size[1], subsample=stride, name=conv_name)(input_tensor)
    x = Activation(activation_fn)(x)
    x = MaxPooling2D(pool_size=pool_size, strides=pool_stride, name=mp_name)(x)

    return x


def hybrid_conv2d_block(n_blocks, input_tensor, nb_filters, kernel_sizes, stage, activation_fns='relu', strides=(2, 2),
                        pool_sizes=(2, 2),
                        pool_strides=(2, 2)):
    nb_filter = nb_filters
    kernel_size = kernel_sizes
    activation_fn = activation_fns
    stride = strides
    pool_size = pool_sizes
    pool_stride = pool_strides
    layers = []

    print('Creating hybrid block with %d conv2d blocks: stage %d' % (n_blocks, stage))

    for i in range(n_blocks):
        if isinstance(nb_filters, list):
            nb_filter = nb_filters[i]

        if isinstance(kernel_sizes, list):
            kernel_size = kernel_sizes[i]

        if isinstance(activation_fns, list):
            activation_fn = activation_fn[i]

        if isinstance(strides, list):
            stride = strides[i]

        if isinstance(pool_sizes, list):
            pool_size = pool_sizes[i]

        if isinstance(pool_strides, list):
            pool_stride = pool_strides[i]

        params = dict(
            input_tensor=input_tensor,
            nb_filter=nb_filter,
            kernel_size=kernel_size,
            stage=stage,
            block=i + 1,
            activation_fn=activation_fn,
            stride=stride,
            pool_size=pool_size,
            pool_stride=pool_stride
        )

        x = conv2d_block(**params)

        layers.append(x)

    print('Merging hybrid blocks : stage %d' % stage)
    x = Merge(layers, mode='concat', concat_axis=1)

    return x


def hdnn(input_shape=(48, 48, 3), input_tensor=None, weights=None):
    if input_tensor is None:
        img_input = Input(shape=input_shape)
    else:
        if not K.is_keras_tensor(input_tensor):
            img_input = Input(tensor=input_tensor, shape=input_shape)
        else:
            img_input = input_tensor

    x = conv2d_block(input_tensor=img_input, nb_filter=84, kernel_size=(7, 7), stage=1, block=1, activation_fn='tanh')
    x = conv2d_block(input_tensor=x, nb_filter=84, kernel_size=(4, 4), stage=2, block=1, activation_fn='tanh')

    # Hybrid block parameters
    hybrid_block_params = dict(
        n_blocks=3,
        input_tensor=x,
        nb_filters=[54, 20, 10],
        kernel_sizes=[(4, 4), (4, 4), (6, 6)],
        stage=3,
        activation_fns='tanh',
        strides=(2, 2),
        pool_sizes=[(3, 3), (2, 2), (2, 2)]
    )
    x = hybrid_conv2d_block(**hybrid_block_params)(x)

    x = Dense(output_dim=2, activation='tanh')(x)

    model = Model(input=img_input, output=x, name='hdnn')

    if weights is not None:
        # TODO Handling pre-trained model
        pass

    return model

if __name__ == '__main__':
    m = hdnn()

    m.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
