import os
import glob
import re
import sys # access system routines, including writing console output to file

import math
import scipy
import numpy as np
import matplotlib.pyplot as plt

import Common
import Plotting

# Make plots of the data obtained while characterising the Yenista TLS TUNICS T100S-HP TLS
# R. Sheehan 14 - 3 - 2018

MOD_NAME_STR = "Yenista_TLS" # use this in exception handling messages

def Yen_Char_Plots():

    # Run the functions to plot the Yenista Data

    FUNC_NAME = ".Yen_Char_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "C:/Users/Robert/Research/CAPPA/Data/Yenista_TLS/"

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            Yen_Pow_Spctrm()
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot find",DATA_HOME)
    except Exception:
        print(ERR_STATEMENT)

def Yen_Pow_Spctrm():

    # Function for plotting the Yenista Power Spectrum

    FUNC_NAME = ".Yen_Char_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        HOME = os.getcwd()

        DATA_HOME = "Power_Data/"

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            #pow_vals = [1, 5, 10, 15, 20, 25]
            pow_vals = [20, 30, 50, 75, 100, 150, 200, 250, 300, 350]

            hv_data = []; labels = []; mrk_list = []; 

            delim = '\t'
            
            for i in range(0, len(pow_vals), 2):
                #file_name = "Pow_Spctrm_P_%(v1)d.txt"%{"v1":pow_vals[i]}
                file_name = "Pow_Spctrm_I_%(v1)d.txt"%{"v1":pow_vals[i]}
                if glob.glob(file_name):
                    data = Common.read_matrix(file_name, delim)
                    data = Common.transpose_multi_col(data)
                    hv_data.append(data)
                    labels.append("%(v1)d mA"%{"v1":pow_vals[i]})
                    mrk_list.append( Plotting.labs_pts[ i % len(Plotting.labs_pts) ] )
                    del data

            if len(hv_data)>0:

                arguments = Plotting.plot_arg_multiple()

                arguments.x_label = 'Wavelength (nm)'
                arguments.y_label = 'Power (mW)'
                arguments.plt_range = [1500, 1625, 0, 16.5]
                arguments.loud = True
                arguments.crv_lab_list = labels
                arguments.mrk_list = mrk_list
                arguments.plt_title = 'Yenista TLS TUNICS T100S-HP TLS'
                arguments.fig_name = 'Yen_TLS_Pow_Spctrm_CC'

                Plotting.plot_multiple_curves(hv_data, arguments)

                del hv_data; del labels; del mrk_list; 

            os.chdir(HOME)
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot find",DATA_HOME)
    except Exception:
        print(ERR_STATEMENT)
