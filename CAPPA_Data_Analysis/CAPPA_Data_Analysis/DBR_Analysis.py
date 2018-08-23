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

# Make plots of the results obtained for the design of the DBR grating for the CORNERSTONE fab run April 2018
# See notebook 426, pg 7 for details
# R. Sheehan 3 - 4 - 2018

MOD_NAME_STR = "DBR_Analysis" # use this in exception handling messages

def DBR_Sim_Plots():

    # Run the functions to plot the DBR simulation Data
    # R. Sheehan 3 - 4 - 2018

    FUNC_NAME = ".DBR_Sim_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "C:/Users/Robert/Research/CAPPA/Simulations/DBR_Design_Apr_2018/"

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            Wm = 0.5; Wh = 0.55; Wl = 0.45

            SUB_DIR = "WG_%(v1)0.2f_Wh_%(v2)0.2f_Wl_%(v3)0.2f/"%{"v1":Wm, "v2":Wh, "v3":Wl}

            if os.path.isdir(SUB_DIR):
                os.chdir(SUB_DIR)
                print(os.getcwd())

                polar = 'Ey'
                Ldbr = 50
                dbr_type = 1

                data = read_DBR_data_file(Wm, Wh, Wl, polar, dbr_type, Ldbr)
                
                period = 1; BW = 3; Rpeak = 4

                #plot_qty_versus_WL_Bragg(data, period, Ldbr)
                #plot_qty_versus_WL_Bragg(data, BW, Ldbr)
                #plot_qty_versus_WL_Bragg(data, Rpeak, Ldbr)                

                WLbrg = 1570
                Ldbr = 100
                #plot_reflectivity_data(Wm, Wh, Wl, polar, WLbrg, Ldbr)
                #compute_FWHM(Wm, Wh, Wl, polar, WLbrg, Ldbr)

                Ldbr_list = [30, 40, 50, 70, 100]
                WLbrg_list = [1530, 1555, 1570, 1595, 1610, 1630]
                #for j in range(0, len(Ldbr_list), 1):
                #    get_FWHM_multiple_WLbragg(Wm, Wh, Wl, polar, WLbrg_list, Ldbr_list[j])

                #plot_multiple_FWHM(WLbrg_list, Ldbr_list)
                
                #plot_multiple_reflectivity_data(Wm, Wh, Wl, polar, WLbrg, Ldbr)

                #plot_multiple_qty_versus_WL_Bragg(Wm, Wh, Wl, polar, dbr_type, BW, Ldbr)

                plot_multiple_qty_versus_WL_Bragg(Wm, Wh, Wl, polar, dbr_type, period, Ldbr_list)

                #plot_multiple_qty_versus_WL_Bragg(Wm, Wh, Wl, polar, dbr_type, Rpeak, Ldbr)

            else:
                raise EnvironmentError
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot find",DATA_HOME)
    except Exception:
        print(ERR_STATEMENT)

