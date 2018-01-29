"""
Interfaces and comparison for various Bubbler codes
===================================================

Define a potential by a ginac string:

>>> ginac_potential = "0.1*((-x + 2)^4 - 14*(-x + 2)^2 + 24*(-x + 2))"

Solve it with a particular code:

>>> print bubbler(ginac_potential)

Solve it with all codes:

>>> print bubblers(ginac_potential)

Plot results from a few codes:

>>> profiles(ginac_potential)

Look at a one-dimensional potential:

>>> one_dim_bubblers(1., 0.6)
"""

from collections import namedtuple
from itertools import cycle
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np


from potential import Potential, one_dim_potential
import cosmotransitions
import bubbleprofiler
import anybubble


BACKENDS = ["cosmotransitions", "bubbleprofiler", "anybubble"]

attributes = ['backend', 'action', 'trajectory', 'rho_end', 'time', 'command']
Solution = namedtuple('Solution', attributes)

interp = lambda x, y: interp1d(x, y, fill_value=(y[0], y[-1]), bounds_error=False)


def bubbler(potential, backend="cosmotransitions", **kwargs):
    """
    :param potential: Potential object or string
    :param backend: Code with which to solve bounce
    :returns: Results from a particular code
    :rtype: namedtuple
    """
    try:

        # Call function

        module = globals()[backend]
        potential = Potential(potential) if isinstance(potential, str) else potential
        action, trajectory_data, time, command = module.solve(potential, **kwargs)

        # Make interpolation function from output

        trajectory = [interp(trajectory_data[:, 0], trajectory_data[:, i + 1])
                      for i in range(potential.n_fields)]

        # Find maximum value of rho

        rho_end = trajectory_data[-1, 0]

        return Solution(backend, action, trajectory, rho_end, time, command)

    except Exception as error:

        return Solution(backend, None, None, None, None, error.message)

def bubblers(potential, backends=None):
    """
    :param potential: Potential object or string
    :param backend: Code with which to solve bounce
    :returns: Results from all codes
    :rtype: list of namedtuple
    """
    potential = Potential(potential) if isinstance(potential, str) else potential
    backends = backends if backends else BACKENDS
    return {backend: bubbler(potential, backend=backend) for backend in backends}

def profiles(potential, backends=None, **kwargs):
    """
    :param potential: Potential object or string

    Plots field profiles for all codes.
    """
    potential = Potential(potential) if isinstance(potential, str) else potential
    results = bubblers(potential, backends, **kwargs)

    # Make profile plot

    fig, ax = plt.subplots()
    colors = cycle(["Brown", "Green", "Blue"])

    for result in results.itervalues():

        if not result.action:
            continue

        color = next(colors)
        lines = cycle(["-", "--", "-."])
        rho = np.linspace(0, result.rho_end, 1000)

        for name, trajectory in zip(potential.field_latex, result.trajectory):
            ax.plot(rho,
                    trajectory(rho),
                    ls=next(lines),
                    c=color,
                    lw=3,
                    label="{} from {}".format(name, result.backend),
                    alpha=0.8)

    # Plot true vacuum

    markers = cycle(["^", "p", "*"])

    for name, field in zip(potential.field_latex, potential.true_vacuum):
        ax.plot(0.,
                field,
                next(markers),
                c="Gold",
                label="True vacuum for {}".format(name),
                ms=10,
                clip_on=False,
                zorder=10)

    # Labels etc

    ax.set_xlabel(r"$\rho$")
    ax.set_ylabel(r"$\phi$")
    leg = ax.legend(numpoints=1, fontsize=12, loc='best')
    leg.get_frame().set_alpha(0.5)
    ax.set_title(potential.potential_latex)

    plt.show()

def one_dim_bubblers(E, alpha, backends=None):
    """
    :param E: Scale of one-dimensional potential
    :type E: float
    :param alpha: Shape of one-dimensional potential
    :type alpha: float

    :returns: Result from one-dimensional potential parameterised by
    E and alpha.
    :rtype: list of namedtuple
    """
    return bubblers(one_dim_potential(E, alpha), backends)

def one_dim_profiles(E, alpha, backends=None):
    """
    :param E: Scale of one-dimensional potential
    :type E: float
    :param alpha: Shape of one-dimensional potential
    :type alpha: float

    Plots field profiles for all codes.
    """
    return profiles(one_dim_potential(E, alpha), backends=backends)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
