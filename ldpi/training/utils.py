import matplotlib as mpl
import matplotlib.patheffects as PathEffects
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
from scipy.interpolate import interp1d
from scipy.optimize import brentq
from sklearn.metrics import roc_curve, auc


def roc(scores, labels, plot=True):
    fpr = dict()
    tpr = dict()

    # True/False Positive Rates.
    fpr, tpr, thresholds = roc_curve(labels, scores)
    auroc = auc(fpr, tpr)

    # new_auc = auroc_score(labels, scores)

    # Equal Error Rate
    eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)

    if plot:
        # Colors, color cycles, and colormaps
        mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')

        # Colormap
        mpl.rcParams['image.cmap'] = 'jet'

        # Grid lines
        mpl.rcParams['grid.color'] = 'k'
        mpl.rcParams['grid.linestyle'] = ':'
        mpl.rcParams['grid.linewidth'] = 0.5

        # Figure size, font size, and screen dpi
        mpl.rcParams['figure.figsize'] = [8.0, 6.0]
        mpl.rcParams['figure.dpi'] = 80
        mpl.rcParams['savefig.dpi'] = 100
        mpl.rcParams['font.size'] = 12
        mpl.rcParams['legend.fontsize'] = 'large'
        mpl.rcParams['figure.titlesize'] = 'medium'

        # Marker size for scatter plot
        mpl.rcParams['lines.markersize'] = 3

        # Plot
        mpl.rcParams['lines.linewidth'] = 0.9
        mpl.rcParams['lines.dashed_pattern'] = [6, 6]
        mpl.rcParams['lines.dashdot_pattern'] = [3, 5, 1, 5]
        mpl.rcParams['lines.dotted_pattern'] = [1, 3]
        mpl.rcParams['lines.scale_dashes'] = False

        # Error bar
        mpl.rcParams['errorbar.capsize'] = 3

        # Patch edges and color
        mpl.rcParams['patch.force_edgecolor'] = True
        mpl.rcParams['patch.facecolor'] = 'b'

        plt.figure()
        lw = 1
        plt.plot(fpr, tpr, color='darkorange', label='(AUC = %0.4f, EER = %0.4f)' % (auroc, eer))
        plt.plot([eer], [1 - eer], marker='o', markersize=3, color="navy")
        # plt.plot([0, 1], [1, 0], color='navy', lw=1, linestyle=':')
        plt.plot([0, 0], [0, 1], color='navy', linestyle=':')
        plt.plot([0, 1], [1, 1], color='navy', linestyle=':')
        plt.xlim([-0.05, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        # plt.title('Receiver operating characteristic')
        plt.legend(loc="lower right")
        # plt.savefig(f'{args.exp_path}/auc_{epoch}.svg', bbox_inches='tight', format='svg', dpi=800)
        plt.show()
        plt.close()

    return auroc


# Plot normal/abnormal anomaly score distributions
def plot_anomaly_score_dists(test_scores, labels, threshold, add_legend=False):
    # Convert labels to boolean mask
    bool_abnormal = labels.astype(bool)
    bool_normal = ~bool_abnormal
    normal = test_scores[bool_normal]
    abnormal = test_scores[bool_abnormal]

    # Compute FAR and Detection Rate
    # Assuming perf_measure function is defined elsewhere and provides accuracy, precision, recall, and f-score
    acc, prec, rec, f_score = perf_measure(threshold, labels, test_scores)
    prec_label = f"{round((1 - prec) * 100, 2):.0f}%"
    rec_label = f"{round(rec * 100, 2):.0f}%"
    print('FAR', prec_label)
    print('detection rate', rec_label)

    # Define histogram bins
    bins = np.linspace(np.min(normal), np.percentile(abnormal, 99.95), 150)

    # Setup plot
    plt.style.use('classic')
    px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
    fig, ax = plt.subplots(figsize=(650 * px, 200 * px))

    # Plot histograms
    ax.hist(abnormal, bins=bins, label='Anomaly' if add_legend else '', linewidth=0, color='#DC3912', stacked=True)
    ax.hist(normal, bins=bins, label='Normal Traffic' if add_legend else '', linewidth=0, color='#3366cc', stacked=True, alpha=0.9)

    # Set various attributes
    ax.grid(zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(np.min(normal), np.percentile(abnormal, 99.95))
    ax.set_ylim(bottom=1)
    ax.set_xlabel('Anomaly Score')
    ax.set_ylabel(r'# of Flows (log)')
    ax.set_yscale('log')

    # Threshold annotation
    plt.axvline(x=threshold, linewidth=1.5, color='#3366cc', linestyle='dashed', label=f'DR: {rec_label}')
    text = plt.text(threshold, ax.get_ylim()[0] + 0.5, 'Threshold', rotation=90, size='small', color='black')
    text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='w')])

    # Add line to max percentile of abnormal
    maxth = np.percentile(abnormal, 99.99)
    plt.text(maxth, ax.get_ylim()[0] + 0.5, 'Max. Abnormal', rotation=90, size='small', color='black')

    if add_legend:
        ax.legend()

    fig.tight_layout()
    # Uncomment the following line to save the figure, ensure fig_name variable exists
    # plt.savefig(f'experiments/plots/{time.time()}.pdf', bbox_inches='tight', format='pdf', dpi=800)
    plt.show()
    plt.close(fig)


def plot_multiclass_anomaly_scores(test_scores, labels, threshold, add_legend=False):
    """
    Plot the anomaly scores for multiclass data, with each class in a different color.

    Args:
        test_scores (np.ndarray): The anomaly scores.
        labels (np.ndarray): The multiclass labels.
        threshold (float): The threshold for anomaly detection.
        add_legend (bool, optional): Whether to add a legend to the plot. Defaults to False.
    """
    unique_labels = np.unique(labels)

    # Define colors for each class - adjust this as needed
    colors = plt.cm.get_cmap('tab10', len(unique_labels))

    # Define histogram bins
    bins = np.linspace(np.min(test_scores), np.percentile(test_scores, 99.95), 150)

    # Setup plot
    plt.style.use('classic')
    px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
    fig, ax = plt.subplots(figsize=(650 * px, 200 * px))

    for i, label in enumerate(unique_labels):
        # Extract scores for the current label
        class_scores = test_scores[labels == label]

        # Plot histogram for the current label
        ax.hist(class_scores, bins=bins, label=f'Class {label}' if add_legend else '', linewidth=0, color=colors(i), stacked=True, alpha=0.7)

    # Set various attributes
    ax.grid(zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(np.min(test_scores), np.percentile(test_scores, 99.95))
    ax.set_ylim(bottom=1)
    ax.set_xlabel('Anomaly Score')
    ax.set_ylabel(r'# of Samples (log)')
    ax.set_yscale('log')

    # Threshold annotation
    plt.axvline(x=threshold, linewidth=1.5, color='#3366cc', linestyle='dashed', label=f'Threshold: {threshold}')
    text = plt.text(threshold, ax.get_ylim()[0] + 0.5, 'Threshold', rotation=90, size='small', color='black')
    text.set_path_effects([PathEffects.withStroke(linewidth=1.5, foreground='w')])

    if add_legend:
        ax.legend()

    fig.tight_layout()
    plt.show()
    plt.close(fig)
