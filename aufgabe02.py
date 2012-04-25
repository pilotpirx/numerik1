import ctypes
import numpy as np
import matplotlib.pyplot as plt

_ndpointer_double = np.ctypeslib.ndpointer(dtype=np.double,
                                           ndim=1,
                                           flags='C_CONTIGUOUS')

_libpoly = np.ctypeslib.load_library('libpoly', '.')
_libpoly.poly_de_casteljau_array.argtypes = [_ndpointer_double,
                                             ctypes.c_int,
                                             _ndpointer_double,
                                             _ndpointer_double,
                                             ctypes.c_int]

def poly_de_casteljau(points, t):
    points = np.asarray(points, dtype=np.double)
    t = np.asarray(t, dtype=np.double)
    out_all_dims = []
    for b in points:
        out = np.empty(t.size, np.double)
        _libpoly.poly_de_casteljau_array(b, len(b), t.ravel(), out, t.size)
        out_all_dims.append(out.reshape(t.shape))
    return np.array(out_all_dims)

def main():
    x = np.array([0,1,2,3])
    y = np.array([0,1,0,2])
    t = np.linspace(-0, 1, 40)
    p_x, p_y = poly_de_casteljau([x, y], t)
    plt.plot(p_x, p_y)
    plt.plot(*poly_de_casteljau([x[:-1], y[:-1]], t), alpha=0.5, linewidth=0.5)
    plt.plot(*poly_de_casteljau([x[1:], y[1:]], t), alpha=0.5, linewidth=0.5)
    plt.plot(x, y, '--', alpha=0.5, linewidth=0.5)
    plt.plot(x, y, 'o', color='red')
    plt.show()

if __name__ == '__main__':
    main()
