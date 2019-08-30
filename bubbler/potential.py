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

>>> print potential.true_vacuum, potential.false_vacuum

Plot a one-dimensional potential:

>>> potential.plot()

Make a one-dimensional potential

>>> one_dim_potential(1., 0.55)
"""

from sympy.utilities.lambdify import lambdify
from sympy import diff, sympify, latex
from sympy.solvers import nsolve, solve
from sympy.printing.cxxcode import cxxcode

import matplotlib.pyplot as plt
import numpy as np
import re


class Potential(object):
    """
    Scalar potential from ginac string.
    """
    def __init__(self,
                 ginac_potential,
                 true_vacuum=None,
                 false_vacuum=None,
                 polish=True):
        """
        :param potential: Potential as ginac string
        """
        self.ginac_potential = ginac_potential
        self._sympy_potential = sympify(self.ginac_potential)
        self.field_names = list(self._sympy_potential.free_symbols)
        self.field_names_str = map(str, self.field_names)
        self.n_fields = len(self.field_names)
        self._potential = lambdify(self.field_names, self._sympy_potential)

        self._sympy_gradient = [diff(self._sympy_potential, f)
                                for f in self.field_names]
        self._gradient_functions = [lambdify(self.field_names, gradient)
                                    for gradient in self._sympy_gradient]

        if polish and true_vacuum is not None:
            self.true_vacuum = self._nsolve(true_vacuum)
        elif true_vacuum is not None:
            self.true_vacuum = np.atleast_1d(true_vacuum)
        else:
            self.true_vacuum = self._solve[0]

        if polish and false_vacuum is not None:
            self.false_vacuum = self._nsolve(false_vacuum)
        elif true_vacuum is not None:
            self.false_vacuum = np.atleast_1d(false_vacuum)
        else:
            self.false_vacuum = self._solve[1]

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
        assert len(extrema) >= 3
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

    def names_to_array(self, string, array_name="q", zero_based=True):
        """
        :returns: String with field names replaced by an indexed array
        """
        shift = 0 if zero_based else 1

        for i, name in enumerate(self.field_names_str):
            if array_name in name:
                raise ValueError("Field name cannot contain {}".format(array_name))
            find = r"(\W)({})(\W)".format(name)
            replace = r"\1{}[{}]\3".format(array_name, i + shift)
            string = re.sub(find, replace, string)

        return string

    @property
    def mathematica_potential(self):
        """
        @returns Potential in Mathematica format
        """
        return self.names_to_array(self.ginac_potential, zero_based=False)

    @property
    def c_potential(self):
        """
        @returns Potential in C format
        """
        return self.names_to_array(cxxcode(self.ginac_potential))

    @property
    def c_gradient(self, pattern="dvdq[{}] = {};"):
        """
        @returns Gradient in very particlar C format
        """
        lines = [pattern.format(i, cxxcode(g)) for i, g in enumerate(self._sympy_gradient)]
        joined = "\n".join(lines)
        return self.names_to_array(joined)

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

    def __str__(self):
        return self.ginac_potential

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
