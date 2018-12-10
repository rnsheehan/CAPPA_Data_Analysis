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

MOD_NAME_STR = "FR_Meas_Setup" # use this in exception handling messages

Conn_types = ["BNC", "N"]

def Meas_Setup_Plots():

    # run the methods needed to generate the plots
    # R. Sheehan 23 - 8 - 2018

    FUNC_NAME = ".Meas_Setup_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        #DATA_HOME = "C:/Users/Robert/Research/CAPPA/Data/FR_Meas_Eq_Circ/"
        #DATA_HOME = "C:/Users/Robert/Research/CAPPA/Data/Scope_SetUp_Calibration/"
        DATA_HOME = "C:/Users/Robert/Research/CAPPA/Data/PhC_FR_Swp/"

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())   

            Make_Rsp_Plot()

            #Plot_F_Swp_Data()

            #Plot_2_chan_F_Swp_Data()

            #Plot_Averaged_Output()

            #Plot_2_chan_Averaged_Output()

            #Plot_2_chan_Averaged_Output()
            
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

def Plot_2_chan_F_Swp_Data():
    # plot the measured frequency sweep data from the two channel sweep measurements
    # R. Sheehan 21 - 11 - 2018

    FUNC_NAME = ".Plot_2_chan_F_Swp_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        filelist = []
        vals = ['01', '05', '07', '10']
        vpp = [0.1, 0.5, 0.7, 1.0]
        for v in vals:
            filename = "2_chan_Rf_Swp_Vpp_%(v1)s.txt"%{"v1":v}
            if glob.glob(filename):
                filelist.append(filename)

        if len(filelist) > 0:
            # plot the imported data
            hv_data = []; labels = []; marks = []

            count = 0
            for f in filelist:
                data = Common.read_matrix(f, '\t')
                data = Common.transpose_multi_col(data)
                #hv_data.append([data[0], data[5]]); labels.append("$V_{pp} = %(v1)0.1f$"%{"v1":vpp[count]}); marks.append(Plotting.labs_lins[count]);
                #hv_data.append([data[0], data[11]]); labels.append("$V_{pp} = %(v1)0.1f$"%{"v1":vpp[count]}); marks.append(Plotting.labs_dashed[count]);
                hv_data.append([data[0], data[3]]); labels.append("$V_{pp} = %(v1)0.1f$"%{"v1":vpp[count]}); marks.append(Plotting.labs_lins[count]);
                hv_data.append([data[0], data[9]]); labels.append("$V_{pp} = %(v1)0.1f$"%{"v1":vpp[count]}); marks.append(Plotting.labs_dashed[count]);
                #hv_data.append([data[0], data[2], data[3]]); labels.append("$V_{pp} = %(v1)0.1f$"%{"v1":vpp[count]}); marks.append(Plotting.labs_lins[count]);
                #hv_data.append([data[0], data[8], data[9]]); labels.append("$V_{pp} = %(v1)0.1f$"%{"v1":vpp[count]}); marks.append(Plotting.labs_dashed[count]);
                #hv_data.append([data[0],data[4], data[5]]); labels.append("$V_{pp} = %(v1)0.1f$"%{"v1":vpp[count]}); marks.append(Plotting.labs_lins[count]);
                #hv_data.append([data[0],data[10], data[11]]); labels.append("$V_{pp} = %(v1)0.1f$"%{"v1":vpp[count]}); marks.append(Plotting.labs_dashed[count]);
                count = (count+1)%len(Plotting.labs)

            args = Plotting.plot_arg_multiple()

            args.crv_lab_list = labels
            args.mrk_list = marks
            args.x_label = 'Frequency (Hz)'
            args.y_label = 'Pk-to-Pk Variation (V)'
            args.fig_name = '2_chan_deltaPk2Pk'
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