def read_DBR_data_file(Wm, Wh, Wl, Polar, Type, Ldbr):
    # read a file containing DBR simulation data
    # Wm is the width of the main waveguide
    # Wl is the lower waveguide width expressed in nm
    # Wh is the higher waveguide width expressed in nm
    # Polar is either Ex or Ey
    # Type determines the corrugation on the rib
    # Ldbr is the length of the DBR section
        
    # contents of the file are as follows
    # col[0] = Bragg wavelength (nm)
    # col[1] = Period (nm)
    # col[2] = LDBR (um)
    # col[3] = BW (nm)
    # col[4] = Rpeak

    # R. Sheehan 5 - 4 - 2018

    FUNC_NAME = ".read_DBR_data_file()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        filename = "DBR_Vals_W_%(v1)0.2f_Wh_%(v2)0.2f_Wl_%(v3)0.2f_%(v4)s_Type_%(v5)d_LDBR_%(v6)d.txt"%{"v1":Wm, "v2":Wh, "v3":Wl, "v4":Polar, "v5":Type, "v6":Ldbr}

        if glob.glob(filename):
            data = Common.read_matrix(filename, '\t', True)
            data = Common.transpose_multi_col(data)
            return data
        else:
            return None
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def plot_qty_versus_WL_Bragg(bragg_data, qty, Ldbr):
    # plot the computed DBR parameter and plot it for different Bragg WL
    # qty = 1 => DBR period (nm)
    # qty = 3 => DBR BW (nm)
    # qty = 4 => DBR Rpeak

    FUNC_NAME = ".plot_qty_versus_WL_Bragg()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if qty == 1 or qty == 3 or qty == 4:
            args = Plotting.plot_arg_single()

            args.x_label = 'Bragg Wavelength (nm)'
            args.loud = True

            if qty == 1:
                args.y_label = 'DBR Period $\Lambda$ (nm)'
                args.plt_range = [1520, 1640, 290, 325]
            elif qty == 3:
                args.y_label = 'DBR BW (nm)'
                args.plt_range = [1500, 1650, 5, 70]
            elif qty == 4:
                args.y_label = 'DBR $R_{peak}$'
                args.plt_range = [1500, 1650, 0, 1]
            else:
                raise Exception

            Plotting.plot_single_curve(bragg_data[0], bragg_data[qty], args)

        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def plot_qty_versus_WL_Bragg(bragg_data, qty, Ldbr):
    # plot the computed DBR parameter and plot it for different Bragg WL
    # qty = 1 => DBR period (nm)
    # qty = 3 => DBR BW (nm)
    # qty = 4 => DBR Rpeak

    FUNC_NAME = ".plot_qty_versus_WL_Bragg()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if qty == 1 or qty == 3 or qty == 4:
            args = Plotting.plot_arg_single()

            args.x_label = 'Bragg Wavelength (nm)'
            args.loud = True

            if qty == 1:
                args.y_label = 'DBR Period $\Lambda$ (nm)'
                args.plt_range = [1520, 1640, 290, 325]
            elif qty == 3:
                args.y_label = 'DBR BW (nm)'
                args.plt_range = [1500, 1650, 5, 70]
            elif qty == 4:
                args.y_label = 'DBR $R_{peak}$'
                args.plt_range = [1500, 1650, 0, 1]
            else:
                raise Exception

            Plotting.plot_single_curve(bragg_data[0], bragg_data[qty], args)

        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def plot_multiple_qty_versus_WL_Bragg(Wm, Wh, Wl, Polar, Type, qty, Ldbr):
    # plot the computed DBR parameter and plot it for different Bragg WL for multiple DBR lengths
    # qty = 1 => DBR period (nm)
    # qty = 3 => DBR BW (nm)
    # qty = 4 => DBR Rpeak

    FUNC_NAME = ".plot_qty_versus_WL_Bragg()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:

        if qty == 1 or qty == 3 or qty == 4:
            hv_data = []; labels = []; marks = []
            
            for i in range(0, len(Ldbr), 1):
                
                data = read_DBR_data_file(Wm, Wh, Wl, Polar, Type, Ldbr[i])
                
                if qty == 1:
                    for j in range(0, len(data[1]), 1): 
                        data[1][j] = 2.0*data[1][j]
                
                if data is not None:
                    hv_data.append( [ data[0], data[qty] ] )
                    marks.append(Plotting.labs[i%len(Plotting.labs)])
                    labels.append('L = %(v1)d ($\mu$m)'%{"v1":Ldbr[i]})

            if len(hv_data) > 2:
                args = Plotting.plot_arg_multiple()

                args.x_label = 'Bragg Wavelength (nm)'
                args.loud = True
                args.crv_lab_list = labels
                args.mrk_list = marks

                if qty == 1:
                    args.y_label = 'DBR Period $\Lambda$ (nm)'
                    #args.plt_range = [1520, 1640, 2*290, 2*325]
                    args.plt_range = [1520, 1640, 2*290, 2*325]
                    args.fig_name = 'DBR_Period'
                elif qty == 3:
                    args.y_label = 'DBR BW (nm)'
                    args.plt_range = [1500, 1650, 0, 35]
                    args.fig_name = 'DBR_BW'
                elif qty == 4:
                    args.y_label = 'DBR $R_{peak}$'
                    args.plt_range = [1500, 1650, 0, 1]
                    args.fig_name = 'DBR_RPeak'
                else:
                    raise Exception

                Plotting.plot_multiple_curves(hv_data, args)
            else:
                raise Exception
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def plot_reflectivity_data(Wm, Wh, Wl, Polar, WLbragg, Ldbr):

    # plot the reflectivity for single LDBR and single WL-Bragg
    # R. Sheehan 5 - 4 - 2018

    FUNC_NAME = ".plot_reflectivity_data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # gather WL and reflectivity data
        wl_file = "WL_data_W_%(v1)0.2f_Ey.txt"%{"v1":Wm}
        ref_file = "reflectivity_data_W_%(v1)0.2f_Wh_%(v2)0.2f_Wl_%(v3)0.2f_%(v4)s_BWL_%(v5)d_LDBR_%(v6)d.txt"%{"v1":Wm, "v2":Wh, "v3":Wl, "v4":Polar, "v5":WLbragg, "v6":Ldbr}

        # if data is found plot it
        if glob.glob(wl_file) and glob.glob(ref_file):
            wl_data = Common.read_data(wl_file)
            ref_file = Common.read_data(ref_file)

            args = Plotting.plot_arg_single()

            args.loud = True
            args.x_label = 'Wavelength (nm)'
            args.y_label = 'Reflectivity $|r|^{2}$'
            args.plt_range = [1500, 1650, 0, 1]
            args.marker = 'r-'

            Plotting.plot_single_curve(wl_data, ref_file, args)
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def plot_multiple_reflectivity_data(Wm, Wh, Wl, Polar, WLbragg, Ldbr):

    # plot the reflectivity for multiple LDBR and single WL-Bragg
    # R. Sheehan 5 - 4 - 2018

    FUNC_NAME = ".plot_multiple_reflectivity_data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        wl_file = "WL_data_W_%(v1)0.2f_Ey.txt"%{"v1":Wm}

        if glob.glob(wl_file):

            # read WL data
            wl_data = Common.read_data(wl_file)

            # Gather reflectivity data at multiple lengths for single Bragg wavelength
            hv_data = []; labels = []; marks = []; 
            for i in range(0, len(Ldbr), 1):
                ref_file = "reflectivity_data_W_%(v1)0.2f_Wh_%(v2)0.2f_Wl_%(v3)0.2f_%(v4)s_BWL_%(v5)d_LDBR_%(v6)d.txt"%{"v1":Wm, "v2":Wh, "v3":Wl, "v4":Polar, "v5":WLbragg, "v6":Ldbr[i]}
                if glob.glob(ref_file):
                    ref_data = Common.read_data(ref_file)
                    hv_data.append([wl_data, ref_data]); 
                    marks.append(Plotting.labs_lins[i%len(Plotting.labs_lins)])
                    labels.append('L = %(v1)d ($\mu$m)'%{"v1":Ldbr[i]})
                    del ref_data

            # if data is found plot it
            if len(hv_data) > 2:
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.x_label = 'Wavelength (nm)'
                args.y_label = 'Reflectivity $|r|^{2}$'
                args.plt_range = [1500, 1650, 0, 1]
                args.mrk_list = marks
                args.crv_lab_list = labels
                args.fig_name = 'DBR_Reflectivity_Bragg_WL_%(v1)d'%{"v1":WLbragg}

                Plotting.plot_multiple_curves(hv_data, args)

                del hv_data; del labels; del marks;
            else:
                raise Exception 
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def compute_FWHM(Wm, Wh, Wl, Polar, WLbragg, Ldbr):
    # given a DBR reflectivity spectrum compute the 3dB BW which is actually the FWHM
    # R. Sheehan 6 - 4 - 2018

    FUNC_NAME = ".compute_FWHM()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # gather WL and reflectivity data
        wl_file = "WL_data_W_%(v1)0.2f_Ey.txt"%{"v1":Wm}
        ref_file = "reflectivity_data_W_%(v1)0.2f_Wh_%(v2)0.2f_Wl_%(v3)0.2f_%(v4)s_BWL_%(v5)d_LDBR_%(v6)d.txt"%{"v1":Wm, "v2":Wh, "v3":Wl, "v4":Polar, "v5":WLbragg, "v6":Ldbr}
        if glob.glob(wl_file) and glob.glob(ref_file):
            wl_data = Common.read_data(wl_file)
            ref_data = Common.read_data(ref_file)

            # find max ref value and corresponding wavelength
            rpeak, rpeak_indx = Common.index_max_val_numpy(ref_data)

            half_max = 0.5*rpeak

            #print(rpeak
            #print(ref_data[rpeak_indx]
            #print(wl_data[rpeak_indx]
            
            # search ref_data to find element closest to rpeak/2
            nearest_indx = 0; nearest_val = 0.0
            min_delta = 100
            for i in range(0, len(ref_data), 1):
                delta = math.fabs(ref_data[i]-half_max)
                if delta < min_delta:
                    min_delta = delta
                    nearest_indx = i
                    nearest_val = ref_data[i] 

            FWHM = 2.0*math.fabs(wl_data[rpeak_indx]-wl_data[nearest_indx])
            
            #print(nearest_indx
            #print(wl_data[nearest_indx]
            #print(half_max
            #print(nearest_val            
            #print(ref_data[nearest_indx]
            #print(FWHM

            return FWHM
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def get_FWHM_multiple_WLbragg(Wm, Wh, Wl, Polar, WLbragg, Ldbr):
    # compute the FWHM for multiple Bragg wavelengths at fixed length
    # R. Sheehan 6 - 4 - 2018

    FUNC_NAME = ".get_FWHM_multiple_WLbragg()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if len(WLbragg) > 0:
            FWHM_data = []
            for i in range(0, len(WLbragg), 1):
                FWHM = compute_FWHM(Wm, Wh, Wl, Polar, WLbragg[i], Ldbr)
                if FWHM > 0.0:
                    FWHM_data.append(FWHM)
            if len(FWHM_data) > 0:
                
                filename = 'FWHM_data_Ldbr_%(v2)d.txt'%{"v2":Ldbr}
                Common.write_data(filename, FWHM_data); 

                return FWHM_data
            else:
                return None
                raise Exception
    except Exception:
        print(ERR_STATEMENT)

