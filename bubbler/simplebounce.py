"""
Interface to SimpleBounce
=========================

You need to export SIMPLEBOUNCE=/your/path/to/SimpleBounce

>>> ginac_potential = "0.1*((-x + 2)^4 - 14*(-x + 2)^2 + 24*(-x + 2))"
>>> from potential import Potential
>>> print solve(Potential(ginac_potential))
"""

import os
import numpy as np
from subprocess32 import check_output
from StringIO import StringIO

from anybubble import curly
from timer import clock


CODE = """
#include<iostream>
#include <cmath>
#include "simplebounce.h"

using namespace std;
using namespace simplebounce;

class BubblerModel : public GenericModel {{
  public:
	BubblerModel() {{
		setNphi({0});
	}}
	double vpot (const double* q) const {{
		return {1};
	}}
	void calcDvdphi(const double *q, double *dvdq) const {{
		{2}
	}}
}};

int main() {{

  // Settings from example provided with code
	BounceCalculator bounce;
	bounce.verboseOff();
	bounce.setRmax(1.);
	bounce.setN(100);
	BubblerModel model;
	bounce.setModel(&model);

  // Contains our input
	bounce.setDimension({3});
	double phiTV[{0}] = {4};
	double phiFV[{0}] = {5};

	bounce.setVacuum(phiTV, phiFV);
	bounce.solve();
	bounce.printBounce();
	std::cout << bounce.action();

	return 0;
}}
"""

def solve(potential, dim=3, **kwargs):
    """
    :returns: Action, trajectory of bounce and time taken
    :rtype: tuple
    """
    # Make extrema in C format

    true_vacuum = curly(potential.true_vacuum)
    false_vacuum = curly(potential.false_vacuum)

    # Make C program that solves this problem

    code = CODE.format(potential.n_fields,
                       potential.c_potential,
                       potential.c_gradient,
                       dim,
                       true_vacuum,
                       false_vacuum)

    # Build C program

    code_file = "{}/bubbler.cc".format(os.environ["SIMPLEBOUNCE"])

    with open(code_file, "w") as f:
        f.write(code)

    make = "make -C {} bubbler.x".format(os.environ["SIMPLEBOUNCE"])

    try:
        check_output(make, shell=True)
    except Exception as error:
        raise RuntimeError("SimpleBounce build crashed: {}".format(error))

    # Execute C program

    command = "{}/bubbler.x".format(os.environ["SIMPLEBOUNCE"])

    with clock() as time:
        try:
            output = check_output(command, shell=True)
        except Exception as error:
            raise RuntimeError("SimpleBounce crashed: {}".format(error))

    # Parse output

    lines = output.split("\n")
    action = float(lines[-1])

    parsed = "\n".join(lines[1:-1])
    traj = np.genfromtxt(StringIO(parsed), dtype=float)[:, :-1]

    return action, traj, time.time, command

if __name__ == "__main__":
    import doctest
    doctest.testmod()
