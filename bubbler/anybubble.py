"""
Interface to AnyBubble
======================

>>> ginac_potential = "0.1*((-x + 2)^4 - 14*(-x + 2)^2 + 24*(-x + 2))"
>>> from potential import Potential
>>> print solve(Potential(ginac_potential))
"""

import os
import tempfile
import numpy as np
from subprocess32 import check_output


SCRIPT = """
#!/usr/bin/env wolframscript
SetDirectory["{0}"]
<< anybubble`
potential = ToExpression["{1}"];
{{time, sol}} = Timing[FindBubble[potential, q, {2}, {3}, SpaceTimeDimension -> {4}, PowellVerbosity -> 0, Verbose -> False]];
action = sol[[1]];
R = Subdivide[0, 100, 1000] // N;
fields = Map[sol[[2]], R];
traj = MapThread[Append, {{fields, R}}];
Export["{5}/traj.txt", traj, "Table"];
Export["{5}/action.txt", action // CForm];
Export["{5}/time.txt", time // CForm];
Quit[];
"""

def curly(array):
    """
    :returns: Array as a Mathematica string
    """
    return str(array.tolist()).replace('[', '{').replace(']', '}')

def solve(potential, output=None, dim=3, **kwargs):
    """
    :returns: Action, trajectory of bounce and time taken
    :rtype: tuple
    """

    output = output if output else tempfile.mkdtemp()

    # Make extrema in Mathematica format

    true_vacuum = curly(potential.true_vacuum)
    false_vacuum = curly(potential.false_vacuum)

    # Make Mathematica script that solves this problem

    script = SCRIPT.format(os.environ["ANYBUBBLE"],
                           potential.mathematica_potential,
                           true_vacuum,
                           false_vacuum,
                           dim,
                           output)

    script_file = "{}/anybubble.ws".format(output)

    with open(script_file, "w") as f:
        f.write(script)

    # Execute Mathematica script

    command = 'math -script {}'.format(script_file)

    try:
        check_output(command, shell=True)
    except Exception as error:
        raise RuntimeError("AnyBubble crashed: {}".format(error))

    # Read action, time and trajectory from text files

    trajectory_file = "{}/traj.txt".format(output)
    trajectory_data = np.loadtxt(trajectory_file)

    new_order = [potential.n_fields] + list(range(potential.n_fields))
    trajectory_data = trajectory_data[:, new_order]

    action_file = "{}/action.txt".format(output)
    action = float(np.loadtxt(action_file))

    time_file = "{}/time.txt".format(output)
    time = float(np.loadtxt(time_file))

    return action, trajectory_data, time, command

if __name__ == "__main__":
    import doctest
    doctest.testmod()
