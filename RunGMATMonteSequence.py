#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
import subprocess
import time

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

GMAT_LEM_STATE = """

Create Spacecraft A10LEM;
GMAT A10LEM.DateFormat = UTCGregorian;
GMAT A10LEM.Epoch = '22 May 1969 23:34:16.900'; % From Mission Report Table 6-II 
GMAT A10LEM.CoordinateSystem = LunaFixed;
GMAT A10LEM.DisplayStateType = Planetodetic;
GMAT A10LEM.PlanetodeticRMAG = {};
GMAT A10LEM.PlanetodeticLON = {};
GMAT A10LEM.PlanetodeticLAT = {};
GMAT A10LEM.PlanetodeticVMAG = {};
GMAT A10LEM.PlanetodeticAZI = {};
GMAT A10LEM.PlanetodeticHFPA = {};


    % actually total mass at staging including unused propellants
GMAT A10LEM.DryMass = 10071;

GMAT A10LEM.Cd = 2.2;
GMAT A10LEM.Cr = 1.8;
GMAT A10LEM.DragArea = 15;
GMAT A10LEM.SRPArea = 10;   % worst case
GMAT A10LEM.NAIFId = -10001001;
GMAT A10LEM.NAIFIdReferenceFrame = -9001001;
GMAT A10LEM.OrbitColor = Red;
GMAT A10LEM.TargetColor = Teal;
GMAT A10LEM.OrbitErrorCovariance = [ 1e+070 0 0 0 0 0 ; 0 1e+070 0 0 0 0 ; 0 0 1e+070 0 0 0 ; 0 0 0 1e+070 0 0 ; 0 0 0 0 1e+070 0 ; 0 0 0 0 0 1e+070 ];
GMAT A10LEM.CdSigma = 1e+070;
GMAT A10LEM.CrSigma = 1e+070;
GMAT A10LEM.Id = 'Snoopy';
GMAT A10LEM.Attitude = CoordinateSystemFixed;
GMAT A10LEM.SPADSRPScaleFactor = 1;

"""

# create a new directory for each run 
# script filename reflects the run...like long_-30.script, long_45.script, etc
# result filename also reflects the run...long_-30.csv, etc

# the basic sequence
# read in the next parameter set from params.txt
# patch the spacecraft state
# join the patched state to the mission to create the script
# call GMAT with the script 
# {wait 8 hours for the script to finish }
# copy the result file into the result directory

# running the full sequence of 100 parameter sets will take about a month

def runSet():

    # TODO: You need to edit the below paths for your system

            # path where you want the scripts and data to end up
    CWD = 'C:/Users/jim/Desktop/runs'   # Roger is not my real name

            # path where GMAT is installed
    GMAT_PATH = 'C:/Users/jim/AppData/Local/GMAT/R2018a/bin/'

            # I changed the default GMAT output folder
    GMAT_OUTPUT_PATH = 'C:/Users/jim/Desktop/GMAToutput/'

            # path where this script and the other source files live
    SCRIPT_PATH = 'C:/Users/jim/Desktop/sources/'

            # prefix that will be attached to each script and result file, and the result directory
    PREFIX = 'Monte10yr'

    outputFileName = GMAT_OUTPUT_PATH+'perilune.csv'

            # start by creating a unique subdirectory
    timestring = time.strftime("%H%M%S")
    CWD = CWD + '/'+PREFIX+timestring
    os.mkdir(CWD)

        # open the file with rows of params to try
    thereIsdata = 1
    pfile = open('params.txt', 'r')
    headers = pfile.readline().strip().split(',')

    while (thereIsdata):
        # read in the next set
        params = pfile.readline().strip().split(',')
        if (params[0]==""):
            thereIsdata = 0
            continue    # KlunKy KonstruKt...I am an EE, not a programmer

        # patch the state and write to state.txt
        print("patching the script with param set {}".format(params[0]))
        patchScript(np.array(params[1:]))

        # Concatenate the state to the mission and copy and rename resulting script
        concatenate()
        scriptName = CWD+'/'+PREFIX+params[0]+'.script'

        os.rename('gmat.script',scriptName) 
        print("script created...{}".format(scriptName))
        current_dir = os.getcwd()

            # run GMAT with that script
        os.chdir(GMAT_PATH)
        print ("starting GMAT at {}".format(time.strftime("%H %M %S")))

            # unless you modify the mission, expect this step to run for hours
            # on my system this call completed after about 9 hours
        subprocess.call(['GMAT.exe', '-x', '-m', '-r', scriptName])     # -x exit when finished   -m run minimized, -r run the script at startup

        print ("GMAT finished at {}".format(time.strftime("%H %M %S")))
        time.sleep(2)
        os.chdir(current_dir)

        # copy result file and rename with parameter in filename
        os.rename( outputFileName, CWD+'/'+PREFIX+params[0]+'.csv')

    return CWD



def patchScript(inVal):
    with open("state.txt", 'w') as f:
        f.write(GMAT_LEM_STATE.format(*inVal))


def concatenate():
    filenames = ['state.txt', 'mission.txt']
    with open('gmat.script', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())


def main():

    path = runSet() 


main()