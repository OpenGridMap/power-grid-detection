import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_loss_acc(f, xlim=None, ylim=None, figsize=(16, 8)):
    df = pd.read_csv(f)

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, figsize=figsize)

    ax1.plot(df.loss, label='Training loss', linewidth=1.5)
    ax1.plot(df.val_loss, label='Validation loss', linewidth=1.5)

    # ax1.set_title('Loss vs Epochs')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.legend(loc='upper right')

    ax2.plot(df.acc, label='Training accuracy', linewidth=1.5)
    ax2.plot(df.val_acc, label='Validation accuracy', linewidth=1.5)
    ax2.set_xlabel('epochs')
    ax2.set_ylabel('binary accuracy')
    ax2.legend(loc='upper right')

    if xlim is not None:
        ax1.set_xlim(xlim)
        ax2.set_xlim(xlim)

    if ylim is not None:
        ax1.set_ylim(ylim)
        ax2.set_ylim(ylim)

    plt.show()


if __name__ == '__main__':
    plot_loss_acc('cnn_140_1_thr_dil_ero_lr_0.100000_training.log')