"""
Compare results from different codes against analytic results
=============================================================
"""

import numpy as np
import matplotlib.pyplot as plt

from bubbler import bubblers, Potential
from quartic_from_files import RC_PARAMS


# Make potentials

def thin_wall(lambda_, a, epsilon):

    thin_wall_str = "{lambda_} / 8 * (x^2 - {a}^2)^2 + 1/2 * {epsilon} / {a} * (x - {a})"
    p = Potential(thin_wall_str.format(lambda_=lambda_, epsilon=epsilon, a=a), true_vacuum=-a, false_vacuum=a)
    S = 16. * np.pi**2 * a**12 * lambda_**2 / (6. * epsilon**3)
    return (p, S)

def logarithmic(mass, omega):

    logarithmic_str = "1/2 * {mass}^2 * x^2 * (1 - log(x^2 / {omega}^2))"
    p = Potential(logarithmic_str.format(mass=mass, omega=omega),
                  true_vacuum=10. * omega, false_vacuum=1e-3 * omega, polish=False)
    S = 0.5 * np.pi**2 * np.exp(4.) * omega**2 / mass**2
    return (p, S)

def fubini(u, v, m):

    fubini_str = "4 * {u} * {m}^2 * ({m} - 1) / (2 * {m} + 1) * x^(2 + 1 / {m}) - 2 * {u} * {v} * {m}^2 * x^(2 + 2 / {m})"
    zero = 2**m / (m**2 * u * v)**m * (((m - 1) * m**2 * u) / (1 + 2 * m))**m
    p = Potential(fubini_str.format(u=u, v=v, m=m), true_vacuum=10. * zero, false_vacuum=0., polish=False)
    S = m * np.pi**2 / ((4. * m**2 - 1.) * u * v**(2 * m - 1))
    return (p, S)

def make_fig(action_ct, action_bp, action_exact, time_ct, time_bp, name, coord, coord_name, plot_time=False):

    rdiff_ct = abs((action_ct - action_exact) / action_exact)
    rdiff_bp = abs((action_bp - action_exact) / action_exact)

    fig = plt.figure(figsize=(12, 20))
    plt.rcParams.update(RC_PARAMS)
    plt.subplots_adjust(hspace=0.1)

    ax_1 = plt.subplot(311)
    ax_1.plot(coord, action_ct, '--', label=r"\texttt{CosmoTransitions}", color="Brown", lw=3)
    ax_1.plot(coord, action_bp, '-', label=r"\texttt{BubbleProfiler}", color="Green", lw=3)
    ax_1.plot(coord, action_exact, ':', label=r"Analytic", color="Blue", lw=3)
    ax_1.set_ylabel("Action, $S$")
    ax_1.legend(numpoints=1, fontsize=16, loc='best')
    ax_1.set_yscale('log')
    ax_1.set_xscale('log')
    ax_1.set_xlim(0.45, 0.8)

    ax_2 = plt.subplot(312, sharex=ax_1)
    ax_2.plot(coord, rdiff_ct, "--", label=r"\texttt{CosmoTransitions}", color="Brown", lw=3)
    ax_2.plot(coord, rdiff_bp, "-", label=r"\texttt{BubbleProfiler}", color="Green", lw=3)
    ax_2.set_ylabel("Relative difference")
    ax_2.set_yscale('log')
    ax_2.set_ylim(None, 1.)
    ax_2.legend(numpoints=1, fontsize=16, loc='best')

    if plot_time:

        ax_3 = plt.subplot(313, sharex=ax_1)
        ax_3.plot(coord, time_ct, '--', label=r"\texttt{CosmoTransitions}", color="Brown", lw=3)
        ax_3.plot(coord, time_bp, '-', label=r"\texttt{BubbleProfiler}", color="Green", lw=3)
        ax_3.legend(numpoints=1, fontsize=16, loc='best')
        ax_3.set_xlabel(coord_name)
        ax_3.set_ylabel(r"time (s)")
        ax_3.set_yscale('log')
        plt.setp(ax_2.get_xticklabels(), visible=False)

    else:

        ax_2.set_xlabel(coord_name)

    plt.setp(ax_1.get_xticklabels(), visible=False)

    plt.savefig(name)


def check_analytic_one_dim(potentials, action_exact, name, coord, coord_name):

    action_ct = []
    action_bp = []
    time_bp = []
    time_ct = []

    for potential in potentials:

        print "============================="
        print "potential = {}".format(potential)
        print "============================="

        results = bubblers(potential, dim=4, backends=['bubbleprofiler', 'cosmotransitions'])
        action_bp.append(results['bubbleprofiler'].action or 0.)
        action_ct.append(results['cosmotransitions'].action or 0.)
        time_bp.append(results['bubbleprofiler'].time)
        time_ct.append(results['cosmotransitions'].time)

        print results

    make_fig(action_ct, action_bp, action_exact, time_ct, time_bp, name, coord, coord_name)

if __name__ == "__main__":

    # Thin wall

    epsilons = np.logspace(-8, -1, 50, endpoint=False)
    analytic = [thin_wall(1., 1., epsilon) for epsilon in epsilons]
    potentials, action_exact = zip(*analytic)
    action_exact = np.array(action_exact)
    check_analytic_one_dim(potentials, action_exact, "thin_wall_from_interface.pdf", epsilons, r"$\epsilon$")

    # Logarithmic

    omegas = np.logspace(-4, 1, 50, endpoint=False)
    analytic = [logarithmic(1., omega) for omega in omegas]
    potentials, action_exact = zip(*analytic)
    action_exact = np.array(action_exact)
    check_analytic_one_dim(potentials, action_exact, "logarithmic_from_interface.pdf", omegas, r"$\omega$")

    # Fubini

    deltas = np.logspace(-4, 2, 50, endpoint=False)
    analytic = [fubini(1., 1., 1. + delta) for delta in deltas]
    potentials, action_exact = zip(*analytic)
    action_exact = np.array(action_exact)
    check_analytic_one_dim(potentials, action_exact, "fubini_from_interface.pdf", deltas, r"$\Delta m$")
