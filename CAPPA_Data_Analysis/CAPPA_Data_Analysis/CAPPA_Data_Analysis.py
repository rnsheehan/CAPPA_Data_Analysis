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

def main():
    pass

if __name__ == '__main__':
    main()

    pwd = os.getcwd() # get current working directory

    print(pwd)

    #Yenista_TLS.Yen_Char_Plots()

    #DBR_Analysis.DBR_Sim_Plots()

    FR_Meas_Setup.Meas_Setup_Plots()
