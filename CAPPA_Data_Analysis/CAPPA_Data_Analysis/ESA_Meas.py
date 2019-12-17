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

MOD_NAME_STR = "ESA_Meas" # use this in exception handling messages

def Optical_Spectra():

    # plot the measured optical spectra that were recorded
    # R. Sheehan 17 - 12 - 2019

    FUNC_NAME = ".Optical_Spectra()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/ESA_Test/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            print(os.getcwd())

            # plot the DFB spectra with the individual TLS spectra

            dfb_file = np.loadtxt('OSA_DFB_Only.txt')
            tls_1 = np.loadtxt('OSA_TLS_Only_1550_10.txt')
            tls_2 = np.loadtxt('OSA_TLS_Only_1550_19.txt')
            tls_3 = np.loadtxt('OSA_TLS_Only_1550_27.txt')

            # OSA was uncalibrated so horizontal scale must be adjusted appropriately
            l1 = 1550.1
            shift1 = l1 - tls_1[0][np.argmax(tls_1[1])]
            tls_1[0] = tls_1[0]+shift1

            dfb_file[0] = dfb_file[0] + shift1

            print("\nDFB Peak Location ",dfb_file[0][np.argmax(dfb_file[1])],"\n")

            l2 = 1550.19
            shift2 = l2 - tls_2[0][np.argmax(tls_2[1])]
            tls_2[0] = tls_2[0]+shift2

            l3 = 1550.27
            shift3 = l3 - tls_3[0][np.argmax(tls_3[1])]
            tls_3[0] = tls_3[0]+shift3

            #print("offsets")
            #print("tls 1 was set ",l1)
            #print("actual peak ",tls_1[0][np.argmax(tls_1[1])])
            #print("required shift",l1-tls_1[0][np.argmax(tls_1[1])])
            #print("tls 2 was set ",l2)
            #print("actual peak ",tls_2[0][np.argmax(tls_2[1])])
            #print("required shift",l2-tls_2[0][np.argmax(tls_2[1])])
            #print("tls 1 was set ",l3)
            #print("actual peak ",tls_3[0][np.argmax(tls_3[1])])
            #print("required shift",l3-tls_3[0][np.argmax(tls_3[1])])

            hv_data = []; labels = []; marks = []; 

            hv_data.append(dfb_file); labels.append('DFB'); marks.append(Plotting.labs_dashed[0]); 
            hv_data.append(tls_3); labels.append('$\lambda_{TLS}$ = 1550.27 nm'); marks.append(Plotting.labs_lins[1]); 
            hv_data.append(tls_2); labels.append('$\lambda_{TLS}$ = 1550.19 nm'); marks.append(Plotting.labs_lins[2]); 
            hv_data.append(tls_1); labels.append('$\lambda_{TLS}$ = 1550.10 nm'); marks.append(Plotting.labs_lins[3]); 

            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.plt_range = [1549.5, 1550.5, -70, 0]
            args.x_label = 'Wavelength (nm)'
            args.y_label = 'Power (dBm / 0.01 nm)'
            args.fig_name = 'Individual_Optical_Spectra'

            Plotting.plot_multiple_curves(hv_data, args)

            # plot the combined measured spectra with the DFB spectra
            tls_1 = np.loadtxt('OSA_LTLS_1550_10.txt')
            tls_2 = np.loadtxt('OSA_LTLS_1550_19.txt')
            tls_3 = np.loadtxt('OSA_LTLS_1550_27.txt')

            # OSA was uncalibrated so horizontal scale must be adjusted appropriately
            tls_1[0] = tls_1[0]+shift1
            tls_2[0] = tls_2[0]+shift2
            tls_3[0] = tls_3[0]+shift3

            hv_data = []; labels = []; marks = [];

            hv_data.append(dfb_file); labels.append('DFB'); marks.append(Plotting.labs_dashed[0]);
            hv_data.append(tls_3); labels.append('$\lambda$ = 1550.27 nm'); marks.append(Plotting.labs_lins[1]); 
            hv_data.append(tls_2); labels.append('$\lambda$ = 1550.19 nm'); marks.append(Plotting.labs_lins[2]); 
            hv_data.append(tls_1); labels.append('$\lambda$ = 1550.10 nm'); marks.append(Plotting.labs_lins[3]);

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.plt_range = [1549.5, 1550.5, -70, 0]
            args.x_label = 'Wavelength (nm)'
            args.y_label = 'Power (dBm / 0.01 nm)'
            args.fig_name = 'Coupled_Optical_Spectra'

            Plotting.plot_multiple_curves(hv_data, args)

        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Frequency_Analysis():

    FUNC_NAME = ".Frequency_Analysis()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/ESA_Test/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            print(os.getcwd())

            deltal = [0.025, 0.034, 0.047, 0.055, 0.065, 0.076, 0.087, 0.097, 0.106, 0.117, 0.125, 0.136, 0.146, 0.155, 0.165, 0.176]

            ltls = np.linspace(1550.27, 1550.10, 18)

            fvals = np.zeros(len(ltls));
            pvals = np.zeros(len(ltls));
            ferrvals = np.zeros(len(ltls));
            perrvals = np.zeros(len(ltls));

            count = 0; 
            for x in ltls:
                xstr = "%(v1)0.2f"%{"v1":x}
                
                filename = 'F_Swp_LTLS_1550_%(v1)s.txt'%{"v1":xstr.replace('1550.','')}

                if glob.glob(filename):

                    data = np.loadtxt(filename, delimiter=',', unpack = True)

                    fmean = np.mean(data[1]); ferr = 0.5*np.std(data[1], ddof = 1); 

                    pmean = np.mean(data[2]); perr = 0.5*np.std(data[2], ddof = 2); 

                    fvals[count] = fmean; pvals[count] = pmean; perrvals[count] = perr; ferrvals[count] = ferr; 

                    print("%(v3)s, %(v1)0.2f +/-  %(v4)0.2f, %(v2)0.2f +/-  %(v5)0.2f"%{"v3":filename, "v1":fmean, "v2":pmean, "v4":ferr, "v5":perr})

                    count = count + 1


            # Make a plot of the data

            args = Plotting.plot_arg_single(); 

            args.loud = True
            #args.marker = Plotting.labs_pts[0]
            #args.curve_label = '$\Delta\nu = -125.17 $\lambda_{TLS}$ + 194050'
            args.x_label = "TLS Wavelength (nm)"
            args.y_label = "Beat Frequency (GHz)"
            args.fig_name = 'Beat_Frequency'

            Plotting.plot_single_linear_fit_curve(ltls, fvals, args)

            args.loud = True
            #args.marker = Plotting.labs_pts[0]
            #args.curve_label = '$\Delta\nu = -125.17 $\lambda_{TLS}$ + 194050'
            args.x_label = "Wavelength Separation (nm)"
            args.y_label = "Beat Frequency (GHz)"
            args.fig_name = 'Beat_Frequency_Separation'

            Plotting.plot_single_linear_fit_curve(deltal, fvals[1:-1], args)

            args.loud = True
            args.marker = Plotting.labs_pts[0]
            args.x_label = "Beat Frequency (GHz)"
            args.y_label = "Signal Power (dBm)"
            args.fig_name = 'Frequency_Response'

            Plotting.plot_single_curve_with_errors(fvals, pvals, perrvals, args)
        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
