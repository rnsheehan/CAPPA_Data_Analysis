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

            #Laser_Spectra_2()

            #Laser_Spectra_Combo()

            #Trans_Spectra()

            #Mode_Hopping_2()

            #Q_Factor_Plots()

            #More_Q_Factor_Plots()

            Modulation_Depth()

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

def Laser_Spectra_2():
    # plot the laser spectra from the existing data
    # trying to find the plot the largest SMSR value try and save the SMSR readings also
    # R. Sheehan 18 - 9 - 2019

    FUNC_NAME = ".Laser_Spectra()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        lnum = 5
        DATA_HOME = "170922_Laser/%(v1)d"%{"v1":lnum}
        if os.path.isdir(DATA_HOME):
            cwd = os.getcwd() # store location of home directory

            os.chdir(DATA_HOME) # move to directory containing data
            print(os.getcwd())
            
            curr_list = np.arange(20,115,1)

            file_template = "%(v1)d_%(v2)dmA.dat"

            thepath = "Peak_Analysis_%(v1)d.txt"%{"v1":lnum}

            thefile = open(thepath, "w")

            thefile.write("Num., Current (mA), Wavelength (nm), Power (dBm)\n")

            for j in range(0, len(curr_list), 1):
                filename = file_template%{"v1":lnum, "v2":curr_list[j]}
                if glob.glob(filename):
                    # import the data 
                    data = np.loadtxt(filename, unpack=True)

                    # find the max value and its associated wavelength value
                    power = np.max(data[1])
                    wavel = data[0][np.argmax(data[1])]
                        
                    print(curr_list[j],",",wavel,",",power)

                    data_info = "%(v2)d, %(v3)0.2f, %(v4)0.2f\n"%{"v2":curr_list[j], "v3":wavel, "v4":power}

                    thefile.write(data_info)

                    # make a plot of the imported data
                    args = Plotting.plot_arg_single()
                    args.loud = True
                    #args.plt_title = filename
                    #args.fig_name = filename.replace('.dat','')
                    args.x_label = 'Wavelength (nm)'
                    args.y_label = 'Power (dBm)'
                    args.plt_range = [1565, 1580, -75, -25]
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

