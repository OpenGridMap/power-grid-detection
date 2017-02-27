from keras.applications import VGG16
from keras.layers import Input, Flatten, Dense, Dropout
from keras.regularizers import l1l2
from keras.models import Model


def vgg16(input_shape=(224, 224, 3), weights=None, vgg_transfer=None, activation_fn='relu', l1=0.00001, l2=0.00001, dropout=0.5):
    input_tensor = Input(shape=input_shape)

    if vgg_transfer is not None:
        vgg_transfer = 'imagenet'

    vgg = VGG16(input_tensor=input_tensor, include_top=False, weights=vgg_transfer, input_shape=input_shape)

    x = Flatten(name='flatten')(vgg.output)
    x = Dense(4096, activation=activation_fn, name='fc1', W_regularizer=l1l2(l1, l2), b_regularizer=l1l2(l1, l2))(x)
    x = Dropout(dropout)(x)
    x = Dense(4096, activation=activation_fn, name='fc2', W_regularizer=l1l2(l1, l2), b_regularizer=l1l2(l1, l2))(x)
    x = Dense(2, activation='softmax', name='predictions')(x)

    model = Model(input=input_tensor, output=x)

    if weights is not None:
        model.load_weights(weights)

    return model


if __name__ == '__main__':
    m = vgg16(vgg_transfer=True)
    m.summary()

