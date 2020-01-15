
# WHAT I WANT TO DO

# given a set of csv result files with times and data points
# need to aggregate into a single table that can be scatter plotted
# need to align all y values to a unified x axis
# which means I need to interpolate and create new files

# Create the new x-axis...for instance a sequence of Modified Julian Days
# Write out the new x-axis as it's own csv file.

# For each cav result file, load in the MJD and Altitude columns
# Interpolate to the desired MJD sequence
# Add the interpolated data to the aggregate results.


# csv files need header rows so I can track what the data is
# so a basic data structure is a "Column" list containing a string (which is the header) and an array of values
    # --> pandas 'Series'


# FUNCTIONS I NEED

# it seems that pandas should be used as the underlying framework

# Need a function to add a column of values to a csv file
    #   --> pandas concat({dataframes},axis=1, join='inner')

# Need a function to load columns from a csv into Column structures
    #   --> pandas read_csv()


import os
import numpy as np
import pandas as pd

    # find y values that correspond to x values by linear interpolation of xp, yp
    # x values must be increasing
def interpolate(x, xp, fp):
    np.interp(x,xp,fp)


    # load in a data file, with first column as the x values, and columns of y values
    # load a new data file
    # peel off xp and yp columns from that file
    # create interpolated values from xp, yp aligned to the main x values
    # add the interpolated values to the last column of the data file

def buildAlignedCSV(fileList):
    
        # output file
    agg_path = 'C:/Users/jim/Desktop/Aligned.csv'

        # read in the aggregated, aligned data file
        # (this is initially a single column of MJD values to align to, with header name "MJD")
        # If I was good I could create it here if the file did not already exist
    #agg = pd.read_csv(agg_path)

        # create the list of x values to plot (one value per MJD day)
    x_vals = np.arange(14014, 14364)
    #x_vals = np.arange(14014, 14364).tolist()

                # create a pandas 'Series' from this array, with the given name
    x_ser = pd.Series(x_vals,name = 'MJD')

    agg =  pd.DataFrame(x_ser)   # copy it to the dataframe

    for dataFile in fileList:
            # read in the new data file, skipping the header, and use given column names
        dat = pd.read_csv(dataFile, names = ['MJD','UTC','long','lat','alt'], skiprows = 1)

            # create an array of values from the new data aligned to the x values from agg
        alignedAlt = np.interp(x_ser,dat['MJD'],dat['alt'])

            # create a pandas 'Series' from this array, with the name from the file name
        ser = pd.Series(alignedAlt,name = dataFile)

            # add the new column to the aggregate data frame
        agg = pd.concat([agg, ser], axis=1, join='inner')

            #\\\\\\\\\\\\\\\\\\\\\
        # when all the new columns are added, write the file back out once

        # write it back out
    agg.to_csv(agg_path, index=False, header = True )





def main():

            # edit this path for your system, unless your name is jim
    CWD = 'C:/Users/jim/Desktop/runs/Monte10yr194019/'
    os.chdir(CWD)

        # first get a list of all the csv files in the directory
    list = os.listdir(CWD)
    newlist = []
    for names in list:
        if names.endswith(".csv"):
            newlist.append(names)


    buildAlignedCSV(newlist)
    


main()
            