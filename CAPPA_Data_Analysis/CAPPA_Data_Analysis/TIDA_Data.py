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
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT);print(e);

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
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT);print(e);

def Plot_Dispersion_Curve_Data():
    # plot the computed SiN Wire WG dispersion curve data for the AWG
    # R. Sheehan 17 - 4 - 2019

    FUNC_NAME = ".Plot_Dispersion_Curve_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/TIDA/SiN_AWG_Design/'
        
        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME); 
            
            hval = 0.3; 

            wlist = np.arange(1, 2.25, 0.25); 

            neff_avg = np.zeros( len(wlist) ); ng_avg = np.zeros( len(wlist) ); 

            pol_str = 'TM'

            avg_file = open('Average_Index_Values_%(v1)s.txt'%{"v1":pol_str}, 'w')

            filelist = []

            for i in range(0, len(wlist), 1):
                filename = "Wire_WG_Dispersion_W_%(v1)0.2f_H_%(v2)0.2f_%(v3)s.txt"%{"v1":wlist[i], "v2":hval, "v3":pol_str}
                if glob.glob(filename):
                    ret_val = Plot_single_disp_data_set(filename, True)
                    neff_avg[i] = ret_val[0]; ng_avg[i] = ret_val[1]; 
                    avg_file.write("%(v1)0.2f, %(v2)0.3f, %(v3)0.3f\n"%{"v1":wlist[i], "v2":ret_val[0], "v3":ret_val[1]})
                    filelist.append(filename)

            avg_file.close()

            # Make a plot of the average indices versus WG width
            args = Plotting.plot_arg_multiple()

            args.x_label = 'Waveguide Width ($\mu$m)'
            args.y_label = 'Average Index'
            args.mrk_list = [Plotting.labs[0], Plotting.labs[1]]
            args.crv_lab_list = ['$<n_{eff}>$', '$<n_{g}>$']
            args.loud = False
            args.fig_name = 'Average_Indices_%(v1)s'%{"v1":pol_str}

            Plotting.plot_multiple_curves([ [wlist, neff_avg], [wlist, ng_avg] ], args)

        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT);print(e);

def Plot_single_disp_data_set(filename, loud = False):
    # make a plot of the data inside a single file
    # plot the effective index and the group index on the same plot
    # R. Sheehan 17 - 4 - 2019

    FUNC_NAME = ".Plot_single_disp_data_set()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if glob.glob(filename):
            data = np.loadtxt(filename, delimiter = ',', unpack = True);

            neff_mean = np.mean(data[1]); ng_mean = np.mean(data[2])
            neff_range = 0.5*(np.max(data[1])-np.min(data[1])); 
            ng_range = 0.5*(np.max(data[2])-np.min(data[2])); 
            
            if loud:
                print(filename)
                print("n_{eff} =",neff_mean,"+/-", neff_range)
                print("rel. err n_{eff} =",200*(neff_range/neff_mean) )
                print("n_{g} =",ng_mean,"+/-",ng_range )
                print("rel. err n_{g} =",200*(ng_range/ng_mean) )
                print("")

            # make a plot of the data in the file
            args = Plotting.plot_arg_multiple()

            args.loud = loud
            args.x_label = 'Wavelength ($\mu$m)'
            args.y_label = 'Index Value'
            args.mrk_list = [Plotting.labs[0], Plotting.labs[1]]
            args.crv_lab_list = ['$n_{eff}(\lambda)$', '$n_{g}(\lambda)$']
            args.fig_name = filename.replace('.txt','').replace('.','')

            Plotting.plot_multiple_curves([[data[0], data[1]], [data[0], data[2]]], args)

            del args; del data; 

            return [neff_mean, ng_mean]
        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT);print(e);

