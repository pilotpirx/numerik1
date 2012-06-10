import ctypes as ct
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as mpl
from itertools import product
from math import log, log10
from quickvis import interact
import traits.api as traits

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


@interact
def main(fig,
         k_values_plot=traits.Expression('[2, 4, 6]'),
         m_max=traits.Int(8),
         log_x=traits.Bool(True),
         show_fit=traits.Bool(True)):

    def f(x):
        return 1.0 / x

    k_values_plot = eval(k_values_plot)
    k_values = [-6, -4, -2, 0, 2, 4, 6]
    m_values = list(range(1, m_max))

    for k, m in product(k_values, m_values):
        approx_log = integrate_romberg(f, 1, 10 ** k, m)
        print "k = {: }, m = {}, ln ist {}. Fehler ist {}".format(
                            k, m, approx_log, k * log(10) - approx_log)

    ax = fig.add_subplot(111)
    if log_x:
        ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('number of operations')
    ax.set_ylabel('error')
    ax.grid()

    for k in k_values_plot:
        ops = []
        error = []
        for m in m_values:
            res, calls, operations = integrate_romberg(f, 1, 10 ** k, m, True)
            ops.append(calls + operations)
            error.append(abs(res - k * log(10)))
        ax.plot(ops, error, label='$k = {}$'.format(k))

        if show_fit:
            def fit_func(x, alpha, c):
                return alpha * x + np.log(c)
    
            popt, pcov = curve_fit(fit_func, np.log(ops), np.log(error))
            alpha, c = popt
            x = np.logspace(log10(min(ops)), log10(max(ops)), 20)
            y = c * x ** alpha
            ax.plot(x, y, '--', color='black')
    
            loc = np.array([x[11], y[11]])
            angle = np.arctan((y[12] - y[11]) / (x[12] - x[11]))
    
            trans_angle = ax.transData.transform_angles(np.array((angle,)),
                                         loc.reshape((1,2)), radians=True)[0]
            trans_angle *= 180 / np.pi
            ax.text(loc[0], loc[1], r"$\alpha = {:.3g}$".format(alpha),
                    rotation=trans_angle,
                    ha='right', va='center')


    ax.legend(loc='lower left')


if __name__ == '__main__':
    main.show_gui()