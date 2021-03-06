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

MOD_NAME_STR = "COSMICC_Data" # use this in exception handling messages

def Nanostick_Spectrum(num, normalise = False, loud = False):

    # plot the measured transmission spectra for Simone's Nanostick devices
    # R. Sheehan 2 - 7 - 2019

    FUNC_NAME = ".Nanostick_Spectrum()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/COSMICC/Nanosticks/June_2019/Passive_Results/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            filename = 'd1_3%(v1)d_.dat'%{"v1":num}

            if glob.glob(filename):
                print(filename,"exists")

                data = np.loadtxt(filename, unpack = True)

                if data is not None:

                    # normalise the data so that max value is unity
                    if normalise:
                        
                        scal_fac = -1.0*np.min(data[1])

                        if loud: print("Scale_factor:",scal_fac)

                        for i in range(0, len(data[1]),1):
                            data[1][i] = 1.0+(data[1][i] / scal_fac)

                    # plot the data in the file
                    arguments = Plotting.plot_arg_single()
                    arguments.y_label = 'Power (dBm)' if normalise == False else 'Transmission (a.u.)'
                    arguments.x_label = 'Wavelength (nm)'
                    arguments.marker = 'r-'
                    #arguments.plt_range = [1520, 1540, -76, -46]
                    arguments.plt_range = [1520, 1540, 0, 0.4]
                    arguments.loud = loud
                    #arguments.fig_name = filename.replace('.dat','')

                    Plotting.plot_single_curve(data[0], data[1], arguments)

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
        print(ERR_STATEMENT);
        print(e);

def Nanostick_Spectra(normalise = False, loud = False):

    # plot the measured transmission spectra for Simone's Nanostick devices
    # R. Sheehan 2 - 7 - 2019

    FUNC_NAME = ".Nanostick_Spectra()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/COSMICC/Nanosticks/June_2019/Passive_Results/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            numlst = [0, 1, 2]
            sep_list = [50, 150, 250]
            hv_data = []; mrk_lst = []; lab_lst = []
            for i in range(0, len(numlst), 1):
                filename = 'd1_3%(v1)d_.dat'%{"v1":numlst[i]}

                if glob.glob(filename):
                    print(filename,"exists")
                    data = np.loadtxt(filename, unpack = True)
                    if normalise:
                        scal_fac = -1.0*np.min(data[1])
                        for j in range(0, len(data[1]), 1):
                            data[1][j] = 1.0+(data[1][j] / scal_fac)
                    hv_data.append(data); 
                    mrk_lst.append(Plotting.labs_lins[i%len(Plotting.labs_lins)]); 
                    #lab_lst.append(filename.replace('.dat',''))
                    lab_lst.append("D = %(v1)d nm"%{"v1":sep_list[i]})

            if hv_data is not None:
                # plot the data in the file
                arguments = Plotting.plot_arg_multiple()

                arguments.y_label = 'Power (dBm)' if normalise == False else 'Transmission (a.u.)'
                arguments.x_label = 'Wavelength (nm)'
                arguments.mrk_list = mrk_lst
                arguments.crv_lab_list = lab_lst
                if normalise:
                    arguments.plt_range = [1520, 1540, 0.0, 0.4]
                else:
                    #arguments.plt_range = [1520, 1526, -76, -56]
                    arguments.plt_range = [1520, 1540, -76, -46]
                arguments.loud = loud
                arguments.fig_name = 'Combined_Nanostick_Spectra'

                Plotting.plot_multiple_curves(hv_data, arguments)

                del data
                
            else:
                raise Exception
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT);
        print(e);

def Nanostick_Peak_Analysis(num, loud = False):

    # Locate the spectral peaks and their FWHM
    # Compute the mode Q-factor from this data Q = \Delta lambda / \lambda
    # R. Sheehan 2 - 7 - 2019

    FUNC_NAME = ".Nanostick_Spectrum()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/COSMICC/Nanosticks/June_2019/Passive_Results/'

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            filename = 'd1_3%(v1)d_.dat'%{"v1":num}

            if glob.glob(filename):
                print(filename,"exists")

                data = np.loadtxt(filename, unpack = True)

                if data is not None:
                    from scipy.signal import find_peaks, peak_prominences, peak_widths

                    peaks, heights = find_peaks(-1.0*data[1], height = 5)
                    prominences = peak_prominences(-1.0*data[1], peaks)[0] # compute peak prominences
                    widths = peak_widths(-1.0*data[1], peaks, rel_height=0.5)[0] # compute peak FWHM

                    #print(widths)

                    for i in range(0, len(peaks), 1):
                        if prominences[i] > 2:
                            Q = 500.0*data[0][ peaks[i] ]/widths[i]
                            print("Peak:",data[0][ peaks[i] ], heights['peak_heights'][i], prominences[i], widths[i]/500.0, Q)

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
        print(ERR_STATEMENT);
        print(e);

