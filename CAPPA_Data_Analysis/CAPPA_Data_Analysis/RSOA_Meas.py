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

MOD_NAME_STR = "RSOA_Meas" # use this in exception handling messages

def plot_IV_Curve():
    # make a plot of the RSOA IV curve

    FUNC_NAME = ".plot_IV_Curve()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/RSOA_HS_Meas/'
        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            filename = 'RSOA_Vpp_R_T_20.csv'

            if glob.glob(filename):
                pass
            else:
                raise Exception
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print('Cannot find',DATA_HOME)
    except Exception:
        print(ERR_STATEMENT)


def plot_Vpp_R_Curve():
    # make a plot of the measured response data

    FUNC_NAME = ".plot_Vpp_R_Curve()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/RSOA_HS_Meas/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            filename = 'RSOA_Vpp_R_T_20.csv'

            if glob.glob(filename):
                print('File:',filename,'exists')
                data = Common.read_matrix(filename)
                data = Common.transpose_multi_col(data)

                args = Plotting.plot_arg_single()

                args.loud = True
                args.x_label = 'Frequency (MHz)'
                

                # plot the Vpp data
                args.y_label = 'Peak-Peak Voltage (V)'
                #Plotting.plot_single_curve(data[0], data[1], args)

                # plot the FR data
                args.y_label = 'Response (dB)'
                args.marker = 'r-'
                args.fig_name = 'RSOA_FR'
                Plotting.plot_single_curve(data[0], data[2], args)

            else:
                raise Exception
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print('Cannot find',DATA_HOME)
    except Exception:
        print(ERR_STATEMENT)
