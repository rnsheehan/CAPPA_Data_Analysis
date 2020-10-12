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
            print os.getcwd()

            #plot_RI_versus_WL()

            #Wh=2000; Nl=20; 
            #plot_reflectivity_versus_WL_layers(Wh)
            #Wh_list = range(500, 2500, 500)   
            #Nl_list = range(5, 25, 5)
            #for Nl in Nl_list:         
            #for Wh in Wh_list: 
            #    #plot_neff_versus_WL(Wh)
            #    #plot_period_versus_WL(Wh)
            #    plot_reflectivity_versus_WL_layers(Wh)

            #plot_reflectivity_versus_width_ratio('Ex')

            #plot_device_dims_versus_width_ratio('Ey')

            #plot_index_contrast_versus_width_ratio()

            plot_layer_lengths_versus_width_ratio()

        else:
            raise EnvironmentError
    except EnvironmentError:
        print ERR_STATEMENT
        print "Cannot find",DATA_HOME
    except Exception:
        print ERR_STATEMENT

def read_DBR_data_file(Wl, Wh, Polar, Nlayers):

    # read a file containing DBR simulation data
    # data is contained in files of the form "DBR_params_Wl_*_Wh_*_Pol_*_Nl_*.txt"
    # Wl is the lower waveguide width expressed in nm
    # Wh is the higher waveguide width expressed in nm
    # Polar is either Ex or Ey
    # Nlayers is the assumed number of layers
    
    # contents of the file are as follows
    # col[0] = wavelength (nm)
    # col[1] = core refractive index (RI)
    # col[2] = substrate RI, cladding is assumed to be air
    # col[3] = effective RI in waveguide with width W1
    # col[4] = layer length of waveguide with width W1 units (nm)
    # col[5] = effective RI in waveguide with width W2
    # col[6] = layer length of waveguide with width W2 units (nm)
    # col[7] = period of grating formed from waveguides with width W1 and W2 units (nm)
    # col[8] = total length of grating structure formed from waveguides with width W1 and W2 units (um)
    # col[9] = reflectivity of grating structure formed from waveguides with width W1 and W2 units (um)

    # R. Sheehan 3 - 4 - 2018

    FUNC_NAME = ".read_DBR_data_file()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        filename = "DBR_params_Wl_%(v1)d_Wh_%(v2)d_Pol_%(v3)s_Nl_%(v4)d.txt"%{"v1":Wl, "v2":Wh, "v3":Polar, "v4":Nlayers}

        if glob.glob(filename):
            data = Common.read_matrix(filename, '\t', True)
            data = Common.transpose_multi_col(data)
            return data
        else:
            raise Exception
    except Exception:
        print ERR_STATEMENT

def plot_RI_versus_WL():
    # make a plot of RI versus wavelength
    # R. Sheehan 3 - 4 - 2018

    FUNC_NAME = ".plot_RI_versus_WL()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        Wl = 250; Wh = 1000; pol = 'Ex'; Nl = 15; 
        data = read_DBR_data_file(Wl, Wh, pol, Nl)

        if data is not None:            
            hv_data = []; labels = []; mark_list = []
            hv_data.append([data[0], data[1]]); hv_data.append([data[0], data[2]]); 
            labels.append('$n_{core}$ Si'); labels.append('$n_{sub}$ SiO$_{2}$');
            mark_list.append(Plotting.labs[0]); mark_list.append(Plotting.labs[1]); 

            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.x_label = "Wavelength (nm)"
            args.y_label = "Refractive Index"
            args.mrk_list = mark_list
            args.crv_lab_list = labels
            args.plt_range = [1500, 1660, 1.0, 4.0]
            args.fig_name = 'RI_Dispersion_Si_SiO2'

            Plotting.plot_multiple_curves(hv_data, args)

            del data; del hv_data; del labels; del mark_list; del args; 
        else:
            raise Exception
    except Exception:
        print ERR_STATEMENT

