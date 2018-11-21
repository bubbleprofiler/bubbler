"""
Compare results from different codes for a one-dimensional potential
====================================================================
"""


import numpy as np

from bubbler import one_dim_bubblers
from quartic_from_files import make_fig


alphas = np.linspace(0.5, 0.75, 500, endpoint=False)
E = 1.


action_ct = []
action_bp = []
time_bp = []
time_ct = []


for alpha in alphas:

    print "============================="
    print "alpha = {}".format(alpha)
    print "============================="

    results = one_dim_bubblers(E, alpha,
                               backends=['bubbleprofiler', 'cosmotransitions'])
    action_bp.append(results['bubbleprofiler'].action)
    action_ct.append(results['cosmotransitions'].action)
    time_bp.append(results['bubbleprofiler'].time)
    time_ct.append(results['cosmotransitions'].time)

    print results


make_fig(action_ct, action_bp, time_ct, time_bp, "quartic_from_interface.pdf")
