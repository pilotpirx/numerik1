import ctypes
import numpy as np
import matplotlib.pyplot as plt

_ndpointer_double = np.ctypeslib.ndpointer(dtype=np.double,
                                           ndim=1,
                                           flags='C_CONTIGUOUS')

_libpoly = np.ctypeslib.load_library('libpoly', '.')
_libpoly.poly_neville_array.argtypes = [_ndpointer_double,
                                        _ndpointer_double,
                                        ctypes.c_int,
                                        _ndpointer_double,
                                        _ndpointer_double,
                                        ctypes.c_int]

def poly_neville(x, f, t):
    x = np.asarray(x, dtype=np.double)
    f = np.asarray(f, dtype=np.double)
    assert x.size == f.size
    assert np.unique(x).shape == x.shape
    out = np.empty(t.size, dtype=np.double)
    _libpoly.poly_neville_array(x, f, len(x), t.ravel(), out, t.size)
    return out.reshape(t.shape)

def main():
    x = np.random.randn(4)
    f = np.random.randn(4)
    t = np.linspace(x.min() - 0.2, x.max() + 0.2)
    p = poly_neville(x, f, t)
    plt.plot(t, p)
    plt.plot(x, f, 'o')
    plt.show()

if __name__ == '__main__':
    main()
