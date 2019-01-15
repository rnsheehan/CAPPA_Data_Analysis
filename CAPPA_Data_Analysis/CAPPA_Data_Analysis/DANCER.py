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

# Make plots of the data obtained during measurements for DANCER related devices
# R. Sheehan 15 - 1 - 2019

MOD_NAME_STR = "DANCER" # use this in exception handling messages

Conn_types = ["BNC", "N"]

def DANCER_Plots():

    # run the methods needed to generate the plots
    # R. Sheehan 15 - 1 - 2019

    FUNC_NAME = ".DANCER_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "C:/Users/Robert/Research/CAPPA/Data/PhC_FR_Swp/"

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())  
            
            plot_PhC_stimulus(False)
            
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot find",DATA_HOME)
    except Exception:
        print(ERR_STATEMENT)

def plot_PhC_spctrm():
    # plot the optical spectrum as measured through the PhC device under an applied bias
    # R. Sheehan 15 - 1 - 2019

    FUNC_NAME = ".plot_PhC_spctrm()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        wl_file = "TLS_WL.txt"
        pow_file = "PhC_Pout_uW_Vd_26.txt"

        if glob.glob(wl_file) and glob.glob(pow_file):
            wl_data = Common.read_data(wl_file)
            pow_data = Common.read_data(pow_file)

            if wl_data is not None and pow_data is not None:

                #wl_data = Common.scale_data(np.asarray(wl_data), 1000.0) # convert the nm data to um

                args = Plotting.plot_arg_single()

                args.loud = True
                args.x_label = 'Wavelength ($\mu$m)'
                args.y_label = 'PhC Output Power ($\mu$W)'
                args.fig_name = 'PhC_Output_Power_Vd_26'

                Plotting.plot_single_curve(wl_data, pow_data, args)

                del wl_data; del pow_data; 
            else:
                raise Exception
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def plot_PhC_bias():
    # plot the optical spectrum as measured through the PhC device while bias is varied at fixed input wavelength
    # R. Sheehan 15 - 1 - 2019

    FUNC_NAME = ".plot_PhC_bias()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        bias_file = "PhC_Bias_WL_1567p8.txt"
        pow_file = "PhC_Pout_uW_WL_1567p8.txt"

        if glob.glob(bias_file) and glob.glob(pow_file):
            bias_data = Common.read_data(bias_file)
            pow_data = Common.read_data(pow_file)

            if bias_data is not None and pow_data is not None:
                args = Plotting.plot_arg_single()

                args.loud = True
                args.x_label = 'PhC Bias (V)'
                args.y_label = 'PhC Output Power ($\mu$W)'
                args.fig_name = 'PhC_Output_Power_WL_1567p8'

                Plotting.plot_single_curve(bias_data, pow_data, args)

                del bias_data; del pow_data; 
            else:
                raise Exception
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def plot_PhC_stimulus(input = True):
    # plot the AC bias applied to the PhC and the AC response measured from the PhC
    # R. Sheehan 15 - 1 - 2019

    FUNC_NAME = ".plot_PhC_stimulus()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        fr_file = "Swp_FR_MHz.txt"
        resp_file_1 = "Vin_BNC_Vpp_03.txt" if input else "Vout_HSPD_Vpp_03.txt"
        resp_file_2 = "Vin_BNC_Vpp_05.txt" if input else "Vout_HSPD_Vpp_05.txt"

        if glob.glob(fr_file) and glob.glob(resp_file_1) and glob.glob(resp_file_2):
            fr_data = Common.read_data(fr_file)
            resp_data_1 = Common.read_data(resp_file_1)
            resp_data_2 = Common.read_data(resp_file_2)

            if fr_data is not None and resp_data_1 is not None and resp_data_2 is not None:
                hv_data = []; marks = []; labels = []

                if input == False: 
                    # scale the Vpp data to mV
                    resp_data_1 = Common.scale_data(np.asarray(resp_data_1), 1.0e+3)
                    resp_data_2 = Common.scale_data(np.asarray(resp_data_2), 1.0e+3)

                hv_data.append([fr_data, resp_data_1]); marks.append(Plotting.labs[0]); labels.append('$V_{pp}$ = 0.3 V')
                hv_data.append([fr_data, resp_data_2]); marks.append(Plotting.labs[1]); labels.append('$V_{pp}$ = 0.5 V')

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.x_label = 'Frequency (MHz)'
                args.y_label = 'Input $V_{pp}$ (V)' if input else 'Output $V_{pp}$ (mV)'
                args.fig_name = 'PhC_Vin' if input else 'PhC_Vout'
                args.crv_lab_list = labels
                args.mrk_list = marks

                Plotting.plot_multiple_curves(hv_data, args)
                
                del fr_data; del resp_data_1; del resp_data_2;                 
            else:
                raise Exception
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def plot_PhC_response(scale_horz = False):
    # plot the response of the PhC to the input signal
    # response is taken to be the ratio of the output / input signals
    # R. Sheehan 15 - 1 - 2019

    FUNC_NAME = ".plot_PhC_stimulus()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        fr_file = "Swp_FR_MHz.txt"
        resp_file_1 = "Vin_BNC_Vpp_03.txt"        
        resp_file_11 = "Vout_HSPD_Vpp_03.txt"

        resp_file_2 = "Vin_BNC_Vpp_05.txt"
        resp_file_12 = "Vout_HSPD_Vpp_05.txt"

        if glob.glob(fr_file) and glob.glob(resp_file_1) and glob.glob(resp_file_2) and glob.glob(resp_file_11) and glob.glob(resp_file_12):
            fr_data = Common.read_data(fr_file)
            resp_data_1 = Common.read_data(resp_file_1)
            resp_data_2 = Common.read_data(resp_file_2)
            resp_data_11 = Common.read_data(resp_file_11)
            resp_data_12 = Common.read_data(resp_file_12)

            if fr_data is not None and resp_data_1 is not None and resp_data_2 is not None and resp_data_11 is not None and resp_data_12 is not None:

                if scale_horz:
                    fr_data = Common.scale_data(np.asarray(fr_data), 1000); 

                # compute the electrical reponse of the device
                resp_03 = []; resp_05 = [];
                ref_level_03 = resp_data_11[0] / resp_data_1[0]; 
                ref_level_05 = resp_data_12[0] / resp_data_2[0]; 
                for i in range(0, len(resp_data_1), 1):
                    response = resp_data_11[i] / resp_data_1[i]
                    resp_03.append( Common.convert_dB( response , ref_level_03 ) )

                    response = resp_data_12[i] / resp_data_2[i]
                    resp_05.append( Common.convert_dB( response , ref_level_05 ) )


                hv_data = []; marks = []; labels = []

                hv_data.append([fr_data, resp_03]); marks.append(Plotting.labs[0]); labels.append('$V_{pp}$ = 0.3 V')
                hv_data.append([fr_data, resp_05]); marks.append(Plotting.labs[1]); labels.append('$V_{pp}$ = 0.5 V')

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.x_label = 'Frequency (kHz)' if scale_horz else 'Frequency (MHz)'
                args.y_label = 'Response (dB)'
                args.fig_name = 'PhC_Response'
                args.crv_lab_list = labels
                args.mrk_list = marks

                Plotting.plot_multiple_curves(hv_data, args)
                
                del fr_data; del resp_data_1; del resp_data_2;                 
            else:
                raise Exception
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)
