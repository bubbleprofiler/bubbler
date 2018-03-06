"""
Interface to shooting
=====================

>>> from potential import one_dim_potential
>>> solve(one_dim_potential(1., 0.65))
"""


from timer import clock
import pyshooting


def solve(one_dim_potential, dim=3, **kwargs):
    """
    :returns: Action and time taken
    :rtype: tuple
    """

    assert dim == 3, "dim = 3 only at the moment"

    try:
        with clock() as time:
            action = pyshooting.action(one_dim_potential.E, one_dim_potential.alpha)
    except Exception as error:
        raise RuntimeError("Shooting crashed: {}".format(error))

    return action, None, time.time, pyshooting.action.__name__

if __name__ == "__main__":
    import doctest
    doctest.testmod()
