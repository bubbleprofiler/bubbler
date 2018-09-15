"""
Interface to BubbleProfiler
===========================

>>> ginac_potential = "0.1*((-x + 2)^4 - 14*(-x + 2)^2 + 24*(-x + 2))"
>>> from potential import Potential
>>> solve(Potential(ginac_potential))
"""

import os
import tempfile
import numpy as np
from subprocess32 import check_call

from timer import clock


def solve(potential,
          output=None,
          n_spline_samples=1000,
          n_knots=100,
          rho_min=-1.,
          rho_max=-1.,
          rtol_action=1E-3,
          rtol_fields=1E-3,
          int_method='runge-kutta-4',
          shooting=True,
          dim=3):
    """
    :param potential: Potential object or string
    :returns: Action, trajectory of bounce, time taken and extra information
    :rtype: tuple
    """

    assert dim == 3, "dim = 3 only at the moment"

    if potential.n_fields > 1:
        shooting = False

    # System call to BubblerProfiler executable

    shooting_str = "" if shooting else "--perturbative"

    output = output if output else tempfile.mkstemp()[1]

    field_names = " ".join(["--field '{}'".format(n)
                            for n in potential.field_names])
    false_vacuum = " ".join(["--local-minimum {}".format(v)
                             for v in potential.false_vacuum])
    true_vacuum = " ".join(["--global-minimum {}".format(v)
                            for v in potential.true_vacuum])

    template = ("{0}/bin/run_cmd_line_potential --force-output --write-profiles "
                "--potential '{1}' "
                "{2} "
                "--output-file {3} "
                "--grid-points {4} "
                "--knots {5} "
                "--domain-start {6} "
                "--domain-end {7} "
                "{8} "
                "{9} "
                "--rtol-action {10} "
                "--rtol-fields {11} "
                "--integration-method {12} "
                "{13}"
                "> /dev/null 2>&1")

    command = template.format(os.environ["BUBBLEPROFILER"],
                              potential.ginac_potential,
                              field_names,
                              output,
                              n_spline_samples,
                              n_knots,
                              rho_min,
                              rho_max,
                              false_vacuum,
                              true_vacuum,
                              rtol_action,
                              rtol_fields,
                              int_method,
                              shooting_str)

    try:
        with clock() as time:
            check_call(command, shell=True)
    except Exception as error:
        raise RuntimeError("BubbleProfiler crashed: {}".format(error))

    # Read action

    with open(output) as f:
      action_line = f.readline()
    action = float(action_line.split(":")[-1])

    # Read fields

    trajectory_data = np.loadtxt(output)

    return action, trajectory_data, time.time, command

if __name__ == "__main__":
    import doctest
    doctest.testmod()
