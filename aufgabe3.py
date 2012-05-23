import ctypes
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from quickvis import Interact
import guidata.dataset.dataitems as di
from math import floor, log

_ndpointer_complex = np.ctypeslib.ndpointer(dtype=np.complex,
                                            ndim=1,
                                            flags='C_CONTIGUOUS')

_libfft = np.ctypeslib.load_library('libfft', 'build')
_libfft.fft.argtypes = [_ndpointer_complex,
                        ctypes.c_int]

def fft(array):
    n = len(array)
    if n == 0:
        raise ValueError("length of array is 0")
    while n > 1:
        if n % 2 != 0:
            raise ValueError("length of array is not a power of 2")
        n /= 2
    points = np.array(array, dtype=np.complex, copy=True)
    _libfft.fft(points, len(points))
    return points

def ifft(array):
    return fft(array.conj()).conj()

saw = lambda x: x.copy()
rect = lambda x: np.where(x > 0, np.pi, - np.pi)
def triag(x):
    y = np.zeros_like(x)
    y = np.where((x <= np.pi / 2) & (x >= - np.pi / 2), - 2 * x, y)
    y = np.where(x > np.pi / 2, + 2 * x - 2 * np.pi, y)
    y = np.where(x < - np.pi / 2, + 2 * x + 2 * np.pi, y)
    return y


@Interact
def show_fft(fig,
             func=di.ChoiceItem("Funktion",
                        [(saw, "saw"), (rect, "rect"), (triag, "triag")]),
             n=di.IntItem("N", default=32)):
    
    fig.clear()
    
    #x = np.linspace(- np.pi, np.pi, n)
    x = 2 * np.pi * np.arange(n) / n - np.pi
    y = func(x)
    
    gs = gridspec.GridSpec(3, 2)
    
    ax = fig.add_subplot(gs[0, 0:2])
    ax.plot(x, y.real, label=r'$\Re(f)$')
    ax.legend(loc='upper left')
    
    ax = fig.add_subplot(gs[1, 0])
    ax.plot(x, fft(y).real, label=r'$\Re(F(f))$')
    ax.legend()
    
    ax = fig.add_subplot(gs[1, 1], sharex=ax)
    ax.plot(x, fft(y).imag, label=r'$\Im(F(f))$')
    ax.legend()
    
    ax = fig.add_subplot(gs[2, 0])
    ax.plot(x, ifft(fft(y)).real, label=r'$\Re\tilde FF(f)$')
    ax.legend(loc='upper left')
    
    ax = fig.add_subplot(gs[2, 1], sharex=ax)
    ax.plot(x, ifft(fft(y)).imag, label=r'$\Im\tilde FF(f)$')
    ax.legend(loc='upper left')
    
    fig.tight_layout()

if __name__ == '__main__':
    show_fft.show_gui()
