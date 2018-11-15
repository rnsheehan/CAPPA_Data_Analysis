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

# Plot the data associated with the design of the Redfinch AWG
# R. Sheehan 13 - 11 - 2018

MOD_NAME_STR = "Redfinch_AWG" # use this in exception handling messages

def Make_AWG_Plots():
    
    FUNC_NAME = ".Make_AWG_Plots()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = "C:/Users/Robert/Research/CAPPA/Simulations/Redfinch_AWG/"

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            Plot_Coupling_Coefficients()

            #wg_type = 'Rib'
            #setnum = 1
            #include_mat_ri = False
            #Plot_Dispersion_Curves(wg_type, setnum, include_mat_ri)

            #wg_type = 'Rib'
            #setnum = 2
            #include_mat_ri = False
            #Plot_Dispersion_Curves(wg_type, setnum, include_mat_ri)

            #wg_type = 'Slab'
            #setnum = 1
            #include_mat_ri = False
            #Plot_Dispersion_Curves(wg_type, setnum, include_mat_ri)

            #wg_type = 'Slab'
            #setnum = 2
            #include_mat_ri = False
            #Plot_Dispersion_Curves(wg_type, setnum, include_mat_ri)

        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT)
        print("Cannot find",DATA_HOME)
    except Exception:
        print(ERR_STATEMENT)

def Plot_Dispersion_Curves(wg_type, setnum, include_mat_ri):
    # Plot the computed Rib, Slab Dispersion Data
    # R. Sheehan 13 - 11 - 2018

    FUNC_NAME = ".Plot_Dispersion_Curves()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if setnum == 1 or setnum == 2:
            wl_file = "Wavelengths_Set_%(v1)d.txt"%{"v1":setnum} # wavelength data for a set
            sige_ri = "SiGe_RI_Set_%(v1)d.txt"%{"v1":setnum} # SiGe RI data for a set
            sin_ri = "SiN_RI_Set_%(v1)d.txt"%{"v1":setnum} # SiN RI data for a set
            rib_te_neff = "Rib_Neff_TE_Set_%(v1)d.txt"%{"v1":setnum} if wg_type == "Rib" else "Slab_W_27_Neff_TE_Set_%(v1)d.txt"%{"v1":setnum}
            rib_tm_neff = "Rib_Neff_TM_Set_%(v1)d.txt"%{"v1":setnum} if wg_type == "Rib" else "Slab_W_27_Neff_TM_Set_%(v1)d.txt"%{"v1":setnum}

            c1 = True if glob.glob(wl_file) else False
            c2 = True if glob.glob(sige_ri)  else False
            c3 = True if glob.glob(sin_ri)  else False
            c4 = True if glob.glob(rib_te_neff) else False
            c5 = True if glob.glob(rib_tm_neff) else False

            if c1 and c2 and c3 and c4 and c5:
                wl_dat = Common.read_data(wl_file)
                sige_ri_dat = Common.read_data(sige_ri)
                sin_ri_dat = Common.read_data(sin_ri)
                rib_te_neff_dat = Common.read_data(rib_te_neff)
                rib_tm_neff_dat = Common.read_data(rib_tm_neff)

                c1 = True if len(wl_dat) == len(sige_ri_dat) else False
                c2 = True if len(wl_dat) == len(sin_ri_dat) else False
                c3 = True if len(wl_dat) == len(rib_te_neff_dat) else False
                c4 = True if len(wl_dat) == len(rib_tm_neff_dat) else False

                if c1 and c2:
                    # plot the imported data
                    hv_data = []; labels = []; marks = []
                    
                    if include_mat_ri:
                        hv_data.append([wl_dat,sige_ri_dat]); labels.append("$n_{SiGe}$"); marks.append(Plotting.labs[0]); 
                    
                    hv_data.append([wl_dat,rib_te_neff_dat]); labels.append("$n_{TE}$"); marks.append(Plotting.labs[2]); 
                    hv_data.append([wl_dat,rib_tm_neff_dat]); labels.append("$n_{TM}$"); marks.append(Plotting.labs[3]); 
                    
                    if include_mat_ri:
                        hv_data.append([wl_dat,sin_ri_dat]); labels.append("$n_{SiN}$"); marks.append(Plotting.labs[1]); 

                    args = Plotting.plot_arg_multiple()

                    args.crv_lab_list = labels
                    args.mrk_list = marks
                    args.x_label = 'Wavelength $(\mu m)$'
                    args.y_label = 'Refractive Index' if include_mat_ri else 'Effective Index'
                    args.plt_title = '%(v1)s WG Material RI Set %(v2)d'%{"v1":wg_type, "v2":setnum} if include_mat_ri else '%(v1)s WG Set %(v2)d'%{"v1":wg_type, "v2":setnum}
                    args.fig_name = '%(v1)s_WG_Material_RI_Set_%(v2)d'%{"v1":wg_type, "v2":setnum} if include_mat_ri else '%(v1)s_Neff_Set_%(v2)d'%{"v1":wg_type, "v2":setnum}
                    #args.plt_range = [0, 50, 0, 300]
                    args.loud = True

                    Plotting.plot_multiple_curves(hv_data, args)

                    del hv_data; del labels; del marks; 
                else:
                    raise Exception
            else:
                raise Exception            
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)

