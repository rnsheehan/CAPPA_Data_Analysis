# Import libraries
# You should try an import the bare minimum of modules
import sys # access system routines
import os
import glob
import re

import math
import scipy
import numpy
import matplotlib.pyplot as plt

# add path to our file
sys.path.append('c:/Users/Robert/Programming/Python/Common/')
sys.path.append('c:/Users/Robert/Programming/Python/Plotting/')

import Yenista_TLS
import DBR_Analysis
import FR_Meas_Setup
import Redfinch_AWG
import DANCER
import RSOA_Meas
import TIDA_Data
import COSMICC_Data

def main():
    pass

if __name__ == '__main__':
    main()

    pwd = os.getcwd() # get current working directory

    print(pwd)

    #Yenista_TLS.Yen_Char_Plots()

    #DBR_Analysis.DBR_Sim_Plots()

    #FR_Meas_Setup.Meas_Setup_Plots()

    #Redfinch_AWG.Make_AWG_Plots()

    #DANCER.DANCER_Plots()

    #RSOA_Meas.plot_Vpp_R_Curve()

    #TIDA_Data.Plot_SiN_RI()

    #TIDA_Data.Plot_coupling_coeff(True)

    #TIDA_Data.Plot_Dispersion_Curve_Data()

    #TIDA_Data.Filter_Data()

    #num = 2

    #COSMICC_Data.Nanostick_Spectrum(num, True, True)
    
    #COSMICC_Data.Nanostick_Peak_Analysis(num)

    #COSMICC_Data.peak_search_example()

    #COSMICC_Data.Nanostick_Spectra(False, True)

    #COSMICC_Data.Nanostick_Laser_Data()

    #COSMICC_Data.Parse_Passive_NS_Data()

    loud = True

    titles, dataframe = COSMICC_Data.Read_Data(loud)

    attrb_titles, attrb, target = COSMICC_Data.parse_ns_df(titles, dataframe, target = 16)

    print(attrb.shape)

    for i in range(0, len(target), 2):
        print(attrb[i][0],",",attrb[i][1],",",attrb[i][2],",",target[i])

    # ''train'' the model
    # the test data {X_test, y_test} is a subset of the actual data set
    # in reality X_test would be a set of measured intensity values from the
    # control, antigen, T1 test strips
    # there would be no equivalent y_test values
    model, coeff_df, X_test, y_test = COSMICC_Data.train_model(attrb, target, attrb_titles, loud)

    if loud:
        print("\nModel Intercept: ",model.intercept_)
        print("Model Coefficients: ")
        print(coeff_df)
        print("")

    print(X_test.shape)

    y_pred = COSMICC_Data.make_prediction(X_test, model)

    for i in range(0, len(y_pred), 1):
        print("Bus Curvature (um^{-1}), Bus Separation (um), Cavity Length (um):",X_test[i])
        print("Predicted Resonance Wavelength (um):", y_pred[i])
        print("Actual Resonance Wavelength (um):", y_test[i])
        print("Relative Error:", 100*(y_pred[i] - y_test[i])/y_pred[i])
        print("")
