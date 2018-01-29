"""
Compare results from different codes for a one-dimensional potential
====================================================================
"""

from bubbler import bubblers

import numpy as np
import matplotlib.pyplot as plt


potential = "-1. * ((4. * {0} - 3.) / 2. * f^2 + f^3 - {0} * f^4)"
alphas = np.linspace(0.5, 0.75, 50, endpoint=False)

action_ct = []
action_bp = []
end_ct = []
end_bp = []


for alpha in alphas:

    print "============================="
    print "alpha = {}".format(alpha)
    print "============================="

    results = bubblers(potential.format(alpha),
                       backends=['bubbleprofiler', 'cosmotransitions'])

    action_bp.append(results['bubbleprofiler'].action)
    action_ct.append(results['cosmotransitions'].action)
    end_bp.append(results['bubbleprofiler'].rho_end)
    end_ct.append(results['cosmotransitions'].rho_end)
    
    for result in results.itervalues():
        print "backend = {}. action = {}".format(result.backend, result.action)
        print "command = ", result.command


rdiff = [(a - b) / a if a and b else 1E5 for a, b in zip(action_ct, action_bp)]

fig = plt.figure()
plt.subplots_adjust(hspace=0.1)

ax_1 = plt.subplot(311)
ax_1.plot(alphas, action_ct, '--', label="CosmoTransitions", color="Brown", lw=2)
ax_1.plot(alphas, action_bp, '-', label="BubbleProfiler", color="Green", lw=2)
ax_1.set_ylabel("Action, $S$")
ax_1.legend(numpoints=1, fontsize=12, loc='best')
ax_1.set_yscale('log')

ax_2 = plt.subplot(312, sharex=ax_1)
ax_2.plot(alphas, rdiff, '--', color="Crimson", lw=2)
ax_2.set_ylabel("Relative difference")
ax_2.set_yscale('log')

ax_3 = plt.subplot(313, sharex=ax_1)
ax_3.plot(alphas, end_ct, '--', label="CosmoTransitions", color="Crimson", lw=2)
ax_3.plot(alphas, end_bp, '-', label="BubbleProfiler", color="Green", lw=2)
ax_3.set_xlabel(r"$\alpha$")
ax_3.legend(numpoints=1, fontsize=12, loc='best')
ax_3.set_ylabel(r"Maximum value of $\rho$")

plt.setp(ax_1.get_xticklabels(), visible=False)
plt.setp(ax_2.get_xticklabels(), visible=False)
plt.savefig("alpha_tests.pdf")
