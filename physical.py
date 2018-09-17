"""
Pass Michael's potential through our codes
==========================================

You need to export a few paths for this script:

export BUBBLEPROFILER=/PATH/TO/BubbleProfiler/
export ANYBUBBLE=/PATH/TO/AnyBubble
export PYTHONPATH=/PATH/TO/CosmoTransitions:/PATH/TO/BubbleProfiler/examples/sm-plus-singlet
"""

import numpy as np

from bubbler import bubblers, Potential
from sm_plus_singlet import generate_potential


BACKENDS = ["cosmotransitions", "bubbleprofiler", "anybubble"]


def physical(T, T_C, lambda_m, lambda_s, backends=None):

    p_dict = generate_potential(T, T_C, lambda_m, lambda_s)
    tv = p_dict["true_vac"][::-1]  # Reverse them as my code likes the fields in alphabetical order!
    fv = p_dict["false_vac"][::-1]
    p = p_dict["potential_str"]

    potential = Potential(p, true_vacuum=tv, false_vacuum=fv)

    backends = BACKENDS if not backends else backends
    results = bubblers(potential, backends=backends)

    return results


if __name__ == "__main__":

    # Works for all codes

    print physical(85., 110., 1.5, 0.688259)

    # Fails for us

    print physical(85., 110., 1.5,  1.76759)

    # Scan in coupling and check for failures

    lambda_ = np.linspace(0., 2., 100)

    n_total = 0
    n_b = 0
    n_c = 0

    for l in lambda_:

        try:
            r = physical(85., 110., 1.5, l, backends=["cosmotransitions", "bubbleprofiler"])
        except:
            continue

        n_total += 1

        if r["bubbleprofiler"].action is not None:
            n_b += 1
        if r["cosmotransitions"].action is not None:
            n_c += 1

    print "cosmo", n_c, n_total
    print "us", n_b, n_total
