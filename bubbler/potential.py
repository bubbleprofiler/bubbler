"""
Potential
=========

Represent a potential with a Python object:

>>> potential = Potential("0.1*((-x + 2)^4 - 14*(-x + 2)^2 + 24*(-x + 2))")

for fields:

>>> print potential.field_names

Evaluate the potential at particular values of the fields:

>>> print potential(10.)

Find minima:

>>> print potential.true_vacuum, potential.false_vacuum, potential.barrier

Plot a one-dimensional potential:

>>> potential.plot()

Make a one-dimensional potential

>>> one_dim_potential(1., 0.55)
"""

from sympy.utilities.lambdify import lambdify
from sympy import diff, sympify, latex
from sympy.solvers import nsolve, solve

import matplotlib.pyplot as plt
import numpy as np


class Potential(object):
    """
    Scalar potential from ginac string.
    """
    def __init__(self,
                 ginac_potential,
                 true_vacuum=None,
                 false_vacuum=None,
                 barrier=None):
        """
        :param potential: Potential as ginac string
        """
        self.ginac_potential = ginac_potential
        self._sympy_potential = sympify(self.ginac_potential)
        self.field_names = list(self._sympy_potential.free_symbols)
        self.n_fields = len(self.field_names)
        self._potential = lambdify(self.field_names, self._sympy_potential)

        self._sympy_gradient = [diff(self._sympy_potential, f)
                                for f in self.field_names]
        self._gradient_functions = [lambdify(self.field_names, gradient)
                                    for gradient in self._sympy_gradient]

        if true_vacuum and false_vacuum and barrier:

            self.true_vacuum = self._nsolve(true_vacuum)
            self.false_vacuum = self._nsolve(false_vacuum)
            self.barrier = self._nsolve(barrier)

        else:

            self.true_vacuum = self._solve[0]
            self.false_vacuum = self._solve[1]
            self.barrier = self._solve[2]

        self.potential_latex = "$V = {}$".format(latex(self._sympy_potential))
        self.field_latex = [latex(n, mode="inline") for n in self.field_names]

    def _nsolve(self, guess):
        """
        :returns: Numerical solution to tapdole equations
        """
        sol = nsolve(self._sympy_gradient, self.field_names, guess)
        return np.array([float(s) for s in sol])

    @property
    def _solve(self):
        """
        :returns: Analytic solution to tapdole equations
        """
        extrema = solve(self._sympy_gradient, self.field_names, dict=True)
        assert len(extrema) == 3
        extrema = sorted(extrema, key=self._sympy_potential.subs)
        return [np.array([extreme[n] for n in self.field_names]).astype(float)
                for extreme in extrema]

    def gradient(self, *fields):
        """
        :returns: Gradient of potential
        """
        return np.array([gradient(*fields)
                         for gradient in self._gradient_functions])

    def __call__(self, *fields):
        """
        :returns: Potential
        """
        return self._potential(*fields)

    def plot(self):
        """
        Plot a one-dimensional potential
        """
        assert self.n_fields == 1
        field = np.linspace(self.true_vacuum[0], self.false_vacuum[0], 1000)
        plt.plot(field, self(field), c='Crimson', lw=3)
        plt.xlabel(self.field_latex[0])
        plt.ylabel(self.potential_latex)
        plt.show()

class one_dim_potential(Potential):
    """
    One-dimensional potential
    """
    def __init__(self, E, alpha):
        """
        :param E: Scale of one-dimensional potential
        :type E: float
        :param alpha: Shape of one-dimensional potential
        :type alpha: float
        """
        assert 0.5 <= alpha <= 0.75
        assert E > 0.

        self.E = E
        self.alpha = alpha

        potential = "-{1} * ((4. * {0} - 3.) / 2. * f^2 + f^3 - {0} * f^4)".format(alpha, E)

        super(one_dim_potential, self).__init__(potential,
                                                true_vacuum=[1.],
                                                false_vacuum=[0.])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
