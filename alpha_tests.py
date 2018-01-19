"""
Compare results from different codes for a one-dimensional potential
====================================================================
"""

from bubbler import bubblers

import numpy as np
import matplotlib.pyplot as plt


potential = "-1. * ((4. * {0} - 3.) / 2. * f^2 + f^3 - {0} * f^4)"
alphas = np.linspace(0.5, 0.75, 500, endpoint=False)

data = {'bubbleprofiler': [], 'cosmotransitions': [], 'rdiff': []}

for alpha in alphas:

    print "============================="
    print "alpha = {}".format(alpha)
    print "============================="

    results = bubblers(potential.format(alpha),
                       backends=['bubbleprofiler', 'cosmotransitions'])

    for result in results:
        data[result.backend].append(result.action)
        print "backend = {}. action = {}".format(result.backend, result.action)
        print "command = ", result.command

    if data['bubbleprofiler'][-1] and data['cosmotransitions'][-1]:
        rdiff = abs(data['bubbleprofiler'][-1] - data['cosmotransitions'][-1]) / data['cosmotransitions'][-1]
    else:
        rdiff = 1E5

    data['rdiff'].append(rdiff)


fig = plt.figure()
plt.subplots_adjust(hspace=0.1)

ax_1 = plt.subplot(211)
ax_1.plot(alphas, data['cosmotransitions'], '--', label="CosmoTransitions", color="Brown", lw=2)
ax_1.plot(alphas, data['bubbleprofiler'], '-', label="BubbleProfiler", color="Green", lw=2)
ax_1.set_ylabel("Action, $S$")
ax_1.legend(numpoints=1, fontsize=12, loc='best')
ax_1.set_yscale('log')

ax_2 = plt.subplot(212, sharex=ax_1)
ax_2.plot(alphas, data['rdiff'], '--', color="Crimson", lw=2)
ax_2.set_xlabel(r"$\alpha$")
ax_2.set_ylabel("Relative difference")
ax_2.set_yscale('log')

plt.setp(ax_1.get_xticklabels(), visible=False)
plt.savefig("alpha_tests.pdf")