def Plot_coupling_coeff(loud = False):
    # plot the simulated coupling coefficients for the different WG widths
    # R. Sheehan 17 - 4 - 2019

    FUNC_NAME = ".Plot_coupling_coeff()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/TIDA/SiN_AWG_Design/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            wlist = np.arange(1, 2.25, 0.25);

            hv_list = []; labels = []; marks = []

            WL = 1535; 

            for i in range(0, len(wlist), 1):
                filename = "Coupling_Coeff_W_%(v1)0.2f_TE_WL_%(v2)d.txt"%{"v1":wlist[i], "v2":WL}

                if glob.glob(filename):
                    data = np.loadtxt(filename, delimiter = ',', unpack = True)
                    hv_list.append(data); marks.append(Plotting.labs[i]); labels.append("W = %(v1)0.2f"%{"v1":wlist[i]})

            if len(hv_list) > 0:
                args = Plotting.plot_arg_multiple()

                args.loud = loud
                args.x_label = 'Waveguide Separation ($\mu$m)'
                args.y_label = 'Coupling Coefficient $(\mu m)^{-1}$'
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.log_y = True
                args.fig_name = 'WaveguideCouplingCoefficients_%(v1)d'%{"v1":WL}
                args.plt_title = '$\lambda$ = %(v1)d nm'%{"v1":WL}

                Plotting.plot_multiple_curves(hv_list, args)
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT);print(e);

def Filter_Data(loud = False):

    # plot the measured filter bias versus output wavelength for the Micron Optics FP filter FFP-C Tunable Filter
    # R. Sheehan 1 - 7 - 2019

    FUNC_NAME = ".Filter_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/Filter_Analysis/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            filename = "Filter_Data.csv"

            if glob.glob(filename):
                data = np.loadtxt(filename, skiprows = 1, delimiter = ',', unpack = True)

                if data is not None:
                    print(filename,"read successfully")
                    print("No. columns:",len(data),", No. rows:",len(data[0]))

                    arguments = Plotting.plot_arg_single()

                    # Plot the set DC bias versus the locked DC bias
                    arguments.x_label = 'Set DC Offset (V)'
                    arguments.y_label = 'Locked DC Offset (V)'
                    arguments.loud = True
                    arguments.fig_name = 'Set_versus_Locked_DC_Offset'

                    Plotting.plot_single_linear_fit_curve(data[0], data[1], arguments)

                    # plot the DC bias versus output wavelength
                    arguments.x_label = 'Locked DC Offset (V)'
                    arguments.y_label = 'Measured Wavelength (nm)'
                    arguments.loud = True
                    arguments.fig_name = 'Wavelength_versus_DC_Offset'

                    Plotting.plot_single_linear_fit_curve(data[1], data[2], arguments)

                    # plot the wavelength versus spectral power
                    arguments.y_label = 'Power (dBm / 0.01 nm)'
                    arguments.x_label = 'Measured Wavelength (nm)'
                    arguments.loud = True
                    arguments.fig_name = 'Power_versus_Wavelength'

                    Plotting.plot_single_curve(data[2], data[3], arguments)

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
        print(ERR_STATEMENT)
        print(e)

def Filter_Spectrum():
    # plot the SOA spectrum along with it's filtered spectrum
    # R. Sheehan 10 - 10 - 2019

    FUNC_NAME = ".Filter_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/Filter_Analysis/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            file_0 = "OSA_Filt_0.csv"
            file_1 = "OSA_Filt_1.csv"

            if glob.glob(file_0) and glob.glob(file_1):
                data_0 = np.loadtxt(file_0, delimiter = ',', unpack = True)
                data_1 = np.loadtxt(file_1, delimiter = ',', unpack = True)

                hv_list = []; markers = []; labels = []; 

                hv_list.append(data_0); markers.append(Plotting.labs_lins[0]); labels.append('SOA Spectrum'); 
                hv_list.append(data_1); markers.append(Plotting.labs_lins[1]); labels.append('Filtered SOA Spectrum'); 

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = markers
                args.plt_range = [1550, 1560, -85, -30]
                args.fig_name ='SOA_Filtered'

                Plotting.plot_multiple_curves(hv_list, args)

            else:
                ERR_STATEMENT = ERR_STATEMENT + "Cannot locate files\n"
                raise Exception
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)