def plot_neff_versus_WL(Wh):
    # make a plot of a quantity versus wavelength
    # R. Sheehan 3 - 4 - 2018

    FUNC_NAME = ".plot_neff_versus_WL()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        Wl = 250; pol1 = 'Ex'; pol2 = 'Ey'; Nl = 15; 
        data1 = read_DBR_data_file(Wl, Wh, pol1, Nl)
        data2 = read_DBR_data_file(Wl, Wh, pol2, Nl)

        if data1 is not None and data2 is not None:            
            hv_data = []; labels = []; mark_list = []           

            hv_data.append([data2[0], data2[3]]); hv_data.append([data2[0], data2[5]]); 
            labels.append('$E_{y}$  Wl'); labels.append('$E_{y}$ Wh');
            mark_list.append(Plotting.labs[0]); mark_list.append(Plotting.labs[1]);

            hv_data.append([data1[0], data1[3]]); hv_data.append([data1[0], data1[5]]); 
            labels.append('$E_{x}$ Wl'); labels.append('$E_{x}$ Wh');
            mark_list.append(Plotting.labs_dashed[0]); mark_list.append(Plotting.labs_dashed[1]);                         

            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.x_label = 'Wavelength (nm)'
            args.y_label = 'Effective Refractive Index $n_{eff}$'
            args.mrk_list = mark_list
            args.crv_lab_list = labels
            args.plt_range = [1500, 1660, 1.4, 3.0]
            args.fig_name = 'Neff_Dispersion_Si_SiO2_Wh_%(v1)d'%{"v1":Wh}

            Plotting.plot_multiple_curves(hv_data, args)

            del data1; del data2; del hv_data; del labels; del mark_list; del args;

    except Exception:
        print ERR_STATEMENT

def plot_period_versus_WL(Wh):
    # make a plot of a quantity versus wavelength
    # R. Sheehan 3 - 4 - 2018

    FUNC_NAME = ".plot_period_versus_WL()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        Wl = 250; pol1 = 'Ex'; pol2 = 'Ey'; Nl = 15; 
        data1 = read_DBR_data_file(Wl, Wh, pol1, Nl)
        data2 = read_DBR_data_file(Wl, Wh, pol2, Nl)

        if data1 is not None and data2 is not None:            
            hv_data = []; labels = []; mark_list = []           

            hv_data.append([data2[0], data2[4]]); hv_data.append([data2[0], data2[6]]); hv_data.append([data2[0], data2[7]]); 
            labels.append('$E_{y}$  $L_{Wl}$'); labels.append('$E_{y}$ $L_{Wh}$'); labels.append('$E_{y}$ $\Lambda$');
            mark_list.append(Plotting.labs[0]); mark_list.append(Plotting.labs[1]); mark_list.append(Plotting.labs[2]);

            hv_data.append([data1[0], data1[4]]); hv_data.append([data1[0], data1[6]]); hv_data.append([data1[0], data1[7]]);
            labels.append('$E_{x}$ $L_{Wl}$'); labels.append('$E_{x}$ $L_{Wh}$'); labels.append('$E_{x}$ $\Lambda$');
            mark_list.append(Plotting.labs_dashed[0]); mark_list.append(Plotting.labs_dashed[1]); mark_list.append(Plotting.labs_dashed[2]);                         

            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.x_label = 'Wavelength (nm)'
            args.y_label = 'Grating Structure Lengths (nm)'
            args.mrk_list = mark_list
            args.crv_lab_list = labels
            args.plt_range = [1500, 1660, 120, 550]
            args.fig_name = 'Grating_Lengths_Dispersion_Si_SiO2_Wh_%(v1)d'%{"v1":Wh}

            Plotting.plot_multiple_curves(hv_data, args)

            del data1; del data2; del hv_data; del labels; del mark_list; del args;

    except Exception:
        print ERR_STATEMENT

