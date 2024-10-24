#!/usr/bin/env python 
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import Bounds
import matplotlib.pyplot as plt
from tkinter import Canvas
from matplotlib import rc
import os
#import time
import my_functions as mf
rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern Sans serif']})
## for Palatino and other serif fonts use:
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
rc('text', usetex=True)

#######################
### DATOS INICIALES ###
#######################


path_oofem = "/home/vant/oofem/build/release/oofem"
path_oofem_extractor = "python3 /home/vant/oofem/oofem.git/tools/extractor.py"
file_exp_path = "./Experimental_data/exp_data" # Ruta del archivo con la curva Load-LVDT experimental
models_folder_path = "./Models" # Ruta de la carpeta con el modelo base y donde se guardarán los modelos para el ajuste
# Abscisas de los puntos de ajuste
main_points = [0.08, 0.5, 4.0, 12.0]
more_points = np.linspace(0,15,100)
x_target = main_points + list(more_points) 

weights_main_points=1.0
weights_more_points=0.25
weights=[weights_main_points]*len(main_points)+[weights_more_points]*len(more_points)

# Se extraen las ordenadas de los puntos de ajuste y se almacenan en y_target
x_exp,y_exp = mf.extractTwoColumns(file_exp_path, 0, 1)
y_target=[]
for i in range(len(x_target)):
    y_target.append(mf.interpolate_value(x_target[i], x_exp, y_exp))

# Valores iniciales de los parámetros de ajuste: E, e0, w_k, w_r, w_f, f_k, f_r
x0=[1.41787e-4, 0.09, 1.65, 6.0, 0.568, 1.180]
#bounds = Bounds([10000.0, 100000.0], [0.0, 0.01], [0.02, 0.50], [0.51, 3.0], [3.1, 10.0], [0.0, 3.0], [0.0, 3.0])
args=[models_folder_path, x_target, y_target]

bnds = Bounds(lb = np.array((1.0e-4, 1.1e-2, 1.0, 4.50, 0.1, 0.1)), ub = np.array((1.0e-2, 0.5, 3.0, 8.0, 1.5, 2.0)), keep_feasible=True)

res = minimize(mf.compute_desv_factor, x0, method='nelder-mead', args=(models_folder_path, x_target, y_target, weights, path_oofem, path_oofem_extractor), options={'maxiter':200, 'maxfev':200}, bounds=bnds)
