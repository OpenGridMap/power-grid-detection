from __future__ import print_function
from __future__ import absolute_import

from keras.models import Sequential, Model
from keras.layers import Input, K, Convolution2D, MaxPooling2D, Activation, Dense, Flatten, merge
from keras.regularizers import l1l2
from keras.layers.core import Merge
from keras.preprocessing.image import ImageDataGenerator


def conv2d_block(input_tensor, nb_filter, kernel_size, stage, block, activation_fn='relu', stride=(2, 2),
                 pool_size=(2, 2), pool_stride=(2, 2), input_shape=None, init='glorot_uniform', l1=0.01, l2=0.01):
    conv_name = 'C%d_%d' % (stage, block)
    mp_name = 'M%d_%d' % (stage, block)
    print('Compiling conv2d layer: stage %d block %d...' % (stage, block))

    x = Convolution2D(nb_filter, kernel_size[0], kernel_size[1], subsample=stride, name=conv_name, init=init,
                      W_regularizer=l1l2(l1, l2), b_regularizer=l1l2(l1, l2))(input_tensor)
    x = Activation(activation_fn)(x)
    x = MaxPooling2D(pool_size=pool_size, strides=pool_stride, name=mp_name)(x)

    return x


def hybrid_conv2d_block(n_blocks, input_tensor, input_shape, nb_filters, kernel_sizes, stage, activation_fns='relu',
                        strides=(2, 2),
                        pool_sizes=(2, 2), pool_strides=(2, 2)):
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

        hybrid_layer_input = Input(tensor=input_tensor, shape=input_shape)

        params = dict(
            # input_tensor=input_tensor,
            input_tensor=hybrid_layer_input,
            # input_shape=input_shape,
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
        # x = Flatten()(x)

        layers.append(Model(input=hybrid_layer_input, output=x)(input_tensor))
        # layers.append(x)

    print('Merging hybrid blocks : stage %d' % stage)
    # x = Merge(layers=layers, mode='concat', concat_axis=3)
    # x = merge(layers, mode='concat', concat_axis=3)
    return merge(layers, mode='concat', concat_axis=3)

    # return x


def hdnn_(input_shape=(140, 140, 3), input_tensor=None, weights=None, activation_fn='tanh', init='glorot_uniform',
          l1=0.01, l2=0.01, dropout=0.5):
    if input_tensor is None:
        img_input = Input(shape=input_shape)
    else:
        if not K.is_keras_tensor(input_tensor):
            img_input = Input(tensor=input_tensor, shape=input_shape)
        else:
            img_input = input_tensor

    x = conv2d_block(input_tensor=img_input, nb_filter=84, kernel_size=(7, 7), stage=1, block=1,
                     activation_fn=activation_fn, stride=(1, 1), init=init, l1=l1, l2=l2)
    x = conv2d_block(input_tensor=x, nb_filter=84, kernel_size=(4, 4), stage=2, block=1, activation_fn=activation_fn,
                     stride=(1, 1), init=init, l1=l1, l2=l2)
    x = conv2d_block(input_tensor=x, nb_filter=54, kernel_size=(4, 4), stage=3, block=1, activation_fn=activation_fn,
                     pool_size=(3, 3), stride=(1, 1), init=init, l1=l1, l2=l2)

    # Hybrid block parameters
    hybrid_block_params = dict(
        n_blocks=3,
        input_tensor=x,
        input_shape=(14, 14, 54),
        nb_filters=[54, 20, 10],
        kernel_sizes=[(4, 4), (4, 4), (6, 6)],
        stage=3,
        activation_fns=activation_fn,
        strides=(2, 2),
        pool_sizes=[(2, 2), (2, 2), (1, 1)]
    )

    # x = hybrid_conv2d_block(**hybrid_block_params)
    #
    # x = Flatten()(x)
    # x = Dense(1024, activation=activation_fn)(x)
    # x = Dense(1024, activation=activation_fn)(x)
    # x = Dense(1024, activation=activation_fn)(x)
    # x = Dense(output_dim=2, activation=activation_fn)(x)
    # x = Activation('softmax')(x)

    model = Model(input=img_input, output=x, name='hdnn')

    if weights is not None:
        # TODO Handling pre-trained model
        pass

    return model


def hdnn(input_shape=(140, 140, 3), input_tensor=None, weights=None, activation_fn='tanh', init='glorot_uniform',
         l1=0.01, l2=0.01, dropout=0.5):
    img_input = Input(shape=input_shape)

    x = conv2d_block(input_tensor=img_input, nb_filter=84, kernel_size=(7, 7), stage=1, block=1,
                     activation_fn=activation_fn, stride=(1, 1), init=init, l1=l1, l2=l2)
    x = conv2d_block(input_tensor=x, nb_filter=84, kernel_size=(4, 4), stage=2, block=1, activation_fn=activation_fn,
                     stride=(1, 1), init=init, l1=l1, l2=l2)
    x = conv2d_block(input_tensor=x, nb_filter=54, kernel_size=(4, 4), stage=3, block=1, activation_fn=activation_fn,
                     pool_size=(3, 3), stride=(1, 1), init=init, l1=l1, l2=l2)

    # Hybrid Block 1
    print('Creating hybrid block with 3 conv2d blocks: stage 4')
    x1 = conv2d_block(input_tensor=x, nb_filter=54, kernel_size=(4, 4), stride=(2, 2), stage=4, block=1,
                      activation_fn=activation_fn, pool_size=(2, 2), init=init, l1=l1, l2=l2)

    x2 = conv2d_block(input_tensor=x, nb_filter=20, kernel_size=(4, 4), stride=(2, 2), stage=4, block=2,
                      activation_fn=activation_fn, pool_size=(2, 2), init=init, l1=l1, l2=l2)

    x3 = conv2d_block(input_tensor=x, nb_filter=10, kernel_size=(6, 6), stride=(2, 2), stage=4, block=3,
                      activation_fn=activation_fn, pool_size=(1, 1), init=init, l1=l1, l2=l2)
    print('Merging hybrid blocks : stage 4')

    x = merge([x1, x2, x3], mode='concat')

    # x = hybrid_conv2d_block(**hybrid_block_params)
    #
    x = Flatten()(x)
    x = Dense(300, activation=activation_fn)(x)
    # x = Dense(1024, activation=activation_fn)(x)
    # x = Dense(1024, activation=activation_fn)(x)
    x = Dense(output_dim=2, activation=activation_fn)(x)
    x = Activation('softmax')(x)

    model = Model(input=img_input, output=x)

    if weights is not None:
        model.load_weights(weights)

    return model


if __name__ == '__main__':
    hdnn()
