import os
import glob
import re
import sys # access system routines, including writing console output to file

import math
import scipy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import Common
import Plotting

MOD_NAME_STR = "Am_Si" # use this in exception handling messages

# Do the analysis of the amorphous silicon data here
# R. Sheehan 17 - 9 - 2019

def a_Si_plots():

    # Run all plot modules from this method
    # R. Sheehan 18 - 9 - 2019

    FUNC_NAME = ".a_Si_plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "c:/users/Robert/Research/CAPPA/Data/170220_Simone_aSi/"
        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            #LI_plots()

            #Laser_Spectra()

            #Trans_Spectra()

            Mode_Hopping()

        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot locate directory:",DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def LI_plots():
    # Get all LI data and plot it together
    # Make an average and plot it with error bars
    # R. Sheehan 18 - 9 - 2019

    FUNC_NAME = ".LI_plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "LI_Data/"
        if os.path.isdir(DATA_HOME):
            cwd = os.getcwd() # store location of home directory

            os.chdir(DATA_HOME) # move to directory containing data
            print(os.getcwd())

            # import data and make your plot
            laser_list = [1,2,3,5]

            file_template = "Laser_%(v1)d.csv"

            for i in range(0, len(laser_list), 1):
                filename = file_template%{"v1":laser_list[i]}
                if glob.glob(filename):
                    data = np.loadtxt(filename, delimiter=',', skiprows = 1, unpack = True)
                    
                    args = Plotting.plot_arg_single()
                    args.loud = True
                    #args.plt_title = filename
                    args.fig_name = filename.replace('.csv','')
                    args.x_label = 'Current (mA)'
                    args.y_label = 'Power (mW)'
                    args.plt_range = [20, 115, 0, 4.5]
                    args.marker = 'r*'
                    Plotting.plot_single_curve(data[0], data[1], args)

                    del data            

            os.chdir(cwd) # return to home directory
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot locate directory:",DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Laser_Spectra():
    # plot the laser spectra from the existing data
    # trying to find the plot the largest SMSR value try and save the SMSR readings also
    # R. Sheehan 18 - 9 - 2019

    FUNC_NAME = ".Laser_Spectra()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "LASER/"
        if os.path.isdir(DATA_HOME):
            cwd = os.getcwd() # store location of home directory

            os.chdir(DATA_HOME) # move to directory containing data
            print(os.getcwd())
            
            num_list = [8,9]
            curr_list = np.arange(65,81,1)

            file_template = "%(v1)dset5_%(v2)dmA_1500_1600.dat"

            thepath = "Peak_Analysis.txt"

            thefile = open(thepath, "w")

            thefile.write("Num., Current (mA), Wavelength (nm), Power (dBm)\n")

            for i in range(0, len(num_list), 1):
                for j in range(0, len(curr_list), 1):
                    filename = file_template%{"v1":num_list[i], "v2":curr_list[j]}
                    if glob.glob(filename):
                        # import the data 
                        data = np.loadtxt(filename, unpack=True)

                        # find the max value and its associated wavelength value
                        power = np.max(data[1])
                        wavel = data[0][np.argmax(data[1])]
                        
                        print(num_list[i],",",curr_list[j],",",wavel,",",power)

                        data_info = "%(v1)d, %(v2)d, %(v3)0.2f, %(v4)0.2f\n"%{"v1":num_list[i], "v2":curr_list[j], "v3":wavel, "v4":power}

                        thefile.write(data_info)

                        # make a plot of the imported data
                        args = Plotting.plot_arg_single()
                        args.loud = True
                        #args.plt_title = filename
                        args.fig_name = filename.replace('.dat','')
                        args.x_label = 'Wavelength (nm)'
                        args.y_label = 'Power (dBm)'
                        args.plt_range = [1500, 1600, -55, -5]
                        args.marker = 'r-'
                        Plotting.plot_single_curve(data[0], data[1], args)

                        del data

            thefile.close()

            os.chdir(cwd) # return to home directory
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot locate directory:",DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Mode_Hopping():
    # Examine the laser spectrum data for mode-hopping
    # how does lasing wavelength change as a function of RSOA current
    # presumably temperature of device was kept fixed during operation
    # R. Sheehan 18 - 9 - 2019

    FUNC_NAME = ".Mode_Hopping()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "LASER/"
        if os.path.isdir(DATA_HOME):
            cwd = os.getcwd() # store location of home directory

            os.chdir(DATA_HOME) # move to directory containing data
            print(os.getcwd())

            from scipy.signal import find_peaks, peak_prominences, peak_widths
            
            num_list = [8,9]
            curr_list = np.arange(65,81,1)

            file_template = "%(v1)dset5_%(v2)dmA_1500_1600.dat"

            for i in range(0, len(num_list), 1):
                thepath = "Mode_Hop_Analysis_%(v1)d.txt"%{"v1":num_list[i]}
                thefile = open(thepath, "w")
                thefile.write("Current (mA), Wavelength (nm), Power (dBm), Prominence (dB)\n")
                peak_wl = []; peak_curr = []
                for j in range(0, len(curr_list), 1):
                    filename = file_template%{"v1":num_list[i], "v2":curr_list[j]}
                    if glob.glob(filename):
                        # import the data 
                        data = np.loadtxt(filename, unpack=True)

                        # peak search analysis
                        peaks, heights = find_peaks(data[1], height = -40)
                        prominences = peak_prominences(data[1], peaks)[0] # compute peak prominences

                        print(filename)
                        print("no. peaks found:",len(peaks))
                        for k in range(0, len(peaks), 1):
                            if prominences[k] > 5 and data[0][ peaks[k] ] > 1510.0 and data[0][ peaks[k] ] < 1590.0:
                                #print("Peak:",data[0][ peaks[k] ], heights['peak_heights'][k], prominences[k])
                                data_info = "%(v1)d, %(v2)0.2f, %(v3)0.2f, %(v4)0.2f\n"%{"v1":curr_list[j], "v2":data[0][ peaks[k] ], "v3":heights['peak_heights'][k],"v4":prominences[k]}
                                thefile.write(data_info)
                                peak_curr.append(curr_list[j])
                                peak_wl.append(data[0][ peaks[k] ])
                        del data

                thefile.close()

                if len(peak_wl) > 0 and len(peak_curr) > 0:
                    # make a plot of the imported data
                    args = Plotting.plot_arg_single()
                    args.loud = True
                    args.fig_name = thepath.replace('.txt','')
                    args.x_label = 'RSOA Current (mA)'
                    args.y_label = 'Lasing Wavelength (nm)'
                    #args.plt_range = [1525, 1570, 0, 1]
                    args.marker = 'g^'
                    Plotting.plot_single_curve(peak_curr, peak_wl, args)

                del peak_wl; del peak_curr; 

            os.chdir(cwd) # return to home directory
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot locate directory:",DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Trans_Spectra():
    # plot the normalised transmission spectrum for the PhC cavity
    # R. Sheehan 18 - 9 - 2019

    FUNC_NAME = ".Trans_Spectra()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "good_sets/"
        if os.path.isdir(DATA_HOME):
            cwd = os.getcwd() # store location of home directory

            os.chdir(DATA_HOME) # move to directory containing data
            print(os.getcwd())

            n1 = 3; n2 = 6;

            file_template = "%(v1)d_set%(v2)dnormalized.dat"

            filename = file_template%{"v1":n1, "v2":n2}

            if glob.glob(filename):
                data = np.loadtxt(filename, unpack = True)

                # make a plot of the imported data
                args = Plotting.plot_arg_single()
                args.loud = True
                #args.plt_title = filename
                args.fig_name = filename.replace('.dat','')
                args.x_label = 'Wavelength (nm)'
                #args.y_label = 'Transmitted Power (dBm)'
                #args.plt_range = [1525, 1570, -55, -40]
                args.y_label = 'Normalised Transmission'
                args.plt_range = [1525, 1570, 0, 1]
                args.marker = 'r-'
                Plotting.plot_single_curve(data[0], data[1], args)

            filename = "Q_factors.csv"

            if glob.glob(filename):
                data = np.loadtxt(filename, delimiter=',', skiprows=1, unpack = True)

                # make a plot of the imported data
                args = Plotting.plot_arg_single()
                args.loud = True
                #args.plt_title = filename
                args.fig_name = filename.replace('.csv','')
                args.x_label = 'Resonant Wavelength (nm)'
                args.y_label = 'Q-factor'
                args.plt_range = [1525, 1580, 1000, 6500]
                args.marker = 'r*'
                Plotting.plot_single_curve(data[0], data[1], args)

            os.chdir(cwd) # return to home directory
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot locate directory:",DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)