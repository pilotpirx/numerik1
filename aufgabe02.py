import ctypes
import numpy as np
import matplotlib.pyplot as plt

_ndpointer_double = np.ctypeslib.ndpointer(dtype=np.double,
                                           ndim=1,
                                           flags='C_CONTIGUOUS')

_libpoly = np.ctypeslib.load_library('libpoly', 'build')
_libpoly.poly_de_casteljau_array.argtypes = [_ndpointer_double,
                                             ctypes.c_int,
                                             ctypes.c_int,
                                             _ndpointer_double,
                                             _ndpointer_double,
                                             ctypes.c_int]

def poly_de_casteljau(points, t, n_deriv=0):
    points = np.ascontiguousarray(points, dtype=np.double)
    t = np.ascontiguousarray(t, dtype=np.double)
    out_all_dims = []
    for b in points:
        out = np.empty(t.size, np.double)
        _libpoly.poly_de_casteljau_array(b, len(b), n_deriv, t.ravel(), out, t.size)
        out_all_dims.append(out.reshape(t.shape))
    return np.array(out_all_dims)

def main():
    x = np.array([0,1,2,3])
    y = np.array([0,1,0,2])
    t = np.linspace(0, 1, 40)
    p_x, p_y = poly_de_casteljau([x, y], t)
    fig = plt.figure("Bezier curve")
    ax1 = fig.add_subplot(121)
    ax1.plot(p_x, p_y, label='Bezier curve')
    ax1.plot(*poly_de_casteljau([x[:-1], y[:-1]], t), linestyle=':', linewidth=0.8)
    ax1.plot(*poly_de_casteljau([x[1:], y[1:]], t), linestyle=':', linewidth=0.8)
    ax1.plot(x, y, '--', linewidth=0.8)
    ax1.plot(x, y, 'o', color='red', label='Bezier points')
    ax1.legend(loc='upper left')

    ax2 = fig.add_subplot(122, sharex=ax1, sharey=ax1)
    dp_x, dp_y = poly_de_casteljau([x, y], t, 1)
    ax2.plot(x.ptp() * t + x.min(), dp_y / dp_x, label=r'$\frac{dy}{dx}$')
    ax2.legend(loc='upper left')
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