def peak_search_example():
    # implementation of the peak search example in 
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.peak_widths.html

    from scipy.signal import chirp, find_peaks, peak_widths

    x = np.linspace(0, 6 * np.pi, 1000)
    x = np.sin(x) + 0.6 * np.sin(2.6 * x) # Create a test signal with two overlayed harmonics

    # Find all peaks and calculate their widths at the relative height of 0.5 
    # (contour line at half the prominence height) and 1 (at the lowest contour line at full prominence height)

    peaks, _ = find_peaks(x)
    results_half = peak_widths(x, peaks, rel_height=0.5)
    results_half[0]  # widths

    print(results_half[0])

    results_full = peak_widths(x, peaks, rel_height=1)
    results_full[0]  # widths

    # Plot signal, peaks and contour lines at which the widths where calculated

    plt.plot(x)
    plt.plot(peaks, x[peaks], "x")
    plt.hlines(*results_half[1:], color="C2")
    #plt.hlines(*results_full[1:], color="C3")
    plt.show()

def Nanostick_Laser_Data():
    # parse the measured Nanostick laser data
    # use the data to compute the cavity length
    # check that it correlates with physical dimensions
    # R. Sheehan 6 - 8 - 2019

    FUNC_NAME = ".Nanostick_Laser_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/COSMICC/Nanosticks/June_2019/Laser_Results/'

        if os.path.isdir(DATA_HOME):

            os.chdir(DATA_HOME)

            print(os.getcwd())

            filenames = ["20C_31_d1_7__wave.dat","20C_31_d1_7__current.dat", "20C_31_d1_7__OSA.dat"]

            wl_data = np.loadtxt(filenames[0], unpack = True)
            current_data = np.loadtxt(filenames[1], unpack = True)
            osa_data = np.loadtxt(filenames[2], unpack = True)

            wl_data = 1.0e+9 * wl_data # scale wl to nm
            fr_data = np.zeros( len(wl_data) ); # scale frequency to PHz =1e+15 Hz
            #speed_of_light = 300 # speed of light in units of nm.PHz
            speed_of_light = 3e+5 # speed of light in units of nm.THz
            for i in range(0, len(fr_data), 1):
                fr_data[i] = speed_of_light / wl_data[i] # frequency in units of THz

            print("WL dims:",wl_data.shape)
            print("Il dims:",current_data.shape)
            print("OSA dims:",osa_data.shape)

            # make some plots to test the import
            args = Plotting.plot_arg_single()

            jj = 45

            args.loud = True
            args.marker = 'g-'
            #args.x_label = 'wavelength (nm)'
            args.x_label = 'frequency (THz)'
            args.y_label = 'spectral density (dBm / 50 pm)'
            args.plt_title = '$I_{RSOA} = %(v1)0.1f mA$'%{"v1":current_data[jj]}

            Plotting.plot_single_curve(fr_data, osa_data[jj], args)

            # write some data to afile for analysis
            wl_file = "Wavelength.txt"
            Common.write_data(wl_file, wl_data); 

            wl_file = "Actual_Frequency.txt"
            Common.write_data(wl_file, 1.0e+12*fr_data);

            spct_file = "Spectrum_I_%(v1)d.txt"%{"v1":current_data[jj]}
            Common.write_data(spct_file, osa_data[jj]); 

            # read in and plot the FFT data
            frq_data = Common.read_data("Spectrum_I_150_Frq_data.txt")
            fft_data = Common.read_data("Spectrum_I_150_Abs_FFT_data.txt")

            # make the plot
            args.loud = True
            args.marker = 'r-'
            args.x_label = 'Time (s)'
            args.y_label = 'FFT'
            args.plt_title = '$I_{RSOA} = %(v1)0.1f mA$'%{"v1":current_data[jj]}

            Plotting.plot_single_curve(frq_data, fft_data, args)

        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Read_Data(loud = False):
    # Read the Nanostick Data frame
    # Not all columns will contribute to the glm

    # R. Sheehan 8 - 8 - 2019

    # From looking at the data so far it seems like Nanostick - Bus waveguide separation is the key parameter
    # since all others are basically fixed. You will want to input desired wavelength, stick width, length centre cell to get 
    # separation that ensures resonance at the desired wavelength. Make sure and take a measurement of the length of the chip 
    # that was tested to measure the Nanostick optical spectra. 
    # R. Sheehan 12 - 8 - 2019 

    FUNC_NAME = ".Read_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/TIDA/Nanosticks/'

        if os.path.isdir(DATA_HOME):

            os.chdir(DATA_HOME)

            print(os.getcwd())

            filename = "Nanostick_Dataframe_Middle.csv"

            if glob.glob(filename):
                print("File:",filename,"found")

                data = pd.read_csv( filename, sep = ',')

                titles = list(data) # extract the names of the columns in the data-frame
                # will have to decide which column contains the target, and which columns the attribute data

                if loud:
                    print("Data read into memory")
                    #print(titles)
                    # get some statistics about the data in the columns
                    print("Data summary")
                    print(data.describe())
                    print()

                return [titles, data]
            else:
                ERR_STATEMENT = ERR_STATEMENT + "\nCannot find file:" + filename
                raise Exception
        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
        return [None, None]
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
        return [None, None]

