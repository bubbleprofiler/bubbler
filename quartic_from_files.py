"""
Compare results from different codes for a one-dimensional potential
====================================================================
"""


import numpy as np
import matplotlib.pyplot as plt

from bubbler import one_dim_bubblers


RC_PARAMS = {'text.latex.preamble' : [r'\usepackage{amsmath}'],
             'font.family': 'lmodern',
             'font.size': 30,
             'axes.titlesize': 20,
             'xtick.labelsize': 30,
             'ytick.labelsize': 30,
             'axes.labelsize': 30,
             'legend.fontsize': 20,
             'text.usetex': True,
             'lines.linewidth': 3,
             'axes.linewidth': 1,
             'axes.grid': True,
             'grid.linestyle': '--',
             'legend.framealpha': 1.,
             'legend.edgecolor': 'black',
             'savefig.bbox': 'tight'}

ACTION = "action_ct.npy"
TIME = "time_ct.npy"

def analytic(alpha):
    return 4. * np.pi / (81. * (alpha - 0.5)**2)


def make_fig(alphas, action_ct, action_bp, time_ct, time_bp, name, plot_time=True):

    # Make numpy arrays and replace any missing data (None types) with inf

    action_ct = np.array(action_ct, dtype=float)
    action_bp = np.array(action_bp, dtype=float)
    action_thin = analytic(alphas)

    rdiff = abs((action_ct - action_bp) / action_bp)

    fig = plt.figure(figsize=(12, 20))
    plt.rcParams.update(RC_PARAMS)
    plt.subplots_adjust(hspace=0.1)

    ax_1 = plt.subplot(311)
    ax_1.plot(alphas, action_ct, '--', label=r"\texttt{CosmoTransitions}", color="Brown", lw=3)
    ax_1.plot(alphas, action_bp, '-', label=r"\texttt{BubbleProfiler}", color="Green", lw=3)
    ax_1.plot(alphas, action_thin, ':', label=r"Thin-wall approximation", color="Red", lw=3)
    ax_1.set_ylabel("Action, $S$")
    ax_1.legend(numpoints=1, fontsize=16, loc='best')
    ax_1.set_yscale('log')
    ax_1.set_xlim(0.45, 0.8)

    ax_2 = plt.subplot(312, sharex=ax_1)
    ax_2.plot(alphas, rdiff, color="Blue", lw=3)
    ax_2.set_ylabel("Relative difference")
    ax_2.set_yscale('log')
    ax_2.set_ylim(None, 1.)


    if plot_time:

        ax_3 = plt.subplot(313, sharex=ax_1)
        ax_3.plot(alphas, time_ct, '--', label=r"\texttt{CosmoTransitions}", color="Brown", lw=3)
        ax_3.plot(alphas, time_bp, '-', label=r"\texttt{BubbleProfiler}", color="Green", lw=3)
        ax_3.set_xlabel(r"$\alpha$")
        ax_3.legend(numpoints=1, fontsize=16, loc='best')
        ax_3.set_ylabel(r"time (s)")
        ax_3.set_yscale('log')
        plt.setp(ax_2.get_xticklabels(), visible=False)

    plt.setp(ax_1.get_xticklabels(), visible=False)
    plt.savefig(name)


if __name__ == "__main__":

    try:
        data = np.loadtxt("bp.dat", unpack=True)
    except IOError:
        raise IOError("Must make bp.dat data file by "
                       "./quartic_tabulate 3 0.5001 0.74999 0.0001 > /bubbler/bp.dat")
    alphas = data[2]
    E = data[1][0]
    action_bp = data[3]
    time_bp = data[4] * 1e-3  # Convert from ms to s

    try:
        action_ct = np.load(ACTION)
        time_ct = np.load(TIME)
    except:

        # Make CosmoTransitions results

        action_ct = np.zeros_like(alphas)
        time_ct = np.zeros_like(alphas)

        for i, alpha in enumerate(alphas):

            print "============================="
            print "alpha = {}".format(alpha)
            print "============================="

            results = one_dim_bubblers(E, alpha, backends=['cosmotransitions'])
            action_ct[i] = results['cosmotransitions'].action
            time_ct[i] = results['cosmotransitions'].time

            print results

        np.save(ACTION, action_ct)
        np.save(TIME, time_ct)

    make_fig(alphas, action_ct, action_bp, time_ct, time_bp, "quartic_from_files.pdf")
