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

            plot_PhC_response(True)
            
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
        #resp_file_11 = "100_1000kHz_step_50kHzpk_pk.dat"

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


                Common.write_data('fr_data.txt',fr_data)
                Common.write_data('resp_03_data.txt',resp_03)
                Common.write_data('resp_05_data.txt',resp_05)

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

def plot_IV_curve(log_scale = False):
    # plot the measured IV curve for the PhC device
    # R. Sheehan 16 - 1 - 2019

    FUNC_NAME = ".plot_IV_curve()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        bias_file = "V_PhC_V.txt"
        curr_file = "I_PhC_mA.txt"

        if glob.glob(bias_file) and glob.glob(curr_file):
            bias_data = Common.read_data(bias_file)
            curr_data = Common.read_data(curr_file)

            if bias_data is not None and curr_data is not None:

                if log_scale:
                    # scale the current data so it can be plotted on log scale
                    for i in range(0, len(curr_data), 1):
                        if curr_data[i] < 0.0:
                            curr_data[i] *= -1.0e-3
                        else:
                            curr_data[i] *= 1.0e-3

                args = Plotting.plot_arg_single()

                args.loud = True
                args.x_label = 'PhC Bias (V)'
                args.y_label = 'PhC Current (A)' if log_scale else 'PhC Current (mA)'
                if log_scale: args.log_y = True
                args.fig_name = 'PhC_IV'

                Plotting.plot_single_curve(bias_data, curr_data, args)

                del bias_data; del curr_data; 
            else:
                raise Exception
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def estimate_PhC_resistance():
    # using equivalent circuit model estimate the PhC diode resistance
    # R. Sheehan 16 - 1 - 2019

    FUNC_NAME = ".plot_IV_curve()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        bias_file = "V_PhC_V.txt"
        curr_file = "I_PhC_mA.txt"

        if glob.glob(bias_file) and glob.glob(curr_file):
            bias_data = Common.read_data(bias_file)
            curr_data = Common.read_data(curr_file)

            if bias_data is not None and curr_data is not None:

                # extract the forward bias data
                hor_data = []; ver_data = []
                for i in range(0, len(bias_data), 1):
                    if bias_data[i] > 0.0:
                        ver_data.append(bias_data[i])
                        hor_data.append(curr_data[i])

                T = 25; 

                popt = diode_fit(hor_data, ver_data, T)

                ver_fit = []
                for i in range(0, len(hor_data), 1):
                    ver_fit.append( diode_voltage(hor_data[i], popt[0], popt[1], popt[2], T) )

                # plot forward bias data with fit for good measure

                hv_data = []; marks = []; labels = []
                hv_data.append([hor_data, ver_data]); marks.append(Plotting.labs_pts[0]); labels.append('Data')
                hv_data.append([hor_data, ver_fit]); marks.append(Plotting.labs_lins[1]); labels.append('Fit')

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.x_label = 'Current (mA)'
                args.y_label = 'Voltage (V)'
                args.crv_lab_list = labels
                args.mrk_list = marks
                args.fig_name ='IV_data_with_Fit'

                Plotting.plot_multiple_curves(hv_data, args)

                del bias_data; del curr_data; 
            else:
                raise Exception
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def diode_voltage(x, eta, rs, eye0, T):
    # ideal diode equation inverted for voltage with Ohm's law contribution
    # across diode included, see Tyndall Notebook 2353, page 100
    # (k_{B} / q) = 8.61733e-5 [J / C K]
    # series resistance needs to have negative sign for some reason
    # what does eye0 represent? 

    # need to define temperature as a global variable so that it gets assigned when function is called
    T_term = 8.61733e-5*Common.convert_C_K(T) # at T = 25 C T_term = 0.0256926 [J/C]
    
    return ( eta*T_term*np.log( 1.0 + x*eye0 ) - rs*x )

def diode_fit(hor_data, vert_data, T):
    # fit the diode voltage equation to the data
    # Temperature T is input in units of deg C
    # T is converted to units of K inside function diode_voltage

    from scipy.optimize import curve_fit

    params = ['eta', 'R_{s}', 'I_{0}']

    # lambda function needed to include temperature dependence in fit calculations
    #https://docs.python.org/2/tutorial/controlflow.html#lambda-expressions

    popt, pcov = scipy.optimize.curve_fit( lambda x, eta, rs, eye0: diode_voltage(x, eta, rs, eye0, T), hor_data, vert_data)

    #print "Fit parameters =",popt
    #print "Fit covariance =",pcov
    #print "eta, rs, I_{0} =", popt[0], -1000*popt[1], 1.0/popt[2]
    #print "eta, rs, I_{0} =", popt[0], popt[1], 1.0/popt[2]

    for i in range(0,len(params),1):
        if i == 1:
            print(params[i]," =",-1000.0*popt[i]," +/-",1000.0*math.sqrt( abs( pcov[i][i] ) ) )
        else:
            print(params[i]," =",popt[i]," +/-",math.sqrt( abs( pcov[i][i] ) ) )
    print(" ")

    return popt