def parse_ns_df(titles, dataframe, target):
    # extract the data needed to build the linear model from the Nanostick dataframe
    # R. Sheehan 22 - 8 - 2019

    FUNC_NAME = ".parse_ns_df()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if dataframe is not None:
            # could use dataframe.shape to get n_data_points and n_cols
            n_pts, n_cols = dataframe.shape

            if target > -1 and target < n_cols:
                # save the target data values, the y-values to be fitted by the model
                # 15. WL 1 / nm (scale to microns)
                # 16. WL 2 / nm (scale to microns)
                # 17. WL 3 / nm (scale to microns)
                target_data = dataframe[ titles[target] ].values

                target_data = target_data / 1000.0 # scale wl to um

                # you only want to create a model with a subset of the data, since most of the parameters are identical
                # parameters of interest
                # 3. bus wg curvature, units of um^{-1}
                # 4. bus-nanostick separation, units of nm, scale to micron
                # 13. length centre cell (optional), units of nm, scale to micron
                # 14. distance facet to nanostick, units of um
                for i in range(0, len(titles), 1):
                    print(i,",",titles[i])

                attrb_titles = [titles[3], titles[4], titles[14]]

                attrb_data = dataframe[attrb_titles].values

                # scale bus-nanostick separation to micron
                attrb_data[:,1] = attrb_data[:,1] / 1000.0

                return [attrb_titles, attrb_data, target_data]
            else:
                ERR_STATEMENT = ERR_STATEMENT + "\nCannot model data that is outside the dataframe"
                raise Exception
        else:
            ERR_STATEMENT = ERR_STATEMENT + "\nNo dataframe was input"
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
        return [None, None]