def Laser_Spectra_Combo():
    # plot the laser spectra from the existing data
    # trying to find the plot the largest SMSR value try and save the SMSR readings also
    # R. Sheehan 18 - 9 - 2019

    FUNC_NAME = ".Laser_Spectra()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "170922_Laser/Combos/"
        if os.path.isdir(DATA_HOME):
            cwd = os.getcwd() # store location of home directory

            os.chdir(DATA_HOME) # move to directory containing data
            print(os.getcwd())

            # plot the single mode lasing spectra together
            file_template = "%(v1)d_%(v2)dmA.dat"

            hv_list = []; markers = []; labels = [];

            lnum = 3; latt_const = 386; curr_list = 26; count = 0; 
            
            filename = file_template%{"v1":lnum, "v2":curr_list}
            if glob.glob(filename):

                # import the data 
                data = np.loadtxt(filename, unpack=True)  
                    
                hv_list.append([data[0], data[1]]); 
                markers.append(Plotting.labs_lins[ count%len(Plotting.labs_lins) ]); 
                labels.append("a = %(v1)d nm"%{"v1":latt_const})

                del data

            lnum = 4; latt_const = 388; curr_list = 26; count = 1; 
            
            filename = file_template%{"v1":lnum, "v2":curr_list}
            if glob.glob(filename):

                # import the data 
                data = np.loadtxt(filename, unpack=True)  
                    
                hv_list.append([data[0], data[1]]); 
                markers.append(Plotting.labs_lins[ count%len(Plotting.labs_lins) ]); 
                labels.append("a = %(v1)d nm"%{"v1":latt_const})

                del data

            lnum = 5; latt_const = 390; curr_list = 28; count = 2;

            filename = file_template%{"v1":lnum, "v2":curr_list}
            if glob.glob(filename):

                # import the data 
                data = np.loadtxt(filename, unpack=True)  
                    
                hv_list.append([data[0], data[1]]); 
                markers.append(Plotting.labs_lins[ count%len(Plotting.labs_lins) ]); 
                labels.append("a = %(v1)d nm"%{"v1":latt_const})

                del data

            # make a plot of the imported data
            args = Plotting.plot_arg_multiple()
            args.loud = True
            #args.plt_title = filename
            args.fig_name = 'Laser_Spectra'
            args.x_label = 'Wavelength (nm)'
            args.y_label = 'Power (dBm)'
            #args.plt_range = [1540, 1575, -70, -25]
            args.plt_range = [1560, 1580, -70, -25]
            args.mrk_list = markers
            args.crv_lab_list = labels
            Plotting.plot_multiple_curves(hv_list, args)

            del hv_list; del markers; del labels; 

            # plot the spectral broadening curves together

            lnum = 2; latt_const = 384; curr_list = [31, 40, 70]; 

            #lnum = 3; latt_const = 386; curr_list = [26, 40, 70]; 

            #lnum = 5; latt_const = 390; curr_list = [28, 40, 70]; 

            file_template = "%(v1)d_%(v2)dmA.dat"

            hv_list = []; markers = []; labels = []; 

            count = 0; 
            for j in range(0, len(curr_list), 1):
                filename = file_template%{"v1":lnum, "v2":curr_list[j]}
                if glob.glob(filename):

                    # import the data 
                    data = np.loadtxt(filename, unpack=True)  
                    
                    hv_list.append([data[0], data[1]]); 
                    markers.append(Plotting.labs_lins[ count%len(Plotting.labs_lins) ]); 
                    labels.append("$I_{RSOA}$ = %(v1)d mA"%{"v1":curr_list[j]})

                    count = count + 1

                    del data

            # make a plot of the imported data
            args = Plotting.plot_arg_multiple()
            args.loud = True
            #args.plt_title = filename
            args.fig_name = 'Broadening_a_%(v1)d'%{"v1":latt_const}
            args.x_label = 'Wavelength (nm)'
            args.y_label = 'Power (dBm)'
            args.plt_range = [1535, 1570, -70, -25]
            #args.plt_range = [1540, 1575, -70, -25]
            #args.plt_range = [1550, 1585, -70, -25]
            args.mrk_list = markers
            args.crv_lab_list = labels
            Plotting.plot_multiple_curves(hv_list, args)

            del hv_list; del markers; del labels; 

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
        #DATA_HOME = "LASER/"
        lnum = 5
        DATA_HOME = "170922_Laser/%(v1)d"%{"v1":lnum}
        if os.path.isdir(DATA_HOME):
            cwd = os.getcwd() # store location of home directory

            os.chdir(DATA_HOME) # move to directory containing data
            print(os.getcwd())

            from scipy.signal import find_peaks, peak_prominences, peak_widths
            
            num_list = [8,9]
            curr_list = np.arange(65,81,1)

            file_template = "%(v1)dset5_%(v2)dmA_1500_1600.dat"
            file_template = "%(v1)d_%(v2)dmA.dat"

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

def Mode_Hopping_2():
    # Examine the laser spectrum data for mode-hopping
    # how does lasing wavelength change as a function of RSOA current
    # presumably temperature of device was kept fixed during operation
    # R. Sheehan 18 - 9 - 2019

    FUNC_NAME = ".Mode_Hopping()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #DATA_HOME = "LASER/"
        lnum = 5
        #DATA_HOME = "170922_Laser/%(v1)d"%{"v1":lnum}
        DATA_HOME = "170922_Laser/Combos/"
        if os.path.isdir(DATA_HOME):
            cwd = os.getcwd() # store location of home directory

            os.chdir(DATA_HOME) # move to directory containing data
            print(os.getcwd())

            from scipy.signal import find_peaks, peak_prominences, peak_widths

            curr_list = np.arange(20,72,1)

            file_template = "%(v1)d_%(v2)dmA.dat"

            thepath = "Mode_Hop_Analysis_%(v1)d.txt"%{"v1":lnum}
            thefile = open(thepath, "w")
            thefile.write("Current (mA), Wavelength (nm), Power (dBm), Prominence (dB)\n")
            peak_wl = []; peak_curr = [];  
            for j in range(0, len(curr_list), 1):
                filename = file_template%{"v1":lnum, "v2":curr_list[j]}
                if glob.glob(filename):
                    # import the data 
                    data = np.loadtxt(filename, unpack=True)

                    res_wl = []; res_pow = [];

                    # peak search analysis
                    peaks, heights = find_peaks(data[1], height = -60)
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
                            res_wl.append(data[0][ peaks[k] ])
                            res_pow.append(heights['peak_heights'][k])
                    del data

                    # Make a plot of the resonant wavelength with its power for each current value
                    if len(res_wl) > 0 and len(res_pow)>0:
                        args = Plotting.plot_arg_single()
                        #args.loud = True
                        thethepath = 'Mode_Hop_Peaks_%(v1)d'%{"v1":curr_list[j]}
                        args.fig_name = thethepath
                        args.x_label = 'Resonant Wavelength (nm)'
                        args.y_label = 'Power (dBm)'
                        args.plt_range = [1540, 1570, -75, -25]
                        args.marker = 'r-'
                        Plotting.plot_single_curve(res_wl, res_pow, args)

                    del res_wl; del res_pow; 

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

