"""
Compare results from different codes for a one-dimensional potential
====================================================================
"""

from bubbler import bubblers, profiles, Potential

import numpy as np
import matplotlib.pyplot as plt


potential = "-1. * ((4. * {0} - 3.) / 2. * f^2 + f^3 - {0} * f^4)"
alphas = np.linspace(0.5, 0.75, 500, endpoint=False)

action_ct = []
action_bp = []
end_ct = []
end_bp = []
time_bp = []
time_ct = []


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
    time_bp.append(results['bubbleprofiler'].time)
    time_ct.append(results['cosmotransitions'].time)
    
    for result in results.itervalues():
        print "backend = {}. action = {}".format(result.backend, result.action)
        print "command = ", result.command



rdiff = [(a - b) / a if a and b else 1E5 for a, b in zip(action_ct, action_bp)]

fig = plt.figure()
plt.subplots_adjust(hspace=0.1)

ax_1 = plt.subplot(411)
ax_1.plot(alphas, action_ct, '--', label="CosmoTransitions", color="Brown", lw=2)
ax_1.plot(alphas, action_bp, '-', label="BubbleProfiler", color="Green", lw=2)
ax_1.set_ylabel("$S$")
ax_1.legend(numpoints=1, fontsize=12, loc='best')
ax_1.set_yscale('log')

ax_2 = plt.subplot(412, sharex=ax_1)
ax_2.plot(alphas, rdiff, '--', color="Crimson", lw=2)
ax_2.set_ylabel("rdiff")
ax_2.set_yscale('log')

ax_3 = plt.subplot(413, sharex=ax_1)
ax_3.plot(alphas, end_ct, '--', label="CosmoTransitions", color="Crimson", lw=2)
ax_3.plot(alphas, end_bp, '-', label="BubbleProfiler", color="Green", lw=2)
ax_3.legend(numpoints=1, fontsize=12, loc='best')
ax_3.set_ylabel(r"Max $\rho$")

ax_4 = plt.subplot(414, sharex=ax_1)
ax_4.plot(alphas, time_ct, '--', label="CosmoTransitions", color="Crimson", lw=2)
ax_4.plot(alphas, time_bp, '-', label="BubbleProfiler", color="Green", lw=2)
ax_4.set_xlabel(r"$\alpha$")
ax_4.legend(numpoints=1, fontsize=12, loc='best')
ax_4.set_ylabel(r"time (s)")
ax_4.set_yscale('log')

plt.setp(ax_1.get_xticklabels(), visible=False)
plt.setp(ax_2.get_xticklabels(), visible=False)
plt.setp(ax_3.get_xticklabels(), visible=False)
plt.savefig("alpha_tests.pdf")
