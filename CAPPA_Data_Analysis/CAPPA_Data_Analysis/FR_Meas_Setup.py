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

# Make plots of the dat obtained during the setup of the software defined VNA
# Want to analyse the data obtained from the basic experiments described in Notebook 426, pg 48-51, 53
# R. Sheehan 23 - 8 - 2018

MOD_NAME_STR = "FR_Meas-Setup" # use this in exception handling messages

def Meas_Setup_Plots():

    # run the methods needed to generate the plots
    # R. Sheehan 23 - 8 - 2018

    FUNC_NAME = ".Meas_Setup_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "C:/Users/Robert/Research/CAPPA/Data/FR_Meas_Eq_Circ/"

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())   
            


        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot find",DATA_HOME)
    except Exception:
        print(ERR_STATEMENT)
