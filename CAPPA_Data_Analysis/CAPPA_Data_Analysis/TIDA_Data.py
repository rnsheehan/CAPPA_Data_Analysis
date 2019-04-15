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

MOD_NAME_STR = "TIDA_Data" # use this in exception handling messages

def SiN_Data():
    # Format the digitised SiN RI and Abs data from the paper
    # ``Expanding the Silicon Photonics Portfolio With SiN PICs''
    # R. Sheehan 12 - 4 - 2019

    FUNC_NAME = ".SiN_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/Papers/SIN/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            print(os.getcwd())

            ri_file = 'SiN_RI_Data.csv'; abs_file = 'SiN_Abs_Data.csv'; 

            if glob.glob(ri_file) and glob.glob(abs_file):
                
                # read the raw data into memory
                ri_data = np.loadtxt(ri_file, delimiter = ',', skiprows = 1, unpack = True)

                abs_data = np.loadtxt(abs_file, delimiter = ',', skiprows = 1, unpack = True)

                # format the data for use in the dispersion calculation code
                # data should be output in the form
                # wavelength (nm) \t n \t k
                from scipy import interpolate

                # interp1d will throw an error if you attempt to compute a value outside the interpolation range
                f = interpolate.interp1d(abs_data[0], abs_data[1]) # interpolation object for the absorption data

                # write the data to the file
                fmtd_name = 'SiN_LPCVD.txt'
                fmtd_file = open(fmtd_name, "w"); 

                if fmtd_file.closed:
                    raise IOError
                else:
                    fmtd_file.write('Wavelength (nm)\tn\tk\n')

                    for i in range(0, len(ri_data[0]), 1):
                        wl = ri_data[0][i]
                        fmtd_file.write("%(v1)0.2f\t %(v2)0.5f\t %(v3)0.5f\n"%{"v1":1000*wl, "v2":ri_data[1][i], "v3":f( wl )})

                    fmtd_file.close()

                del abs_data; del ri_data; 
            else:
                raise Exception
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print('Cannot find',DATA_HOME)
    except Exception:
        print(ERR_STATEMENT)

def Plot_SiN_RI():
    # make a comparison of the SiN data that you have
    # R. Sheehan 12 - 4 - 2019

    FUNC_NAME = ".Plot_SiN_RI()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/Papers/SIN/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            print(os.getcwd())

            old_name = 'Si3N4.txt'
            new_name = 'SiN_LPCVD.txt'

            if glob.glob(old_name) and glob.glob(new_name):
                old_data = np.loadtxt(old_name, delimiter = '\t', skiprows = 1, unpack = True)
                new_data = np.loadtxt(new_name, delimiter = '\t', skiprows = 1, unpack = True)

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.mrk_list = [Plotting.labs_pts[0], Plotting.labs_pts[1]]
                args.crv_lab_list = ['Old Data', 'New Data']

                Plotting.plot_multiple_curves([[old_data[0], old_data[2]], [new_data[0], new_data[2]] ], args)

            else:
                raise Exception
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print('Cannot find',DATA_HOME)
    except Exception:
        print(ERR_STATEMENT)
