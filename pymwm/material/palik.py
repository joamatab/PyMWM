# -*- coding: utf-8 -*-
import os
import numpy as np
from scipy.constants import eV, hbar, c
from scipy.interpolate import interp1d


class Palik():

    """A class defining the dielectric function for noble metals according to
    Handbook of Optical Constants of Solids, ed Palik ED (Academic, Orlando)
    (1985).

    Attributes:
        ws: 1D array of floats indicating the angular frequencys.
        ns: 1D array of floats indicating the real part of RIs.
        ks: 1D array of floats indicating the imaginary part of RIs.
    """

    def __init__(self, metal, unit, kind='cubic'):
        self.num = 2048
        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname, "Palik")
        filename = os.path.join(dirname, "{0}.npy".format(metal))
        data = np.load(filename)
        ws0 = data[:, 0] * eV / hbar * unit * 1e-6 / c
        ns0 = data[:, 1]
        ks0 = data[:, 2]
        n_func = interp1d(ws0, ns0, kind=kind, copy=False,
                          assume_sorted=True)
        k_func = interp1d(ws0, ks0, kind=kind, copy=False,
                          assume_sorted=True)
        self.ws = np.linspace(ws0[0], ws0[-1], self.num)
        self.ns = n_func(self.ws)
        self.ks = k_func(self.ws)

    def __call__(self, w):
        ind = np.searchsorted(self.ws, w)
        if ind == 0 or ind == self.num:
            if w == self.ws[0]:
                n = self.ns[0]
                k = self.ks[0]
            else:
                raise ValueError("The frequency is out-of-range")
        else:
            w0, w1 = self.ws[ind - 1: ind + 1]
            n0, n1 = self.ns[ind - 1: ind + 1]
            k0, k1 = self.ks[ind - 1: ind + 1]
            n = n0 + (n1 - n0) / (w1 - w0) * (w - w0)
            k = k0 + (k1 - k0) / (w1 - w0) * (w - w0)
        return complex(n ** 2 - k ** 2, 2 * n * k)