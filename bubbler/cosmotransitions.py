"""
Interface to CosmoTransitions
=============================

>>> ginac_potential = "-1. * ((4. * 0.502512562814 - 3.) / 2. * f^2 + f^3 - 0.502512562814 * f^4)"
>>> from potential import Potential
>>> solve(Potential(ginac_potential))
"""

import numpy as np

from cosmoTransitions.pathDeformation import fullTunneling
from timer import clock


def solve(potential, dim=3, **kwargs):
    """
    :param potential: Potential object or string
    :returns: Action, trajectory of bounce, time taken and extra information
    :rtype: tuple
    """
    def get_fields(cosmo_fields):
        """
        :returns: Fields without CosmoTransitions signature
        """
        return [cosmo_fields[..., i] for i in range(potential.n_fields)]

    def vector_potential(cosmo_fields):
        """
        :returns: Potential in CosmoTransitions signature
        """
        fields = get_fields(cosmo_fields)
        return potential(*fields)

    def vector_gradient(cosmo_fields):
        """
        :returns: Gradient in CosmoTransitions signature
        """
        fields = get_fields(cosmo_fields)
        cosmo_gradient = np.empty_like(cosmo_fields)
        cosmo_gradient[..., :] = potential.gradient(*fields).T
        return cosmo_gradient.astype(float)

    # Make initial guess of trajectory

    guess = np.empty([2, potential.n_fields])
    guess[0, :] = potential.true_vacuum
    guess[1, :] = potential.false_vacuum

    # Run CosmoTransitions

    with clock() as time:
        try:
            result = fullTunneling(guess,
                                   vector_potential,
                                   vector_gradient,
                                   tunneling_init_params={'alpha': dim - 1},
                                   deformation_deform_params={'verbose': False},
                                   **kwargs)
        except Exception as error:
            raise RuntimeError("CosmoTransitions crashed: {}".format(error))

    profile, fields, action = result[:3]

    # Reshape output and return

    rho = np.reshape(profile.R, (len(profile.R), 1))
    trajectory_data = np.hstack((rho, fields))

    return action, trajectory_data, time.time, fullTunneling.__name__

if __name__ == "__main__":
    import doctest
    doctest.testmod()