def Modulation_Depth():
    # Measure the modulation depth at a certain point in the spectra
    # R. Sheehan 4 - 10 - 2019

    FUNC_NAME = ".Modulation_Depth()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #lnum = 2; wavel = 1551; 
        lnum = 3; wavel = 1555; 
        #lnum = 5; wavel = 1570; 
        DATA_HOME = "170922_Laser/%(v1)d"%{"v1":lnum}

        if os.path.isdir(DATA_HOME):
            cwd = os.getcwd() # store location of home directory

            os.chdir(DATA_HOME) # move to directory containing data
            print(os.getcwd())
            
            curr_list = np.arange(20,115,1)

            file_template = "%(v1)d_%(v2)dmA.dat"

            thepath = "Mod_Depth_Analysis_%(v1)d.txt"%{"v1":lnum}

            thefile = open(thepath, "w")

            thefile.write("Probe Wavelength: %(v1)d\n"%{"v1":wavel})
            thefile.write("Current (mA), Modulation Depth (dB)\n")

            mod_values = np.empty([])
            peak_values = np.empty([])
            curr_values = np.empty([])

            for j in range(0, len(curr_list), 1):
                filename = file_template%{"v1":lnum, "v2":curr_list[j]}
                if glob.glob(filename):
                    # import the data 
                    data = np.loadtxt(filename, unpack=True)

                    result = np.where(data[0]==wavel)[0][0]

                    nn = 100
                    sub_max = np.max(data[1][result-nn:result+nn])
                    sub_min = np.min(data[1][result-nn:result+nn])
                    mod_depth = math.fabs(sub_min) - math.fabs(sub_max)

                    #print(curr_list[j],",",sub_min,",",sub_max,",",mod_depth)

                    mod_values = np.append(mod_values, mod_depth)
                    peak_values = np.append(peak_values, sub_max)
                    curr_values = np.append(curr_values, curr_list[j])

                    thefile.write("%(v1)d,%(v2)0.4f,%(v3)0.4f\n"%{"v1":curr_list[j],"v2":mod_depth,"v3":sub_max})

            mod_values = np.delete(mod_values,0)
            peak_values = np.delete(peak_values,0)
            curr_values = np.delete(curr_values,0)

            thefile.close()
                    
            # quick plot to show the data in the vicinity of 1570
            args = Plotting.plot_arg_single()

            args.loud = True            
            args.fig_name = thepath.replace(".txt","")
            args.x_label = "RSOA Current (mA)"
            args.y_label = "Modulation Depth (dB)"
            args.y_label_2 = "Peak Power (dBm)"
            
            #args.plt_title = 'Modulation Depth'
            #Plotting.plot_single_curve(curr_values, mod_values, args) 
            
            #args.plt_title = 'Broadening Peak'
            #Plotting.plot_single_curve(curr_values, peak_values, args)

            Plotting.plot_two_axis(curr_values, mod_values, peak_values, args)

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

            n1 = 4; n2 = 6;

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
                args.plt_range = [1525, 1590, 0.4, 1.1]
                args.marker = 'r-'
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