def plot_multiple_FWHM(WLbragg, Ldbr):
    # plot multiple FWHM curves
    # R. Sheehan 6 - 4 -2018

    FUNC_NAME = ".plot_multiple_FWHM()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if len(Ldbr) > 0 and len(WLbragg)>0:

            hv_data = []; labels = []; marks = []; 

            for i in range(0, len(Ldbr), 1):
                filename = 'FWHM_data_Ldbr_%(v2)d.txt'%{"v2":Ldbr[i]}
                if glob.glob(filename):
                    FWHM_data = Common.read_data(filename)
                    hv_data.append([WLbragg, FWHM_data]); 
                    marks.append(Plotting.labs[i%len(Plotting.labs)])
                    labels.append('L = %(v1)d ($\mu$m)'%{"v1":Ldbr[i]})

            if len(hv_data) > 0:
                args = Plotting.plot_arg_multiple()

                args.loud = True
                args.x_label = 'Bragg Wavelength (nm)'
                args.y_label = 'DBR FWHM (nm)'

                args.crv_lab_list = labels
                args.mrk_list = marks
                
                args.plt_range = [1500, 1650, 0, 15]
                args.fig_name = 'DBR_FWHM'

                Plotting.plot_multiple_curves(hv_data, args)
            else:
                raise Exception
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)