def Plot_Averaged_Output():
    # plot the averaged output for each Vpp value
    # R. Sheehan 21 - 11 - 2018

    FUNC_NAME = ".Plot_Averaged_Output()" # use this in exception handling messages
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

            averages = []
            stdevs = []
            for f in filelist:
                data = Common.read_matrix(f, '\t')
                data = Common.transpose_multi_col(data)
                mean = np.mean(np.asarray(data[4]))
                stdev = np.std(np.asarray(data[4]))
                averages.append(mean)
                stdevs.append(stdev)

            print(vpp)
            print(averages)
            print(stdevs)

            #filename = 'One_chan_average_Ampl.txt'
            #Common.write_data(filename, averages)

            #filename = 'One_chan_stdev_Ampl.txt'
            #Common.write_data(filename, stdevs)

            #Common.linear_fit(np.asarray(vpp), np.asarray(averages), [0.0, 1.0], loud = True)

            args = Plotting.plot_arg_single()

            args.x_label = 'SRS SG386 BNC $V_{pp}$ (V)'
            args.y_label = 'Measured Amplitude  (V)'
            args.fig_name = 'One_chan_Va_meas'
            args.plt_range = [0.0, 1.1, 0.0, 1.1]
            args.loud = True

            #Plotting.plot_single_curve_with_errors(vpp, averages, stdevs, args)
            Plotting.plot_single_linear_fit_curve(vpp, averages, args)                
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def Plot_2_chan_Averaged_Output():
    # plot the averaged output for each Vpp value
    # R. Sheehan 21 - 11 - 2018

    FUNC_NAME = ".Plot_2_chan_Averaged_Output()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        filelist = []
        vals = ['01', '05', '07', '10']
        vpp = [0.1, 0.5, 0.7, 1.0]
        for v in vals:
            filename = "2_chan_Rf_Swp_Vpp_%(v1)s.txt"%{"v1":v}
            if glob.glob(filename):
                filelist.append(filename)

        if len(filelist) > 0:
            # plot the imported data
            hv_data = []; labels = []; marks = []

            averages_ch1 = []
            averages_ch2 = []
            stdevs_ch1 = []
            stdevs_ch2 = []
            for f in filelist:
                data = Common.read_matrix(f, '\t')
                data = Common.transpose_multi_col(data)
                
                mean = np.mean(np.asarray(data[4]))
                stdev = np.std(np.asarray(data[4]))
                averages_ch1.append(mean)
                stdevs_ch1.append(stdev)

                mean = np.mean(np.asarray(data[10]))
                stdev = np.std(np.asarray(data[10]))
                averages_ch2.append(mean)
                stdevs_ch2.append(stdev)

            #print(vpp)
            #print(averages_ch1)
            #print(stdevs_ch1)
            #print(averages_ch2)
            #print(stdevs_ch2)

            Common.linear_fit(np.asarray(vpp), np.asarray(averages_ch1), [0.0, 1.0], True)

            Common.linear_fit(np.asarray(vpp), np.asarray(averages_ch2), [0.0, 1.0], True)

            #filename = 'Two_chan_average_Ampl_1.txt'
            #Common.write_data(filename, averages_ch1)

            #filename = 'Two_chan_stdev_Ampl_1.txt'
            #Common.write_data(filename, stdevs_ch1)

            #filename = 'Two_chan_average_Ampl_2.txt'
            #Common.write_data(filename, averages_ch2)

            #filename = 'Two_chan_stdev_Ampl_2.txt'
            #Common.write_data(filename, stdevs_ch2)

            #Common.linear_fit(np.asarray(vpp), np.asarray(averages), [0.0, 1.0], loud = True)

            filename = "One_chan_average_Ampl.txt"
            averages = Common.read_data(filename)

            args = Plotting.plot_arg_multiple()

            hv_data = []; labels = []; marks = []

            hv_data.append([vpp, averages]); labels.append("SRS SG386"); marks.append(Plotting.labs_lins[0])
            hv_data.append([vpp, averages_ch1]); labels.append("Ch. 1"); marks.append(Plotting.labs_lins[1])
            hv_data.append([vpp, averages_ch2]); labels.append("Ch. 2"); marks.append(Plotting.labs_lins[1])

            args.mrk_list = marks
            args.crv_lab_list = labels
            args.x_label = 'SRS SG386 BNC $V_{pp}$ (V)'
            args.y_label = 'Measured Amplitude  (V)'
            args.fig_name = 'Two_chan_Va_meas'
            args.plt_range = [0.0, 1.1, 0.0, 1.1]
            args.loud = True

            Plotting.plot_multiple_linear_fit_curves(hv_data, args)

            del hv_data; del labels; del marks;                 
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def Plot_Swp_Data():
    #

    pass