def Q_Factor_Plots():
    # plot the computed Q-factor data 
    # R. Sheehan 18 - 9 - 2019

    FUNC_NAME = ".Q_Factor_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "good_sets/"
        if os.path.isdir(DATA_HOME):
            cwd = os.getcwd() # store location of home directory

            os.chdir(DATA_HOME) # move to directory containing data
            print(os.getcwd())

            #filename = "Q_factors.csv"

            #if glob.glob(filename):
            #    data = np.loadtxt(filename, delimiter=',', skiprows=1, unpack = True)

            #    # make a plot of the imported data
            #    args = Plotting.plot_arg_single()
            #    args.loud = True
            #    #args.plt_title = filename
            #    args.fig_name = filename.replace('.csv','')
            #    args.x_label = 'Resonant Wavelength (nm)'
            #    args.y_label = 'Q-factor'
            #    args.plt_range = [1525, 1580, 1000, 6500]
            #    args.marker = 'r*'
            #    Plotting.plot_single_curve(data[0], data[1], args)

            lattice_constants = np.arange(382, 396, 2)

            #lattice_constants = np.arange(384, 392, 2)

            #lattice_constants = [382, 392, 394]

            file_template = "Q_factor_%(v1)d.csv"

            hv_list = []; marks = []; labels = []

            count = 0
            for a in lattice_constants:
                filename = file_template%{"v1":a}
                if glob.glob(filename):
                    data = np.loadtxt(filename, delimiter = ',', unpack = True)

                    hv_list.append(data)
                    labels.append('a = %(v1)d nm'%{"v1":a})
                    marks.append( Plotting.labs_pts[ count%len( Plotting.labs_pts ) ] )

                    del data

                count = count + 1

            # Make the multi plot
            args = Plotting.plot_arg_multiple()

            args.loud = False
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Resonance Wavelength (nm)'
            args.y_label = 'Q-Factor'
            args.plt_range = [1520, 1580, 1000, 7000]
            args.fig_name = 'Q_Factors_LC'
            
            Plotting.plot_multiple_linear_fit_curves(hv_list, args)

            del hv_list; del marks; del labels; del args; 

            # plot the slopes of the Q-factor fits
            filename = 'Q_Factor_Slopes.csv'

            data = np.loadtxt(filename, delimiter = ',', unpack = True)

            args = Plotting.plot_arg_single()

            args.loud = False
            args.marker = 'r*'
            args.x_label = 'PhC Lattice Constant (nm)'
            args.y_label = '$\Delta Q / \Delta \lambda (nm^{-1})$'
            #args.plt_range = [1520, 1580, 1000, 7000]
            args.fig_name = 'Q_Factor_Slopes_1'

            #Plotting.plot_single_curve(data[0][1:-2], data[1][1:-2], args)
            Plotting.plot_single_linear_fit_curve(data[0][1:-2], data[1][1:-2], args)

            del data; del args; 

            # plot the resonant wavelength versus the lattice constants for the different modes
            filename = 'Res_WL_Lattice_Constant.csv'

            data = np.loadtxt(filename, delimiter = ',', unpack = True)

            hv_list = []; marks = []; labels = []; 

            for i in range(1, len(data), 1):
                hv_list.append([data[0], data[i]])
                labels.append('Mode %(v1)d'%{"v1":i})
                marks.append(Plotting.labs_pts[i])

            # Make the multi plot
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.y_label = 'Resonance Wavelength (nm)'
            args.x_label = 'PhC Lattice Constant (nm)'
            #args.plt_range = [1520, 1580, 1000, 7000]
            args.fig_name = 'Res_WL_LC'
            
            Plotting.plot_multiple_linear_fit_curves(hv_list, args)

            del hv_list; del marks; del labels; del args; del data; 

            # plot the resonant wavelength versus the lattice constants for the different modes
            filename = 'Q_Fac_Lattice_Constant.csv'

            data = np.loadtxt(filename, delimiter = ',', unpack = True)

            hv_list = []; marks = []; labels = []; 

            for i in range(1, len(data), 1):
                hv_list.append([data[0], data[i]])
                labels.append('Mode %(v1)d'%{"v1":i})
                marks.append(Plotting.labs_pts[i])

            # Make the multi plot
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.y_label = 'Q-Factor'
            args.x_label = 'PhC Lattice Constant (nm)'
            #args.plt_range = [1520, 1580, 1000, 7000]
            args.fig_name = 'Q_Fac_LC'
            
            Plotting.plot_multiple_linear_fit_curves(hv_list, args)

            del hv_list; del marks; del labels; del args; del data; 

            os.chdir(cwd) # return to home directory
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot locate directory:",DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def More_Q_Factor_Plots():

    FUNC_NAME = ".More_Q_Factor_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "good_sets/"
        if os.path.isdir(DATA_HOME):
            cwd = os.getcwd() # store location of home directory

            os.chdir(DATA_HOME) # move to directory containing data
            print(os.getcwd())

            # Plot the resonance Wl versus Lattice Spacings
            file_template = "Res_WL_%(v1)d.csv"
            num_list = np.arange(1,7,1)
            hv_list = []; marks = []; labels = [];
            for i in range(0,len(num_list), 1):
                file_name = file_template%{"v1":num_list[i]}
                if glob.glob(file_name):
                    data = np.loadtxt(file_name, delimiter = ',', unpack = True)
                    hv_list.append([data[0], data[1]])
                    labels.append('Mode %(v1)d'%{"v1":i+1})
                    marks.append(Plotting.labs_pts[i])
                    del data

            # Make the multi plot
            args = Plotting.plot_arg_multiple()

            #args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.y_label = 'Resonant Wavelength (nm)'
            args.x_label = 'PhC Lattice Constant (nm)'
            args.plt_range = [380, 395, 1530, 1585]
            args.fig_name = 'Res_WL_Full'
            
            Plotting.plot_multiple_linear_fit_curves(hv_list, args)

            del hv_list; del marks; del labels; del args; 

            # Plot the Q_factors versus Lattice Spacings
            file_template = "Q_Fac_%(v1)d.csv"
            num_list = np.arange(1,7,1)
            latts = np.arange(382, 396, 2)
            hv_list = []; marks = []; labels = [];
            for i in range(0,len(num_list), 1):
                file_name = file_template%{"v1":num_list[i]}
                if glob.glob(file_name):
                    data = np.loadtxt(file_name, delimiter = ',', unpack = True)
                    hv_list.append([data[0], data[2]])
                    labels.append('Mode %(v1)d'%{"v1":i+1})
                    marks.append(Plotting.labs_pts[i])
                    del data

            # Make the multi plot
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.y_label = 'Q-Factor'
            args.x_label = 'PhC Lattice Constant (nm)'
            #args.plt_range = [380, 395, 1000, 6500]
            args.fig_name = 'Q_Fac_Full'
            
            Plotting.plot_multiple_curves(hv_list, args)
            #Plotting.plot_multiple_linear_fit_curves(hv_list, args)

            # Plot the Q_factors versus Resonant Wavelengths
            file_template = "Q_Fac_%(v1)d.csv"
            num_list = np.arange(1,6,1)
            latts = np.arange(382, 396, 2)
            hv_list = []; marks = []; labels = [];
            for i in range(0,len(num_list), 1):
                file_name = file_template%{"v1":num_list[i]}
                if glob.glob(file_name):
                    data = np.loadtxt(file_name, delimiter = ',', unpack = True)
                    hv_list.append([data[1], data[2]])
                    labels.append('Mode %(v1)d'%{"v1":i+1})
                    marks.append(Plotting.labs_pts[i])
                    del data

            # Make the multi plot
            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.crv_lab_list = labels
            args.mrk_list = marks
            args.y_label = 'Q-Factor'
            args.x_label = 'Resonant Wavelength (nm)'
            #args.plt_range = [380, 395, 1000, 6500]
            args.fig_name = 'Q_Fac_Fulller'
            
            #Plotting.plot_multiple_curves(hv_list, args)
            Plotting.plot_multiple_linear_fit_curves(hv_list, args)

            del hv_list; del marks; del labels; del args; 

            os.chdir(cwd) # return to home directory
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot locate directory:",DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)