def plot_reflectivity_versus_WL(Wh, Nl):
    # make a plot of a quantity versus wavelength
    # R. Sheehan 3 - 4 - 2018

    FUNC_NAME = ".plot_reflectivity_versus_WL()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        Wl = 250; pol1 = 'Ex'; pol2 = 'Ey'; 
        data1 = read_DBR_data_file(Wl, Wh, pol1, Nl)
        data2 = read_DBR_data_file(Wl, Wh, pol2, Nl)

        if data1 is not None and data2 is not None:            
            hv_data = []; labels = []; mark_list = []           

            hv_data.append([data2[0], data2[9]]); 
            labels.append('$E_{y}$'); 
            mark_list.append(Plotting.labs[0]); 

            hv_data.append([data1[0], data1[9]]); 
            labels.append('$E_{x}$'); 
            mark_list.append(Plotting.labs_dashed[0]);                      

            args = Plotting.plot_arg_multiple()

            args.loud = False
            args.x_label = 'Wavelength (nm)'
            args.y_label = 'Grating Reflectivity'
            args.mrk_list = mark_list
            args.crv_lab_list = labels
            args.plt_range = [1500, 1660, 0, 1]
            args.fig_name = 'Reflectivity_Dispersion_Si_SiO2_Wh_%(v1)d_Nl_%(v2)d'%{"v1":Wh,"v2":Nl}

            Plotting.plot_multiple_curves(hv_data, args)

            del data1; del data2; del hv_data; del labels; del mark_list; del args;

    except Exception:
        print ERR_STATEMENT

def plot_reflectivity_versus_WL_layers(Wh):
    # make a plot of a quantity versus wavelength
    # R. Sheehan 3 - 4 - 2018

    FUNC_NAME = ".plot_reflectivity_versus_WL()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        Wl = 250; pol1 = 'Ex'; pol2 = 'Ey'; 
        
        Nl = 5
        data1 = read_DBR_data_file(Wl, Wh, pol1, Nl)
        data2 = read_DBR_data_file(Wl, Wh, pol2, Nl)

        Nl = 10
        data1a = read_DBR_data_file(Wl, Wh, pol1, Nl)
        data2a = read_DBR_data_file(Wl, Wh, pol2, Nl)

        Nl = 15
        data1b = read_DBR_data_file(Wl, Wh, pol1, Nl)
        data2b = read_DBR_data_file(Wl, Wh, pol2, Nl)

        Nl = 20
        data1c = read_DBR_data_file(Wl, Wh, pol1, Nl)
        data2c = read_DBR_data_file(Wl, Wh, pol2, Nl)

        if data1 is not None and data2 is not None:            
            hv_data = []; labels = []; mark_list = []           

            # Ey polarisation
            #hv_data.append([data2[0], data2[9]]); hv_data.append([data2a[0], data2a[9]]);  hv_data.append([data2b[0], data2b[9]]); hv_data.append([data2c[0], data2c[9]]); 
            #labels.append('$E_{y}$ $N_{l} = 5$'); labels.append('$E_{y}$ $N_{l} = 10$'); labels.append('$E_{y}$ $N_{l} = 15$'); labels.append('$E_{y}$ $N_{l} = 20$'); 
            #mark_list.append(Plotting.labs[0]); mark_list.append(Plotting.labs[1]); mark_list.append(Plotting.labs[2]); mark_list.append(Plotting.labs[3]); 

            # Ex polarisation
            hv_data.append([data1[0], data1[9]]); hv_data.append([data1a[0], data1a[9]]); hv_data.append([data1b[0], data1b[9]]); hv_data.append([data1c[0], data1c[9]]); 
            labels.append('$E_{x}$ $N_{l} = 5$'); labels.append('$E_{x}$ $N_{l} = 10$'); labels.append('$E_{x}$ $N_{l} = 15$'); labels.append('$E_{x}$ $N_{l} = 20$'); 
            #mark_list.append(Plotting.labs_dashed[0]); mark_list.append(Plotting.labs_dashed[1]); mark_list.append(Plotting.labs_dashed[2]); mark_list.append(Plotting.labs_dashed[3]);                      
            mark_list.append(Plotting.labs[0]); mark_list.append(Plotting.labs[1]); mark_list.append(Plotting.labs[2]); mark_list.append(Plotting.labs[3]); 

            args = Plotting.plot_arg_multiple()

            args.loud = False
            args.x_label = 'Wavelength (nm)'
            args.y_label = 'Grating Reflectivity'
            args.mrk_list = mark_list
            args.crv_lab_list = labels
            args.plt_range = [1500, 1660, 0, 1]
            args.fig_name = 'Ex_Reflectivity_Dispersion_Si_SiO2_Wh_%(v1)d'%{"v1":Wh}

            Plotting.plot_multiple_curves(hv_data, args)

            del data1; del data2; del hv_data; del labels; del mark_list; del args;

    except Exception:
        print ERR_STATEMENT

