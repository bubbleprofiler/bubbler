"""
Interface to AnyBubble
======================

>>> ginac_potential = "0.1*((-x + 2)^4 - 14*(-x + 2)^2 + 24*(-x + 2))"
>>> from potential import Potential
>>> print solve(Potential(ginac_potential))
"""


from timer import clock
from subprocess32 import check_output
import os
import numpy as np
import tempfile



SCRIPT = """
#!/usr/bin/env wolframscript
SetDirectory["{0}"]
<< anybubble`
potential = ToExpression["{1}"];
sol = FindBubble[potential, chi, {2}, {3}, SpaceTimeDimension -> {4}, PowellVerbosity -> 0, Verbose -> False];
action = sol[[1]];
R = Subdivide[0, 100, 1000] // N;
fields = Map[sol[[2]], R];
traj = MapThread[Append, {{fields, R}}];
Export["{5}/traj.txt", traj, "Table"];
Export["{5}/action.txt", action];
Quit[];
"""


def solve(potential, output=None, dim=3, **kwargs):
    """
    :returns: Action, trajectory of bounce and time taken
    :rtype: tuple
    """

    output = output if output else tempfile.mkdtemp()

    # Make potential in Mathematica format

    math_potential = potential.ginac_potential

    for i, n in enumerate(potential.field_names):
        math_potential = math_potential.replace(str(n), "chi[{}]".format(i + 1))

    # Make extrema in Mathematica format

    curly = lambda array: str(array.tolist()).replace('[', '{').replace(']', '}')
    true_vacuum = curly(potential.true_vacuum)
    false_vacuum = curly(potential.false_vacuum)

    # Make Mathematica script that solves this problem

    script = SCRIPT.format(os.environ["ANYBUBBLE"],
                           math_potential,
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
        with clock() as time:
            check_output(command, shell=True)
    except Exception as error:
        raise RuntimeError("AnyBubble crashed: {}".format(error))

    # Read action and trajectory from text files

    trajectory_file = "{}/traj.txt".format(output)
    trajectory_data = np.loadtxt(trajectory_file)

    new_order = [potential.n_fields] + list(range(potential.n_fields))
    trajectory_data = trajectory_data[:, new_order]

    action_file = "{}/action.txt".format(output)
    action = float(np.loadtxt(action_file))

    return action, trajectory_data, time.time, command

if __name__ == "__main__":
    import doctest
    doctest.testmod()
