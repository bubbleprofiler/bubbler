"""
Compare results from different codes
====================================
"""

from bubbler import bubblers
from bubbler import Potential


ginac_potentials = [None,
                    "0.1*((-x + 2)^4 - 14*(-x + 2)^2 + 24*(-x + 2))",
                    "(x^2 + y^2) * (1.8 * (x - 1)^2 + 0.2 * (y - 1)^2 - 0.04)",
                    "(-0.284821 + 0.684373 * (-1 + x)^2 + 0.181928 * (-1 + y)^2 + 0.295089 * (-1 + z)^2) * (x^2 + y^2 + z^2)",
                    "(-0.258889 + 0.534808*(-1 + t)^2 + 0.77023*(-1 + x)^2 + 0.838912*(-1 + y)^2 + 0.00517238*(-1 + z)^2)*(t^2 + x^2 + y^2 + z^2)",
                    "(-0.658889 + 0.4747*(-1 + s)^2 + 0.234808*(-1 + t)^2 + 0.57023*(-1 + x)^2 + 0.138912*(-1 + y)^2 + 0.517238*(-1 + z)^2)*(s^2 + t^2 + x^2 + y^2 + z^2)",
                    "(-0.658889 + 0.34234*(-1 + p)^2 + 0.4747*(-1 + s)^2 + 0.234808*(-1 + t)^2 + 0.57023*(-1 + x)^2 + 0.138912*(-1 + y)^2 + 0.517238*(-1 + z)^2)*(p^2 + s^2 + t^2 + x^2 + y^2 + z^2)",
                    "(-0.658889 + 0.5233*(-1 + r)^2 + 0.34234*(-1 + p)^2 + 0.4747*(-1 + s)^2 + 0.234808*(-1 + t)^2 + 0.57023*(-1 + x)^2 + 0.138912*(-1 + y)^2 + 0.517238*(-1 + z)^2)*(r^2 + p^2 + s^2 + t^2 + x^2 + y^2 + z^2)",
                    "(-0.658889 + 0.2434*(-1 + q)^2 + 0.5233*(-1 + r)^2 + 0.34234*(-1 + p)^2 + 0.4747*(-1 + s)^2 + 0.234808*(-1 + t)^2 + 0.57023*(-1 + x)^2 + 0.138912*(-1 + y)^2 + 0.517238*(-1 + z)^2)*(q^2 + r^2 + p^2 + s^2 + t^2 + x^2 + y^2 + z^2)",
                    None,
                    "(-0.658889 + 0.28765*(-1 + b)^2 + 0.7345*(-1 + a)^2 + 0.2434*(-1 + q)^2 + 0.5233*(-1 + r)^2 + 0.34234*(-1 + p)^2 + 0.4747*(-1 + s)^2 + 0.234808*(-1 + t)^2 + 0.57023*(-1 + x)^2 + 0.138912*(-1 + y)^2 + 0.517238*(-1 + z)^2)*(a^2 + b^2 + q^2 + r^2 + p^2 + s^2 + t^2 + x^2 + y^2 + z^2)",
              ]

for n_fields, ginac_potential in enumerate(ginac_potentials):

    if ginac_potential is None:
        continue

    if n_fields > 1:
        potential = Potential(ginac_potential, true_vacuum=[1.] * n_fields, barrier=[0.5] * n_fields, false_vacuum=[0.] * n_fields)
    else:
        potential = Potential(ginac_potential)

    results = bubblers(potential, backends=["cosmotransitions", "bubbleprofiler"])

    print "============================="
    print "{} fields".format(n_fields)
    print "=============================" 
    
    for result in results:
        print "backend = {}. action = {}. time = {}".format(result.backend, result.action, result.time)
        print "command = {}".format(result.command)