def plot_reflectivity_versus_width_ratio(pol):
    # make a plot of reflectivity versus waveguide width ratio
    # choose \lambda = 1590 nm
    # R. Sheehan 3 - 4 - 2018

    FUNC_NAME = ".plot_reflectivity_versus_width_ratio()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        Wh_list = range(500, 2500, 500)   
        Nl_list = range(5, 25, 5)

        Wl = 250; 

        # Extract the data from the files
        hv_data = []; labels = []; mark_list = []; count = 0
        for Nl in Nl_list:
            wratio = []; rvals = []
            for Wh in Wh_list:
                wratio.append(Wh/Wl)
                data = read_DBR_data_file(Wl, Wh, pol, Nl)
                rvals.append(data[9][3])
            hv_data.append([wratio, rvals])
            labels.append('$N_{l}$ = %(v1)d'%{"v1":Nl})
            mark_list.append(Plotting.labs[count])
            count = (count+1)%len(Plotting.labs)

        if len(hv_data) > 2:

            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.x_label = "Waveguide Rib Width Ratio $W_{h}/W_{l}$"
            args.y_label = "%(v1)s Reflectivity"%{"v1":pol}
            args.mrk_list = mark_list
            args.crv_lab_list = labels
            args.plt_range = [2, 8, 0, 1]
            args.fig_name = 'Reflectivity_W_Ratio_Pol_%(v1)s'%{"v1":pol}

            Plotting.plot_multiple_curves(hv_data, args)

            del data; del hv_data; del labels; del mark_list; del args; 

        else:
            raise Exception
    except Exception:
        print ERR_STATEMENT

def plot_index_contrast_versus_width_ratio():
    # make a plot of reflectivity versus waveguide width ratio
    # choose \lambda = 1590 nm
    # R. Sheehan 3 - 4 - 2018

    FUNC_NAME = ".plot_index_contrast_versus_width_ratio()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        Wh_list = range(500, 2500, 500)   

        Wl = 250; 

        # Extract the data from the files
        hv_data = []; labels = []; mark_list = []; 
        Nl = 5
        wratio = []; rvals = []
        for Wh in Wh_list:
            wratio.append(Wh/Wl)
            data = read_DBR_data_file(Wl, Wh, 'Ey', Nl)
            rvals.append((data[5][3]**2-data[3][3]**2)/(2.0*data[5][3]**2))
        hv_data.append([wratio, rvals])
        labels.append('$E_{y}$')
        mark_list.append(Plotting.labs[0])

        wratio = []; rvals = []
        for Wh in Wh_list:
            wratio.append(Wh/Wl)
            data = read_DBR_data_file(Wl, Wh, 'Ex', Nl)
            rvals.append((data[5][3]**2-data[3][3]**2)/(2.0*data[5][3]**2))
        hv_data.append([wratio, rvals])
        labels.append('$E_{x}$')
        mark_list.append(Plotting.labs_dashed[0])

        if len(hv_data) > 0:

            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.x_label = "Waveguide Rib Width Ratio $W_{h}/W_{l}$"
            args.y_label = "Index Contrast $\Delta n$"
            args.mrk_list = mark_list
            args.crv_lab_list = labels
            args.plt_range = [2, 8, 0, 0.14]
            args.fig_name = 'Index_Contrast_W_Ratio'

            Plotting.plot_multiple_curves(hv_data, args)

            del data; del hv_data; del labels; del mark_list; del args; 

        else:
            raise Exception
    except Exception:
        print ERR_STATEMENT

