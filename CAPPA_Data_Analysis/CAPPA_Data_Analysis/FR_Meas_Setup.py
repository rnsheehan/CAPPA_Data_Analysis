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

Conn_types = ["BNC", "N"]

def Meas_Setup_Plots():

    # run the methods needed to generate the plots
    # R. Sheehan 23 - 8 - 2018

    FUNC_NAME = ".Meas_Setup_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #DATA_HOME = "C:/Users/Robert/Research/CAPPA/Data/FR_Meas_Eq_Circ/"
        DATA_HOME = "C:/Users/Robert/Research/CAPPA/Data/Scope_SetUp_Calibration/"

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())   

            Plot_F_Swp_Data()
            
            #Plot_BW_Max_Min()

            #Avals = ['01','05','10']

            #Conn_type = 'BNC'
            ##Plot_Pwr_Split(Conn_type, Avals)
            #Plot_Pwr_Split_Comb(Conn_type, Avals)

            #Conn_type = 'N'
            ##Plot_Pwr_Split(Conn_type, Avals)
            #Plot_Pwr_Split_Comb(Conn_type, Avals)

            #Conn_type = 'BNC'
            #filename = 'FR_Meas_Simple_R_10_C_1nF_A_01.csv'
            #Plot_Vin_Vout(filename, Conn_type)
            #Plot_Response(filename, Conn_type)

        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot find",DATA_HOME)
    except Exception:
        print(ERR_STATEMENT)