def Parse_Passive_NS_Data():
    # Read in the various measured nanostick data sets
    # Locate their resonances, store their locations

    FUNC_NAME = ".Parse_Passive_NS_Data()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        DATA_HOME = 'c:/users/robert/Research/CAPPA/Data/COSMICC/Nanosticks/'

        dir1 = '190518_1550nm_NB_2.5mTorr_AIR/'
        dir2 = '190705_1550nm_NB_2.5mTorr_SOG/'
        dir3 = '190705_1550nm_NB_10mTorr_AIR/'
        dir4 = '190705_1550nm_NB_10mTorr_SOG/'

        DATA_HOME = DATA_HOME + dir1

        if os.path.isdir(DATA_HOME):
            os.chdir(DATA_HOME)
            print(os.getcwd())

            #ns_files = glob.glob("Bot*[0-9]_.dat"); thepath = 'Bottom_Resonance_Wavelengths.txt'
            #ns_files = glob.glob("Mid*[0-9]_.dat"); thepath = 'Middle_Resonance_Wavelengths.txt'
            ns_files = glob.glob("Top*[0-9]_.dat"); thepath = 'Top_Resonance_Wavelengths.txt'

            ns_file_list = []
            for i in range(0, len(ns_files), 1):
                retval = Common.extract_values_from_string(ns_files[i])
                #print(int(retval[0]), ns_files[i])
                ns_file_list.append([int(retval[0]), ns_files[i]])

            Common.sort_multi_col(ns_file_list)

            #print(ns_file_list)

            from scipy.signal import find_peaks, peak_prominences, peak_widths

            thefile = open(thepath, "w")

            for i in range(0, len(ns_file_list), 1):
                data = np.loadtxt(ns_file_list[i][1], unpack = True)

                #args = Plotting.plot_arg_single()
                #args.loud = False
                #args.marker = 'r-'
                #args.plt_title = ns_file_list[i][1]
                #Plotting.plot_single_curve(data[0], data[1], args)

                peaks, heights = find_peaks(-1.0*data[1], height = 5)
                prominences = peak_prominences(-1.0*data[1], peaks)[0] # compute peak prominences
                
                peak_locs = []

                print(ns_file_list[i][1])
                print("no. peaks found:",len(peaks))
                #print("Peak: WL (nm), Height, Prominence")
                for j in range(0, len(peaks), 1):
                    if prominences[j] > 4 and data[0][ peaks[j] ] > 1525.0 and data[0][ peaks[j] ] < 1610.0:
                        #print("Peak:",data[0][ peaks[j] ], -heights['peak_heights'][j], prominences[j])
                        peak_locs.append(data[0][ peaks[j] ])
                #print()

                #print(ns_file_list[i][0],",",peak_locs)

                thefile.write("%(v1)d,"%{"v1":ns_file_list[i][0]})
                for k in range(0, len(peak_locs), 1):
                    thefile.write("%(v1)0.9f,"%{"v1":peak_locs[k]})
                thefile.write("\n")

            thefile.close(); 

        else:
            raise EnvironmentError
    except EnvironmentError:
        print(ERR_STATEMENT);
        print('Cannot find',DATA_HOME)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def linear_model(X, y, attrb_titles, loud = False):
    # build a linear model from the data in the data
    # arrays must not be empty and shapes must be compatible
    
    # R. Sheehan 18 - 4 - 2019

    FUNC_NAME = ".linear_model()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if X is not None else False
        c2 = True if y is not None else False
        c3 = True if y.shape[0] == X.shape[0] else False
        c10 = True if c1 and c2 and c3 else False
        
        if c10:
            from random import randrange
            from sklearn.model_selection import train_test_split  
            from sklearn.linear_model import LinearRegression
            
            # create the "training" and test data sets
            # split 65% of the data to "training" set while 35% of the data to test set using below code
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state = randrange(0, 101, 2))

            # ''train'' the model
            model = LinearRegression()  
            
            model.fit(X_train, y_train)

            # compute the score of the fit, this is the R^{2} coefficient, or coefficient of determination
            score = model.score(X_test, y_test)

            # print the computed model coefficients
            if len(attrb_titles) == X.shape[1]:
                coeff_df = pd.DataFrame(model.coef_, attrb_titles, columns=['Slope']) 
                if loud:
                    print("\nFit Parameters")
                    print("Intercept %0.2f:" % model.intercept_)
                    print(coeff_df)
                    print("Fit score: ",score)

            return [model, score, coeff_df, X_test, y_test]
        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
        return [None, None, None, None, None]

def train_model(X, y, attrb_titles, loud = False):
    # build a linear model from the data
    # train the model by maximising the coefficient of determination
    # loop model building until R^{2} coefficient is maximised
    # this is justified since the training data is completey randomised in this approach
    # R. Sheehan 24 - 4 - 2019

    FUNC_NAME = ".train_model()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        score = r_sqr = -1000; 
        coeff_t = mod = Xt = yt = None; # dummy variables used during calculation
        coeff_df = model = X_test = y_test = None; # return variables

        count = 0; count_max = 30; 
        while count < count_max:
            mod, r_sqr, coeff_t, Xt, yt = linear_model(X, y, attrb_titles, False)

            if r_sqr > score:
                model = mod; score = r_sqr; X_test = Xt; y_test = yt; coeff_df = coeff_t; 
                if loud:
                    print("Model build iteration: %(v1)d, Score %(v2)0.5f"%{"v1":count, "v2":score})

            count = count + 1; 

        return [model, coeff_df, X_test, y_test]
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
        return [None, None, None, None]

def make_prediction(Xtest, model):
    # make a prediction of concentration value based on input measurements
    
    FUNC_NAME = ".train_model()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        c1 = True if Xtest is not None else False
        c2 = True if model is not None else False
        c10 = c1 and c2

        if c10:
            # Make a prediction from the test data
            y_pred = model.predict(Xtest) # computes \log_{10}(concentration)

            #y_pred = 10**y_pred # re-scale predicted value to original concentration

            return y_pred
        else:
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
