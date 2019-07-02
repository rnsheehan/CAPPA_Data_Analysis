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

MOD_NAME_STR = "COSMICC_Data" # use this in exception handling messages

def Nanostick_Spectrum(num, loud = False):

    # plot the measured transmission spectra for Simone's Nanostick devices
    # R. Sheehan 2 - 7 - 2019

    FUNC_NAME = ".Nanostick_Spectrum()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/COSMICC/Nanosticks/June_2019/Passive_Results/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            filename = 'd1_3%(v1)d_.dat'%{"v1":num}

            if glob.glob(filename):
                print(filename,"exists")

                data = np.loadtxt(filename, unpack = True)

                if data is not None:
                    # plot the data in the file
                    arguments = Plotting.plot_arg_single()
                    arguments.y_label = 'Power (dBm)'
                    arguments.x_label = 'Wavelength (nm)'
                    arguments.marker = 'r-'
                    #arguments.plt_range = [1520, 1540, -76, -46]
                    arguments.loud = True
                    #arguments.fig_name = filename.replace('.dat','')

                    Plotting.plot_single_curve(data[0], -1.0*data[1]-45, arguments)

                    del data
                else:
                    raise Exception
            else:
                raise Exception
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT);
        print(e);

def Nanostick_Spectra(loud = False):

    # plot the measured transmission spectra for Simone's Nanostick devices
    # R. Sheehan 2 - 7 - 2019

    FUNC_NAME = ".Nanostick_Spectra()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/COSMICC/Nanosticks/June_2019/Passive_Results/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            numlst = [0, 1, 2]
            hv_data = []; mrk_lst = []; lab_lst = []
            for i in range(0, len(numlst), 1):
                filename = 'd1_3%(v1)d_.dat'%{"v1":numlst[i]}

                if glob.glob(filename):
                    print(filename,"exists")
                    data = np.loadtxt(filename, unpack = True)
                    hv_data.append(data); mrk_lst.append(Plotting.labs_lins[i%len(Plotting.labs_lins)]); lab_lst.append(filename.replace('.dat',''))

            if hv_data is not None:
                # plot the data in the file
                arguments = Plotting.plot_arg_multiple()

                arguments.y_label = 'Power (dBm)'
                arguments.x_label = 'Wavelength (nm)'
                arguments.mrk_list = mrk_lst
                arguments.crv_lab_list = lab_lst
                arguments.plt_range = [1520, 1540, -76, -46]
                arguments.loud = True
                arguments.fig_name = 'Combined_Nanostick_Spectra'

                Plotting.plot_multiple_curves(hv_data, arguments)

                del data
                
            else:
                raise Exception
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT);
        print(e);

def Nanostick_Peak_Analysis(num, loud = False):

    # Locate the spectral peaks and their FWHM
    # Compute the mode Q-factor from this data Q = \Delta lambda / \lambda
    # R. Sheehan 2 - 7 - 2019

    FUNC_NAME = ".Nanostick_Spectrum()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/COSMICC/Nanosticks/June_2019/Passive_Results/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            filename = 'd1_3%(v1)d_.dat'%{"v1":num}

            if glob.glob(filename):
                print(filename,"exists")

                data = np.loadtxt(filename, unpack = True)

                if data is not None:
                    from scipy.signal import find_peaks, peak_prominences, peak_widths

                    peaks, heights = find_peaks(-1.0*data[1]-45, height = 5)
                    prominences = peak_prominences(-1.0*data[1]-45, peaks)[0] # compute peak prominences
                    widths = peak_widths(-1.0*data[1]-45, peaks, rel_height=0.5)[0] # compute peak FWHM

                    #print(widths)

                    for i in range(0, len(peaks), 1):
                        if prominences[i] > 2:
                            Q = data[0][ peaks[i] ]/widths[i]
                            print("Peak:",data[0][ peaks[i] ], heights['peak_heights'][i], prominences[i], widths[i], Q)

                    del data
                else:
                    raise Exception
            else:
                raise Exception
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT);
        print(e);

def peak_search_example():
    # implementation of the peak search example in 
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.peak_widths.html



    pass
