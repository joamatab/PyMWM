#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from scipy.constants import c
import pymwm
fmin = 2.0
fmax = 6.0
lmin = c * 1e-8 / fmax
lmax = c * 1e-8 / fmin
params = {'core': {'shape': 'cylinder', 'size': 0.15,
                   'fill': {'model': 'air'}},
          'clad': {'model': 'gold_dl'},
          'bounds': {'lmax': lmax, 'lmin': lmin, 'limag': 10.0},
          'modes': {'num_n': 6, 'num_m': 2}}
wg = pymwm.create(params)
wg.plot_betas(fmin, fmax, comp='real')
wg.plot_betas(fmin, fmax, comp='imag')
w = 2 * np.pi / lmax
print("lambda =", lmax)
for alpha in wg.alpha_list:
    print(alpha, np.abs(wg.coef(wg.beta(w, alpha), w, alpha)))
w = 2 * np.pi / lmin
print("lambda =", lmin)
for alpha in wg.alpha_list:
    print(alpha, np.abs(wg.coef(wg.beta(w, alpha), w, alpha)))