def estimate_PhC_capacitance():
    # use the RC model to estimate the PhC capacitance
    # R. Sheehan 16 - 1 - 2019

    FUNC_NAME = ".estimate_PhC_capacitance()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        fr_file = "Swp_FR_MHz.txt"
        resp_file_1 = "Vin_BNC_Vpp_03.txt"        
        resp_file_11 = "Vout_HSPD_Vpp_03.txt"

        if glob.glob(fr_file) and glob.glob(resp_file_1) and glob.glob(resp_file_11):
            fr_data = Common.read_data(fr_file)
            resp_data_1 = Common.read_data(resp_file_1)
            resp_data_11 = Common.read_data(resp_file_11)
            
            if fr_data is not None and resp_data_1 is not None and resp_data_11 is not None:

                fr_data = Common.scale_data(np.asarray(fr_data), 1.0e+3)

                # compute the electrical reponse of the device
                cval = 1.7e-4; rval = 70; 
                resp_03 = []; actual_fit_data = []; actual_response_data = []
                ref_level_03 = resp_data_11[0] / resp_data_1[0]; 
                for i in range(0, len(resp_data_1), 1):
                    response = resp_data_11[i] / resp_data_1[i]
                    actual_response_data.append(response)
                    response = freq_response_RC(fr_data[i], 1.0, cval, rval)
                    resp_03.append( response )
                    actual_fit_data.append(1.0/response**2)

                # estimate the capacitance from the response data
                R = 131; 
                popt = freq_response_fit(fr_data, resp_03)

                print("Model RC:",cval*rval)
                print("RC:",math.sqrt(popt[1])/(2.0*math.pi))
                print("C:",math.sqrt(popt[1])/(2.0*math.pi)/rval)

                fit_data = []
                for i in range(0, len(fr_data), 1):
                    term = popt[0] + popt[1]*fr_data[i]**2
                    fit_data.append(1.0 / math.sqrt(term))
                    #fit_data.append(term)

                # plot the fit for good measure
                hv_data = []; marks = []; labels = []

                fr_data = Common.scale_data(fr_data, 1.0e-3)

                hv_data.append([fr_data, resp_03]); marks.append(Plotting.labs_pts[0]); labels.append('Data')
                hv_data.append([fr_data, actual_response_data]); marks.append(Plotting.labs_pts[2]); labels.append('Real Data')
                #hv_data.append([fr_data, actual_fit_data]); marks.append(Plotting.labs_pts[3]); labels.append('Actual Fit Data')
                hv_data.append([fr_data, fit_data]); marks.append(Plotting.labs_lins[1]); labels.append('Model')                

                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.x_label = 'Frequency (MHz)'
                args.y_label = 'Response'
                args.fig_name = 'PhC_Response'
                args.crv_lab_list = labels
                args.mrk_list = marks
                #args.fig_name = 'Response_Model_Fit'

                Plotting.plot_multiple_curves(hv_data, args)
                
                del fr_data; del resp_data_1;       
            else:
                raise Exception
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def freq_response_RC(x, aval, cval, rval):
    # return the frequency response of an RC circuit
    # it is assumed that the frequency value is input in units of MHz
    # really aval == 1.0
    # R. Sheehan 16 - 1 - 2019

    #fval = 1.0e+6 * x
    term = 2.0 * math.pi * x * rval * cval
    denom = math.sqrt( aval + (term*term) )

    return (1.0 / denom)

def freq_response_RC_fit_func(x, a, b):
    # try fitting to this function instead
    # you're actually fitting to the inverse of the square of the reponse data
    # this is a quadratic of the form a + b x^2 where a = 1 and b = (2 pi R C)^2

    return (a + ( b * x * x) )

def freq_response_fit(hor_data, vert_data):
    # make a fit to the freq response data
    # R. Sheehan 16 - 1 - 2019

    try:
        from scipy.optimize import curve_fit
        
        params = ['A', 'B']
        fit_data = []
        for i in range(0, len(vert_data), 1):
            fit_data.append( 1.0 / (vert_data[i]**2) )
        popt, pcov = scipy.optimize.curve_fit(freq_response_RC_fit_func, hor_data, fit_data)

        for i in range(0,len(params),1):
            print(params[i]," =",popt[i]," +/-",math.sqrt( abs( pcov[i][i] ) ) )
        print(" ")

        return popt
    except Exception:
        print("An error occurred")

def WL_Repeatibility():

    FUNC_NAME = ".WL_Repeatibility()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        mode_num = np.arange(1,5,1)
        mode_wl = [1540.24, 1546.67, 1552.63, 1557.82]
        mode_dwl = [2.49, 2.53, 2.49, 1.51]
        mode_stdev = [1.46, 1.50, 1.43, 1.18]

        args = Plotting.plot_arg_single()

        args.loud = True
        args.marker = Plotting.labs_pts[1]
        args.plt_range = [0.5,3.5, 1534, 1558]
        args.x_label = "Mode Number"
        args.y_label = "PhC Resonance Wavelength (nm)"
        args.fig_name = 'WL_Repeatibility'

        Plotting.plot_single_curve_with_errors(mode_num, mode_wl, mode_dwl, args)
        
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def PhC_Transmission():

    FUNC_NAME = ".PhC_Transmission()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "C:/Users/Robert/Research/Publications/PhC_Laser_cavity_Length/"

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)

            print(os.getcwd())

            filename = 'Normalised_data_Device_4_T.dat'

            if glob.glob(filename):
                data = np.loadtxt(filename, unpack = True)

                Tmax = np.max(data[1])

                data[1] = data[1] / Tmax

                args = Plotting.plot_arg_single()

                args.loud = True
                args.marker = Plotting.labs_lins[0]
                args.plt_range = [1535, 1555, 0, 1]
                args.x_label = "wavelength (nm)"
                args.y_label = "PhC Transmission (a. u. )"
                args.fig_name = 'PhC_transmission'

                Plotting.plot_single_curve(data[0], data[1], args)
            else:
                raise Exception
        else:
            raise Exception        
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
