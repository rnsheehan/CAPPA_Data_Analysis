# Import libraries
# You should try an import the bare minimum of modules
import sys # access system routines
import os
import glob
import re

import math
import scipy
import numpy
import matplotlib.pyplot as plt

# add path to our file
sys.path.append('c:/Users/Robert/Programming/Python/Common/')
sys.path.append('c:/Users/Robert/Programming/Python/Plotting/')

import Yenista_TLS
import DBR_Analysis
import FR_Meas_Setup
import Redfinch_AWG
import DANCER
import RSOA_Meas
import TIDA_Data

def main():
    pass

if __name__ == '__main__':
    main()

    pwd = os.getcwd() # get current working directory

    print(pwd)

    #Yenista_TLS.Yen_Char_Plots()

    #DBR_Analysis.DBR_Sim_Plots()

    #FR_Meas_Setup.Meas_Setup_Plots()

    #Redfinch_AWG.Make_AWG_Plots()

    #DANCER.DANCER_Plots()

    #RSOA_Meas.plot_Vpp_R_Curve()

    #TIDA_Data.Plot_SiN_RI()

    #TIDA_Data.Plot_coupling_coeff(True)

    TIDA_Data.Filter_Data()
