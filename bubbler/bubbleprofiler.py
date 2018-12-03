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

    template = ("{loc}/bin/run_cmd_line_potential --force-output --write-profiles "
                "--potential '{ginac_potential}' "
                "{field_names} "
                "--output-file {output} "
                "--grid-points {n_spline_samples} "
                "--knots {n_knots} "
                "--domain-start {rho_min} "
                "--domain-end {rho_max} "
                "{false_vacuum} "
                "{true_vacuum} "
                "--rtol-action {rtol_action} "
                "--rtol-fields {rtol_fields} "
                "--integration-method {int_method} "
                "--n-dims {dim}"
                "{shooting_str}"
                " > /dev/null 2>&1")

    command = template.format(loc=os.environ["BUBBLEPROFILER"],
                              ginac_potential=potential.ginac_potential,
                              field_names=field_names,
                              output=output,
                              n_spline_samples=n_spline_samples,
                              n_knots=n_knots,
                              rho_min=rho_min,
                              rho_max=rho_max,
                              false_vacuum=false_vacuum,
                              true_vacuum=true_vacuum,
                              rtol_action=rtol_action,
                              rtol_fields=rtol_fields,
                              int_method=int_method,
                              dim=dim,
                              shooting_str=shooting_str)

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