def Make_Rsp_Plot():
    # driver for the Plot_Rsp_Data method
    # R. Sheehan 21 - 11 - 2018

    FUNC_NAME = ".Make_Rsp_Plot()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        filelist = []
        lablist = []

        ##name_template = 'Brd_Rsp_Data'
        ##name_template = 'R_46_Rsp_Data'
        #name_template = 'R_46_C_470_pF_Rsp_Data'
        ##name_template = 'R_46_C_47_nF_Rsp_Data'
        #vals = ['01', '05', '07', '10']
        #vpp = [0.1, 0.5, 0.7, 1.0]
        #for v in range(0, len(vals), 1):
        #    filename = "%(v2)s_%(v1)s.txt"%{"v2":name_template, "v1":vals[v]}
        #    if glob.glob(filename):
        #        filelist.append(filename)
        #        lablist.append("$V_{pp}$ = %(v1)0.1f V"%{"v1":vpp[v]})

        name_template = 'SRS_small_sig_output'
        vals = ['005', '01', '02', '03']
        vpp = [0.05, 0.1, 0.2, 0.3]
        noyes = ['no', 'yes']
        #for v in range(0, len(vals), 1):
        #    #filename = "SRS_Vpp_%(v1)s_2m_cbl_btee_%(v2)s.txt"%{"v1":vals[v], "v2":noyes[0]}
        #    filename = "SRS_Vpp_%(v1)s_2m_cbl_btee_%(v2)s.txt"%{"v1":vals[v], "v2":noyes[1]}
        #    if glob.glob(filename):
        #        filelist.append(filename)
        #        lablist.append("$V_{pp}$ = %(v1)0.2f V"%{"v1":vpp[v]})

        vppchce = 2
        for v in range(0, len(noyes), 1):
            filename = "SRS_Vpp_%(v1)s_2m_cbl_btee_%(v2)s.txt"%{"v1":vals[vppchce], "v2":noyes[v]}
            if glob.glob(filename):
                filelist.append(filename)
                lablist.append("$V_{pp}$ = %(v1)0.2f V, Bias Tee: %(v2)s"%{"v1":vpp[vppchce], "v2":noyes[v]})

        v = 1
        filename = "SRS_Vpp_%(v1)s_2m_cbl_btee_%(v2)s_del_750.txt"%{"v1":vals[vppchce], "v2":noyes[v]}
        if glob.glob(filename):
            filelist.append(filename)
            lablist.append("$V_{pp}$ = %(v1)0.2f V, Bias Tee: %(v2)s, $\Delta$ = 750 ms"%{"v1":vpp[vppchce], "v2":noyes[v]})

        v = 1
        filename = "SRS_Vpp_%(v1)s_2m_cbl_btee_%(v2)s_mdel_500.txt"%{"v1":vals[vppchce], "v2":noyes[v]}
        if glob.glob(filename):
            filelist.append(filename)
            lablist.append("$V_{pp}$ = %(v1)0.2f V, Bias Tee: %(v2)s, $\Delta$ = 500 ms"%{"v1":vpp[vppchce], "v2":noyes[v]})

        v = 1
        filename = "SRS_Vpp_%(v1)s_2m_cbl_btee_%(v2)s_tdel_750.txt"%{"v1":vals[vppchce], "v2":noyes[v]}
        if glob.glob(filename):
            filelist.append(filename)
            lablist.append("$V_{pp}$ = %(v1)0.2f V, Bias Tee: %(v2)s, $t\Delta$ = 750 ms"%{"v1":vpp[vppchce], "v2":noyes[v]})

        #figname = name_template + 'btee_yes_plot'
        figname = name_template + '_splot'
        plt_pk2pk = True
        include_errors = True
        scale_dB = False
        Plot_Rsp_Data(filelist, lablist, figname, plt_pk2pk, include_errors, scale_dB)

    except Exception:
        print(ERR_STATEMENT)

def Plot_Rsp_Data(filelist, lablist, figname, plt_pk2pk, include_errors, scale_dB):
    # filelist is the list of files with data to be plotted
    # Plot the measured response data
    # plt_pk2pk decides whether to plot the pk2pk response or amplitude reponse
    # include_errors decides whether or not to include the measured error in the plot
    # R. Sheehan 21 - 11 - 2018

    FUNC_NAME = ".Plot_Rsp_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if len(filelist) == 0 else False
        c2 = True if filelist == None else False
        c3 = True if len(lablist) == 0 else False
        c4 = True if lablist == None else False
        c5 = True if math.fabs(len(lablist) - len(filelist)) > 0 else False
        c6 = True if c1 or c2 or c3 or c4 or c5 else False

        if c6:
            raise Exception
        else:
            # Can't do an error bar plot on dB scale
            incl_errors = False if scale_dB == True else include_errors

            hv_data = []; marks = []; labels = []

            frqcol = 0
            datacol = 2 if plt_pk2pk else 4
            errcol = 3 if plt_pk2pk else 5

            delim = '\t'
            count = 0; 
            for f in range(0, len(lablist), 1):
                data = Common.read_matrix(filelist[f], delim)
                data = Common.transpose_multi_col(data)
                if incl_errors:
                    hv_data.append([data[frqcol], data[datacol], data[errcol]]); 
                    marks.append(Plotting.labs_lins[count]); labels.append(lablist[f]);
                else:
                    if scale_dB:
                        for j in range(0, len(data[datacol]), 1):
                            data[datacol][j] = Common.convert_dB(data[datacol][j], 1.0); 
                    hv_data.append([data[frqcol], data[datacol]]); 
                    marks.append(Plotting.labs_lins[count]); labels.append(lablist[f]);
                count = (count + 1)%len(Plotting.labs)

            # record start and end frequencies
            fr_start = hv_data[0][0][0]
            fr_end = hv_data[0][0][-1]
            #fr_end = 20e+6
            r_start = 0.0 if scale_dB == False else -20
            r_end = 1.0 if scale_dB == False else 1.0

            args = Plotting.plot_arg_multiple()

            args.mrk_list = marks
            args.crv_lab_list = labels
            args.x_label = 'Frequency (Hz)'
            args.y_label = 'Pk-to-Pk Response' if plt_pk2pk else 'Amplitude Response'
            if scale_dB: args.y_label = args.y_label + ' (dB)'
            args.fig_name = figname
            args.plt_range = [fr_start, fr_end, r_start, r_end]
            args.loud = True

            if incl_errors:
                Plotting.plot_multiple_curves_with_errors(hv_data, args)
            else:
                Plotting.plot_multiple_curves(hv_data, args)

            del hv_data; del labels; del marks;
    except Exception:
        print(ERR_STATEMENT)

def FFT_testing():
    # plot the computed FFT data
    # R. Sheehan 7 - 12 - 2018

    FUNC_NAME = ".FFT_testing()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        pass
    except Exception:
        print(ERR_STATEMENT)