def Plot_BW_Max_Min():
    # Make a plot of the Max / Min BW values that are possible for RC circuit
    # with lumped elements that are in lab
    # R. Sheehan 23 - 8 - 2018

    FUNC_NAME = ".Plot_BW_Max_Min()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # Check if the data is in the directory
        filemin = "BW_C_1nF.csv"
        filemax = "BW_C_470pF.csv"

        if glob.glob(filemin) and glob.glob(filemax):

            # read the data into memory
            datamin = Common.read_matrix(filemin)
            datamin = Common.transpose_multi_col(datamin)
            datamax = Common.read_matrix(filemax)
            datamax = Common.transpose_multi_col(datamax)

            # make a plot of the data

            hv_data = []; labels = []; marks = []
            hv_data.append(datamin); labels.append("C = 1 nF"); marks.append(Plotting.labs[0]); 
            hv_data.append(datamax); labels.append("C = 470 pF"); marks.append(Plotting.labs[1]); 

            args = Plotting.plot_arg_multiple()

            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Resistance $(\Omega)$'
            args.y_label = 'Bandwidth (MHz)'
            args.plt_title = 'RC Circuit 3dB BW'
            args.fig_name = 'RC_Circ_3dB_BW'
            #args.plt_range = [0, 50, 0, 300]
            args.log_y = False
            args.loud = True

            Plotting.plot_multiple_curves(hv_data, args)

            del hv_data; del labels; del marks; 
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def Plot_Pwr_Split(Conn_type, Aval_list):
    # Make a plot of the measured data from the power split experiment on the BNC and N connectors
    # Make the plot for different connector types
    # This plot shows the data from each arm on the same plot
    # R. Sheehan 23 - 8 - 2018

    FUNC_NAME = ".Plot_Pwr_Split()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if Conn_type in Conn_types and Aval_list is not None:

            if Conn_type == Conn_types[0]:
                scale = 1.0E+6
            else:
                scale = 1.0E+9

            for v in Aval_list: 
                file_tmplt = "Power_Split_%(v1)s_A_%(v2)s.csv"%{"v1":Conn_type, "v2":v}                
                if glob.glob(file_tmplt):

                    hv_data = []; labels = []; marks = []; 
                                        
                    # Read the data
                    data = Common.read_matrix(file_tmplt)
                    data = Common.transpose_multi_col(data)

                    for i in range(0, len(data[0]), 1): data[0][i] = data[0][i] / scale
                    
                    hv_data.append([data[0], data[1], data[2]]); 
                    #labels.append('Arm 1, A = %(v1)0.1f V$_{pp}$'%{"v1":float(v)/10.0}); 
                    labels.append('Arm 1'); 
                    marks.append( Plotting.labs[0] )

                    hv_data.append([data[0], data[3], data[4]]); 
                    labels.append('Arm 2'); 
                    marks.append( Plotting.labs[1] )

                    args = Plotting.plot_arg_multiple()

                    args.crv_lab_list = labels
                    args.mrk_list = marks
                    args.loud = False
                    args.x_label = 'Frequency (MHz)' if Conn_type == Conn_types[0] else 'Frequency (GHz)'
                    args.y_label = 'V$_{pp}$ (mV)'
                    args.plt_title = "%(v1)s output, A = %(v2)0.1f V$_{pp}$"%{ "v1":Conn_type, "v2":float(v)/10.0 }
                    args.fig_name = "Pwr_Splt_%(v1)s_A_%(v2)s"%{"v1":Conn_type, "v2":v}

                    Plotting.plot_multiple_curves_with_errors(hv_data, args)
                    
                    del data; del hv_data; del labels; del marks;
                else:
                    print(file_tmplt,"not found")
        else: 
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def Plot_Pwr_Split_Comb(Conn_type, Aval_list):
    # Make a plot of the measured data from the power split experiment on the BNC and N connectors
    # Make the plot for different connector types
    # This plot shows the data from each arm on the same plot
    # R. Sheehan 23 - 8 - 2018

    FUNC_NAME = ".Plot_Pwr_Split_Comb()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if Conn_type in Conn_types and Aval_list is not None:

            if Conn_type == Conn_types[0]:
                scale = 1.0E+6
            else:
                scale = 1.0E+9

            hv_data = []; labels = []; marks = [];
            cnt = 0

            for v in Aval_list: 
                file_tmplt = "Power_Split_%(v1)s_A_%(v2)s.csv"%{"v1":Conn_type, "v2":v}                
                if glob.glob(file_tmplt):                                         
                    # Read the data
                    data = Common.read_matrix(file_tmplt)
                    data = Common.transpose_multi_col(data)

                    for i in range(0, len(data[0]), 1): data[0][i] = data[0][i] / scale
                    
                    hv_data.append([data[0], data[1], data[2]]); 
                    labels.append('A = %(v1)0.1f V$_{pp}$'%{"v1":float(v)/10.0}); 
                    marks.append( Plotting.labs[cnt] )

                    cnt = (cnt+1)%(len(Plotting.labs))
                    del data
                else:
                    print(file_tmplt,"not found")
                    
            if len(hv_data) > 0:
                args = Plotting.plot_arg_multiple()

                args.crv_lab_list = labels
                args.mrk_list = marks
                args.loud = False
                args.x_label = 'Frequency (MHz)' if Conn_type == Conn_types[0] else 'Frequency (GHz)'
                args.y_label = 'V$_{pp}$ (mV)'
                args.plt_title = "%(v1)s output"%{ "v1":Conn_type}
                args.fig_name = "Pwr_Splt_%(v1)s"%{"v1":Conn_type}

                Plotting.plot_multiple_curves_with_errors(hv_data, args)

                del hv_data; del labels; del marks;
            else:
                raise Exception                
        else: 
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def Plot_Vin_Vout(filename, Conn_type):
    # make a plot of measured Vin and Vout data
    # R. Sheehan 23 - 8 - 2018

    FUNC_NAME = ".Plot_Vin_Vout()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if glob.glob(filename):
            hv_data = []; labels = []; marks = [];

            data = Common.read_matrix(filename)
            data = Common.transpose_multi_col(data)

            if Conn_type == Conn_types[0]:
                scale = 1.0E+6
            else:
                scale = 1.0E+9

            for i in range(0, len(data[0]), 1): data[0][i] = data[0][i] / scale

            hv_data.append([data[0], data[1], data[2]]); 
            #labels.append('Arm 1, A = %(v1)0.1f V$_{pp}$'%{"v1":float(v)/10.0}); 
            labels.append('V$_{in}$'); 
            marks.append( Plotting.labs[0] )

            hv_data.append([data[0], data[3], data[4]]); 
            labels.append('V$_{out}$'); 
            marks.append( Plotting.labs[1] )

            args = Plotting.plot_arg_multiple()

            args.crv_lab_list = labels
            args.mrk_list = marks
            args.loud = True
            args.x_label = 'Frequency (MHz)' if Conn_type == Conn_types[0] else 'Frequency (GHz)'
            args.y_label = 'V$_{pp}$ (mV)'
            #args.plt_title = "%(v1)s output"%{ "v1":Conn_type}
            #args.fig_name = "Pwr_Splt_%(v1)s"%{"v1":Conn_type}
            args.fig_name = "%(v1)s_Vin_Vout"%{"v1":filename.replace('.csv','')}

            Plotting.plot_multiple_curves_with_errors(hv_data, args)
                    
            del hv_data; del labels; del marks;
        else:
            print(filename,"not found")
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def Plot_Response(filename, Conn_type):
    # make a plot of measured Response data
    # R. Sheehan 23 - 8 - 2018

    FUNC_NAME = ".Plot_Response()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if glob.glob(filename):
            hv_data = []; labels = []; marks = [];

            data = Common.read_matrix(filename)
            data = Common.transpose_multi_col(data)

            if Conn_type == Conn_types[0]:
                scale = 1.0E+6
            else:
                scale = 1.0E+9

            # scale the frequency data
            # Compute the response from the data
            v_data = []
            ref_lev = data[3][0] / data[1][0]
            for i in range(0, len(data[0]), 1): 
                data[0][i] = data[0][i] / scale
                r_val = data[3][i] / data[1][i]                
                v_data.append( Common.convert_dB(r_val, ref_lev) )

            args = Plotting.plot_arg_single()

            args.loud = True
            args.x_label = 'Frequency (MHz)' if Conn_type == Conn_types[0] else 'Frequency (GHz)'
            args.y_label = '|H(f) (dB)|'
            #args.plt_title = "%(v1)s output"%{ "v1":Conn_type}
            args.fig_name = "%(v1)s_Response"%{"v1":filename.replace('.csv','')}

            Plotting.plot_single_curve(data[0], v_data, args)
                    
            del data; del v_data; 
        else:
            print(filename,"not found")
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def Plot_F_Swp_Data():
    # plot the measured frequency sweep data
    # R. Sheehan 15 - 11 - 2018

    FUNC_NAME = ".Plot_F_Swp_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        filelist = []
        vals = ['01', '05', '07', '10']
        vpp = [0.1, 0.5, 0.7, 1.0]
        for v in vals:
            filename = "Rf_Swp_Vpp_%(v1)s.txt"%{"v1":v}
            if glob.glob(filename):
                filelist.append(filename)

        if len(filelist) > 0:
            # plot the imported data
            hv_data = []; labels = []; marks = []

            count = 0
            for f in filelist:
                data = Common.read_matrix(f, '\t')
                data = Common.transpose_multi_col(data)
                hv_data.append([data[0],data[5]]); labels.append("$V_{pp} = %(v1)0.1f$"%{"v1":vpp[count]}); marks.append(Plotting.labs[count]);
                #hv_data.append([data[0],data[2], data[3]]); labels.append("$V_{pp} = %(v1)0.1f$"%{"v1":vpp[count]}); marks.append(Plotting.labs[count]);
                #hv_data.append([data[0],data[4], data[5]]); labels.append("$V_{pp} = %(v1)0.1f$"%{"v1":vpp[count]}); marks.append(Plotting.labs[count]);
                count = (count+1)%len(Plotting.labs)

            args = Plotting.plot_arg_multiple()

            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Frequency (Hz)'
            args.y_label = 'Amplitude Variation (V)'
            args.fig_name = 'DeltaVamp'
            #args.plt_range = [0, 50, 0, 300]
            args.log_x = False
            args.log_y = False
            args.loud = True

            Plotting.plot_multiple_curves(hv_data, args)

            #Plotting.plot_multiple_curves_with_errors(hv_data, args)

            del hv_data; del labels; del marks; 
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)