def plot_device_dims_versus_width_ratio(pol):
    # make a plot of reflectivity versus waveguide width ratio
    # choose \lambda = 1590 nm
    # R. Sheehan 3 - 4 - 2018

    FUNC_NAME = ".plot_device_dims_versus_width_ratio()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        Wh_list = range(500, 2500, 500)   
        Nl_list = range(5, 25, 5)

        Wl = 250; 

        # Extract the data from the files
        hv_data = []; labels = []; mark_list = []; count = 0
        for Nl in Nl_list:
            wratio = []; rvals = []
            for Wh in Wh_list:
                wratio.append(Wh/Wl)
                data = read_DBR_data_file(Wl, Wh, pol, Nl)
                rvals.append(data[8][3])
            hv_data.append([wratio, rvals])
            labels.append('$N_{l}$ = %(v1)d'%{"v1":Nl})
            mark_list.append(Plotting.labs[count])
            count = (count+1)%len(Plotting.labs)

        if len(hv_data) > 2:

            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.x_label = "Waveguide Rib Width Ratio $W_{h}/W_{l}$"
            args.y_label = "%(v1)s Total Grating Length (um)"%{"v1":pol}
            args.mrk_list = mark_list
            args.crv_lab_list = labels
            args.plt_range = [2, 8, 0, 10]
            args.fig_name = 'Total_Length_W_Ratio_Pol_%(v1)s'%{"v1":pol}

            Plotting.plot_multiple_curves(hv_data, args)

            del data; del hv_data; del labels; del mark_list; del args; 

        else:
            raise Exception
    except Exception:
        print ERR_STATEMENT

def plot_layer_lengths_versus_width_ratio():
    # make a plot of reflectivity versus waveguide width ratio
    # choose \lambda = 1590 nm
    # R. Sheehan 3 - 4 - 2018

    FUNC_NAME = ".plot_layer_lengths_versus_width_ratio()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        Wh_list = range(500, 2500, 500)   

        Wl = 250; 

        # Extract the data from the files
        hv_data = []; labels = []; mark_list = []; 
        Nl = 5
        wratio = []; rvals = []; l1vals = []; l2vals = [];
        for Wh in Wh_list:
            wratio.append(Wh/Wl)
            data = read_DBR_data_file(Wl, Wh, 'Ey', Nl)
            rvals.append(data[7][3]); l1vals.append(data[4][3]);
            l2vals.append(data[6][3]);
        hv_data.append([wratio, rvals]); hv_data.append([wratio, l1vals]); 
        hv_data.append([wratio, l2vals]); 
        labels.append('$E_{y}$'); labels.append('$E_{y}$ $L_{W1}$'); 
        labels.append('$E_{y}$ $L_{W2}$'); 
        mark_list.append(Plotting.labs[0]); mark_list.append(Plotting.labs[1]); 
        mark_list.append(Plotting.labs[2]); 

        wratio = []; rvals = []; l1vals = []; l2vals = [];
        for Wh in Wh_list:
            wratio.append(Wh/Wl)
            data = read_DBR_data_file(Wl, Wh, 'Ex', Nl)
            rvals.append(data[7][3]); l1vals.append(data[4][3]);
            l2vals.append(data[6][3]);
        hv_data.append([wratio, rvals]); hv_data.append([wratio, l1vals]); 
        hv_data.append([wratio, l2vals]); 
        labels.append('$E_{x}$'); labels.append('$E_{x}$ $L_{W1}$'); 
        labels.append('$E_{x}$ $L_{W2}$'); 
        mark_list.append(Plotting.labs_dashed[0]); mark_list.append(Plotting.labs_dashed[1]); 
        mark_list.append(Plotting.labs_dashed[2]);

        if len(hv_data) > 0:

            args = Plotting.plot_arg_multiple()

            args.loud = True
            args.x_label = "Waveguide Rib Width Ratio $W_{h}/W_{l}$"
            args.y_label = "Grating Period $\Lambda$ (nm)"
            args.mrk_list = mark_list
            args.crv_lab_list = labels
            args.plt_range = [2, 8, 100, 500]
            args.fig_name = 'Grating_Period_W_Ratio'

            Plotting.plot_multiple_curves(hv_data, args)

            del data; del hv_data; del labels; del mark_list; del args; 

        else:
            raise Exception
    except Exception:
        print ERR_STATEMENT


