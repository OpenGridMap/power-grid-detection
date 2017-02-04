import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_loss_acc(f):
    df = pd.read_csv(f)

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, figsize=(16, 8))

    ax1.plot(df.loss, label='Training loss')
    ax1.plot(df.val_loss, label='Validation loss')

    # ax1.set_title('Loss vs Epochs')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.legend(loc='upper right')
    # ax1.set_xlim([0., 100.])
    # ax1.set_ylim([0., 1.])

    ax2.plot(df.acc, label='Training accuracy')
    ax2.plot(df.val_acc, label='Validation accuracy')
    ax2.set_xlabel('epochs')
    ax2.set_ylabel('binary accuracy')
    # ax2.set_xlim([0., 100.])
    # ax2.set_ylim([0., 1.])
    ax2.legend(loc='upper right')

    plt.show()


if __name__ == '__main__':
    plot_loss_acc('cnn_140_1_thr_dil_ero_lr_0.100000_training.log')