def Plot_Dispersion_Curves():
    # Plot the computed Rib, Slab Dispersion Data
    # R. Sheehan 13 - 11 - 2018

    FUNC_NAME = ".Plot_Dispersion_Curves()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        wl_file_1 = "Wavelengths_Set_1.txt" # wavelength data for a set
        wl_file_2 = "Wavelengths_Set_2.txt" # wavelength data for a set
        sige_ri_1 = "SiGe_RI_Set_1.txt" # SiGe RI data for a set
        sin_ri_1 = "SiN_RI_Set_1.txt" # SiN RI data for a set
        sige_ri_2 = "SiGe_RI_Set_2.txt" # SiGe RI data for a set
        sin_ri_2 = "SiN_RI_Set_2.txt" # SiN RI data for a set

        c1 = True if glob.glob(wl_file_1) else False
        c11 = True if glob.glob(wl_file_2) else False
        c2 = True if glob.glob(sige_ri_1) else False
        c3 = True if glob.glob(sin_ri_1) else False
        c22 = True if glob.glob(sige_ri_2) else False
        c33 = True if glob.glob(sin_ri_2) else False
            
        if c1 and c2 and c3 and c11 and c22 and c33:
            wl_dat_1 = Common.read_data(wl_file_1)
            wl_dat_2 = Common.read_data(wl_file_2)
            sige_ri_dat_1 = Common.read_data(sige_ri_1)
            sin_ri_dat_1 = Common.read_data(sin_ri_1)
            sige_ri_dat_2 = Common.read_data(sige_ri_2)
            sin_ri_dat_2 = Common.read_data(sin_ri_2)

            c1 = True if len(wl_dat_1) == len(sige_ri_dat_1) else False
            c2 = True if len(wl_dat_1) == len(sin_ri_dat_1) else False
            c11 = True if len(wl_dat_2) == len(sige_ri_dat_2) else False
            c22 = True if len(wl_dat_2) == len(sin_ri_dat_2) else False

            if c1 and c2 and c11 and c22:
                wl_dat = np.concatenate((wl_dat_2, wl_dat_1))
                sige_ri_dat = np.concatenate((sige_ri_dat_2, sige_ri_dat_1))
                sin_ri_dat = np.concatenate((sin_ri_dat_2, sin_ri_dat_1))
                    
                # plot the imported data
                hv_data = []; labels = []; marks = []

                hv_data.append([wl_dat,sige_ri_dat]); labels.append("$n_{SiGe}$"); marks.append(Plotting.labs[0]); 
                hv_data.append([wl_dat,sin_ri_dat]); labels.append("$n_{SiN}$"); marks.append(Plotting.labs[1]); 

                args = Plotting.plot_arg_multiple()

                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Wavelength $(\mu m)$'
                args.y_label = 'Refractive Index'
                args.plt_title = 'WG Material RI'
                args.fig_name = 'WG_Material_RI'
                #args.plt_range = [0, 50, 0, 300]
                args.loud = True

                Plotting.plot_multiple_curves(hv_data, args)

                del hv_data; del labels; del marks; 
            else:
                raise Exception
        else:
            raise Exception            
    except Exception:
        print(ERR_STATEMENT)

def Plot_Coupling_Coefficients():
    # plot the computed coupling coefficients for the REDFINCH Rib Waveguide
    # R. Sheehan 15 - 11 - 2018

    FUNC_NAME = ".Plot_Coupling_Coefficients()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        sep_file = "Rib_Separation.txt"
        kappa1 = "Rib_kappa_TE_Set_1.txt"
        kappa2 = "Rib_kappa_TM_Set_1.txt"

        c1 = True if glob.glob(sep_file) else False
        c2 = True if glob.glob(kappa1) else False
        c3 = True if glob.glob(kappa2) else False

        if c1 and c2 and c3:
            sep_data = Common.read_data(sep_file)
            k1_data = Common.read_data(kappa1)
            k2_data = Common.read_data(kappa2)

            c1 = True if len(sep_data) == len(k1_data) else False
            c2 = True if len(sep_data) == len(k2_data) else False

            if c1 and c2:
                # plot the imported data
                hv_data = []; labels = []; marks = []

                hv_data.append([sep_data,k1_data]); labels.append("$\kappa_{TE}$"); marks.append(Plotting.labs[0]); 
                hv_data.append([sep_data,k2_data]); labels.append("$\kappa_{TM}$"); marks.append(Plotting.labs[1]); 

                args = Plotting.plot_arg_multiple()

                args.crv_lab_list = labels
                args.mrk_list = marks
                args.x_label = 'Waveguide Separation $(\mu m)$'
                args.y_label = 'Coupling Coefficient $(\mu m)^{-1}$'
                args.fig_name = 'WG_Coupling'
                #args.plt_range = [0, 50, 0, 300]
                args.loud = True

                Plotting.plot_multiple_curves(hv_data, args)

                del hv_data; del labels; del marks; 
            else:
                raise Exception
        else:
            raise Exception
    except Exception:
        print(ERR_STATEMENT)