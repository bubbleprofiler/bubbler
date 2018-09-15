"""
Pass Michael's potential through our codes
==========================================

You need to export a few paths for this script:

export BUBBLEPROFILER=/PATH/TO/BubbleProfiler/
export ANYBUBBLE=/PATH/TO/AnyBubble
export PYTHONPATH=/PATH/TO/CosmoTransitions:/PATH/TO/BubbleProfiler/examples/sm-plus-singlet
"""

from bubbler import bubblers, Potential
from sm_plus_singlet import generate_potential

# Works

T = 85.
Tc = 110.
lambda_m = 1.5
lambda_s = 0.688259

# Fails

# lambda_s = 1.76759

p_dict = generate_potential(T, Tc, lambda_m, lambda_s)
tv = p_dict["true_vac"][::-1]  # Reverse them as my code likes the fields in alphabetical order!
fv = p_dict["false_vac"][::-1]
p = p_dict["potential_str"]

potential = Potential(p, true_vacuum=tv, false_vacuum=fv)

results = bubblers(potential, backends=["cosmotransitions", "bubbleprofiler", "anybubble"])

for result in results.itervalues():
    print "backend = {}. action = {}. time = {}".format(result.backend, result.action, result.time)
    print "command = {}".format(result.command)
