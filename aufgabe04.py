import ctypes as ct
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as mpl
from itertools import product
from math import log, log10

_libint = np.ctypeslib.load_library('libintegrate', 'build')

func_type = ct.CFUNCTYPE(ct.c_double, ct.c_double)
int_p = ct.POINTER(ct.c_int)

_libint.integrate_trapezoidal.restype = ct.c_double
_libint.integrate_trapezoidal.argtypes = [func_type,
                                          ct.c_double,
                                          ct.c_double,
                                          ct.c_int]

_libint.integrate_romberg.restype = ct.c_double
_libint.integrate_romberg.argtypes = [func_type,
                                      ct.c_double,
                                      ct.c_double,
                                      ct.c_int,
                                      int_p,
                                      int_p]

def integrate_trapezoidal(f, a, b, n):
    return _libint.integrate_trapezoidal(func_type(f), a, b, n)

def integrate_romberg(f, a, b, n, operations=False):
    calls, ops = ct.c_int(0), ct.c_int(0)
    res = _libint.integrate_romberg(
                func_type(f), a, b, n, ct.byref(calls), ct.byref(ops))
    if operations:
        return res, calls.value, ops.value
    else:
        return res


if __name__ == '__main__':
    def f(x):
        return 1.0 / x

    #k_values = [-6, -4, -2, 0, 2, 4, 6]
    k_values = [i for i in range(1, 7)]
    #k_values = [1, 2]
    m_values = list(range(1, 8))

    for k, m in product(k_values, m_values):
        approx_log = integrate_romberg(f, 1, 10 ** k, m)
        print "k = {: }, m = {}, ln ist {}. Fehler ist {}".format(
                            k, m, approx_log, k * log(10) - approx_log)

    fig = mpl.figure()
    ax = fig.add_subplot(111)

    for k in k_values:
        ops = []
        error = []
        for m in m_values:
            res, calls, operations = integrate_romberg(f, 1, 10 ** k, m, True)
            ops.append(calls + operations)
            error.append(abs(res - k * log(10)))
        ax.plot(ops, error, label='$k = {}$'.format(k))
        ax.plot(ops, error, '+')

        def fit_func(x, alpha, c):
            return alpha * x + np.log(c)

        popt, pcov = curve_fit(fit_func, np.log(ops), np.log(error))
        alpha, c = popt
        x = np.logspace(log10(min(ops)), log10(max(ops)), 10)
        y = c * x ** alpha
        ax.plot(x, y, '--', color='black')
        ax.text(x[-1] + 50, y[-1], r"$\alpha = {:.3g}$".format(alpha),
                bbox=dict(facecolor='lightgrey', alpha=1))
        print popt


    ax.legend(loc='lower left')
    ax.grid()
    ax.set_xscale('log')
    ax.set_yscale('log')
    mpl.show()
