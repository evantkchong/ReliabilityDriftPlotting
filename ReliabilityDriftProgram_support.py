#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.21
#  in conjunction with Tcl version 8.6
#   May 10, 2019 05:28:54 PM +0800  platform: Windows NT
# App Icon made by https://www.freepik.com/ from www.flaticon.com

import time  # for optimizing, delete before build
import multiprocessing
import glob
import os
import re
import sys
from tempfile import TemporaryFile
from tkinter import filedialog
from tkinter.filedialog import askdirectory, askopenfilenames

# if os.name == "posix":
#     import matplotlib

#     matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
from tqdm import tqdm

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True


def universal_load_csv(filepath):
    """
    This function reads .csv files for any test type.
    """
    with open(filepath) as f, TemporaryFile("w+") as t:
        # Clean the text file so that it can be parsed by the pandas .read_csv method
        for line in f:
            t.write(line.replace(" ", ""))
        t.seek(0)
        ln = len(line.strip().split(","))
        header = t.readline().strip().split(",")
        header += range(ln)
        # Read the temporary file into a dataframe
        df_raw = pd.read_csv(t, names=header)
        del t
        try:
            df_raw["LOT_ID"] = df_raw.at[11, "AMS_CSV_STANDARD_FORMAT"]
        except:
            df_raw["LOT_ID"] = "None"

        cols = df_raw.columns.tolist()
        cols = cols[:1] + cols[-1:] + cols[1:-1]
        df_raw = df_raw[cols]

        try:
            idx = df_raw.index[
                df_raw["AMS_CSV_STANDARD_FORMAT"] == "PART_INDEX"
            ].tolist()
            df_new = df_raw.loc[idx[0] : :, "LOT_ID"::].reset_index()
            df_new.columns = df_new.iloc[1]
        except:
            df_new = df_raw.loc[0::, "LOT_ID"::].reset_index()
            df_new.columns = df_new.iloc[0]

        del df_raw

        df_new.columns = [
            "dropme",
            "LOT_ID",
            "PART_INDEX",
            "PART_X",
            "PART_Y",
            "PART_BIN",
            "SITE",
            "TOUCHDOWN_INDEX",
            "TIMESTAMP",
        ] + df_new.columns.tolist()[9:]
        df_new = (
            df_new.drop("dropme", axis=1)
            .drop([0, 1, 2, 3, 4, 5, 6])
            .reset_index()
            .drop("index", axis=1)
        )
        df_new = df_new[df_new.columns.dropna()]
        try:
            df_new["TIMESTAMP"] = pd.to_datetime(
                df_new["TIMESTAMP"], format="%d.%m.%Y%H:%M:%S"
            )
        except:
            df_new["TIMESTAMP"] = pd.to_datetime(
                df_new["TIMESTAMP"], format="%d.%m.%Y %H:%M:%S"
            )
        df_new.iloc[:, 8:] = df_new.iloc[:, 8:].astype(float)

        return df_new


# Convert dataframe into multi-indexed dataframe with cycle number as main index
def makemulti(frame, cyclenum):
    frame["Hours"] = cyclenum
    newframe = frame.set_index(["Hours"])
    return newframe


# Read cyclenum from filename
def cycle(filename):
    # Searches for XXXXC, XXXX C or XXXXH in the filename where XXXX is the cycle time number
    m = re.search(r"(\d{1,}) ?[CHX]", filename, flags=re.IGNORECASE)
    try:
        numcycle = int(m.group(1))
    except AttributeError:
        # if no regex match can be found, m.group(1) will throw an attribute error
        # We handle this by assuming the file is for cycle time zero
        if m == None:
            # Addling flexibility for "HXXXX" naming of cycletime
            m = re.search(r"[CHX](\d{1,})", filename, flags=re.IGNORECASE)
            try:
                numcycle = int(m.group(1))
            except AttributeError:
                print("setting numcycle for file {} to 0".format(filename))
                numcycle = 0
    except Exception as e:
        print(
            "setting numcycle for file {} to 0 due to exception {}".format(filename, e)
        )
        numcycle = 0
    return numcycle


# Read SNx from filename
def serial_number(filename):
    # Each actual SN number corresponds to a 'PART_X' and 'PART_Y' coordinate
    # We use this dictionary for the conversion
    convertdict = {
        1: [0, 0],
        2: [1, 0],
        3: [2, 0],
        4: [3, 0],
        5: [4, 0],
        6: [4, -1],
        7: [3, -1],
        8: [2, -1],
        9: [1, -1],
        10: [0, -1],
        11: [0, -2],
        12: [1, -2],
        13: [2, -2],
        14: [3, -2],
        15: [4, -2],
        16: [4, -3],
        17: [3, -3],
        18: [2, -3],
        19: [1, -3],
        20: [0, -3],
        21: [0, -4],
        22: [1, -4],
        23: [2, -4],
        24: [3, -4],
        25: [4, -4],
        26: [4, -5],
        27: [3, -5],
        28: [2, -5],
        29: [1, -5],
        30: [0, -5],
    }
    try:
        # We use regex search to obtain SN number
        m = re.search(r"SN(\d{1,2})", filename, flags=re.IGNORECASE)
        snx = int(m.group(1))
        index_xy = convertdict.get(snx)
        return index_xy
    except:
        return None


def find_stress(folderpath):
    """
    Finds stress-named folders present such as "HTOL, HTOL1, HTOL_ref, TH, TC, HTSL, ..." 
    in a given directory and returns them as a list.
    """
    # Obtain folder names in given directory using Glob and OS
    list_of_folders = glob.glob(folderpath + "/*")
    # folder_list = []
    # for i in list_of_folders:
    #     folder_list.append(os.path.basename(i))

    folder_list = [os.path.basename(i) for i in list_of_folders]

    stress_keywords = ["HTOL", "TH", "TC", "HTSL", "HAST", "Reference", "AAA", "BBB", "CCC", "DDD"]

    # # Add folder names that fit our stress types to "stress_list"
    # stress_list = []
    # for folder_name in folder_list:
    #     for stress in stress_keywords:
    #         if stress in folder_name:
    #             stress_list.append(folder_name)

    stress_list = [
        folder_name
        for folder_name in folder_list
        for stress in stress_keywords
        if (
            stress in folder_name
            and "!" not in folder_name
            and ".rtf" not in folder_name
        )
    ]

    return stress_list


def findtesttype(filename):
    """
    This function tries to find the test type of the file by looking through the filename for 'FFT', 'NFT' or 'LIV'. 
    Case is ignored in this search (ie. uppercase vs lowercase). 
    If a match cannot be found, the test type is taken to be 'Unknown' and will generate an error later on.
    """
    try:
        # Search for the words FFT, NFT or LIV in the filename in order to guess which test type it belongs to
        m = re.search("(FFT|NFT|LIV)", filename, flags=re.IGNORECASE)
        testtype = str(m.group(1).upper())
    except:
        testtype = "Unknown"
    return testtype


def combinecsv(listoffiles):
    """
    This function takes a list of files and combines them into a single dataframe,
    using universal_load_csv() to parse the files into dataframes,
    makemulti() to combine the dataframes with cycle() to identify 
    the hours for each of the files.
    """
    for file in listoffiles:
        # print('Processing {}'.format(file))
        if file == listoffiles[0]:
            main_df = makemulti(universal_load_csv(file), cycle(file))
        elif "retest" in file.lower():
            # Skip files with retest in the name
            tqdm.write("Skipping Retest File: {}".format(file))
            continue
        elif "rerun" in file.lower():
            # Skip files with rerun in the name
            tqdm.write("Skipping Retest File: {}".format(file))
            continue
        elif "sn" in file.lower():
            # Skip files with SN in the name
            tqdm.write("Skipping Retest File: {}".format(file))
            continue
        elif re.search(r"u\d+", file, flags=re.IGNORECASE) != None:
            # Skip files that have "u22" or similar in the filename
            tqdm.write("Skipping Retest File: {}".format(file))
            continue
        else:
            new_df = makemulti(universal_load_csv(file), cycle(file))
            main_df = main_df.append(new_df, sort=False)
        # Convert column PART_INDEX to numbers so that it can be sorted properly
        main_df[["PART_INDEX"]] = main_df[["PART_INDEX"]].apply(pd.to_numeric)
        # Sort created dataframe by Hours followed by PART_INDEX
        main_df = main_df.sort_values(by=["Hours", "PART_INDEX", "TIMESTAMP"])
    return main_df


def plotMPIdata(test_dataframe, drift=False):
    """
    Takes a test type (LIV, NFT or FFT) and a dataframe and creates an interactive grouped box plot via local host which
    opens in the user's default browser.

    The labels that the plots are grouped-by are taken from the dataframe headers fed into the plot function.
    """

    # Labels for plotting
    label_raw = test_dataframe.columns.values.tolist()

    if drift == False:
        testlabels = label_raw[9:]
    else:
        test_dataframe.reset_index(level=0, inplace=True)
        testlabels = label_raw[2:]

    # Generate dictlist for data
    dict_list_data = []

    def dict_generator_data(label):
        new_dict = dict(
            type="box",
            y=test_dataframe[label],
            name="{}".format(label),
            transforms=[dict(type="groupby", groups=test_dataframe["Hours"])],
        )
        return new_dict

    for label in testlabels:
        dict_list_data.append(dict_generator_data(label))

    # Generate dictlist for the updatemenus
    dict_list_menu = []

    def dict_generator_menu(label, label_list):
        label_index = label_list.index(label)
        temporary_list = [False] * (len(label_list))
        temporary_list[label_index] = True
        # plotname = "{:02d}_".format(label_index + 1) + label
        if drift == False:
            plotname = label
        else:
            plotname = label + " Drift"
        new_dict = dict(
            label=plotname, method="update", args=[{"visible": temporary_list}]
        )
        return new_dict

    for label in testlabels:
        dict_list_menu.append(dict_generator_menu(label, testlabels))

    # Put dictionary objects into the data construct
    data = dict_list_data

    # Put dictionary objects into the dropdownlist
    updatemenus = list(
        [
            dict(
                active=-1,
                buttons=dict_list_menu,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,
                xanchor="left",
                y=1.1,
                yanchor="bottom",
            )
        ]
    )

    fig = dict({"data": data}, layout=dict(updatemenus=updatemenus))

    plotly.offline.plot(fig, validate=False)


def saveMPIdata_universal(
    test_dataframe, save_location, stress, drift=False, flyers=True
):
    """
    This function plots boxplots with matplotlib and saves them in a specified save_location.
    """
    # Extract parameters from dataframe

    label_raw = test_dataframe.columns.values.tolist()
    if drift == False:
        testlabels = label_raw[9:]
        test_dataframe.iloc[1:, 1:].replace(0, np.nan, inplace=True)
    else:
        testlabels = label_raw[1:]

    def series_values_as_dict(series_object):
        tmp = series_object.to_dict().values()
        return [y for y in tmp][0]

    def find_values(bp, ax):
        """
        find_values() takes a boxplot dictionary as well as plot axes.
        It returns the coordinates of the median lines as well as the optimal
        fontspacing for annotations
        """
        # We use a list comprehension as well as the .get_xydata() function to
        # obtain the x and y values for the median lines of the boxplot

        # First we create a list containg an array for each datapoint
        # The array structure is of the form array((x_l, y), (x_r, _))

        median_data = [line.get_xydata() for line in bp["medians"]]

        # Next we extract the relevant values from median_data
        # median_y is simply y while median_x has to be calculated via (x_l + (x_r - x_l) / 2)
        # in order to give us the coordinates of the center of the median line
        median_y = [i[0][1] for i in median_data]
        median_x = [(i[0][0] + (i[1][0] - i[0][0]) / 2) for i in median_data]

        # The fontspacing is half the width of a median line + 0.02
        fontspacing = ((median_data[0][1][0] - median_data[0][0][0]) / 2) + 0.02

        # bins = len(median_x)
        # if bins >= 5:
        #     fontspacing = 0.275
        # elif bins == 4:
        #     fontspacing = 0.25
        # elif bins == 3:
        #     fontspacing = 0.18
        # else:
        #     fontspacing = 0.16
        return median_x, median_y, fontspacing

    def add_values(bp, ax, fontspacing):
        fontsize = 12
        # fontspacing = 0.27

        """ This actually adds the numbers to the various points of the boxplots"""
        for element in ["medians", "caps"]:
            for line in bp[element]:
                # Get the position of the element. y is the label you want
                (x_l, y), (x_r, _) = line.get_xydata()
                if not np.isnan(y):  # Make sure datapoints exist
                    x_line_center = x_l + (x_r - x_l) / 2
                    y_line_center = y
                    # Format Data Callouts based on magnitude
                    if y >= 100:
                        numformat = "%.1f"
                    elif y >= 1000:
                        numformat = "%d"
                    else:
                        numformat = "%.2f"
                    # overlay the value:  on the line, from center to right

                    if element == "medians":
                        ax.text(
                            x_line_center + fontspacing,
                            y_line_center,  # Position
                            numformat % y,  # Value (3f = 3 decimal float)
                            verticalalignment="center",  # Centered vertically with line
                            color="green",  # Value for median will be green
                            fontsize=fontsize,
                        )

                    # Disable quartile numbers
                    # elif element == "whiskers":
                    #     ax.text(
                    #         x_line_center + fontspacing,
                    #         y_line_center,  # Position
                    #         numformat % y,  # Value (3f = 3 decimal float)
                    #         verticalalignment="center",  # Centered vertically with line
                    #         color="tab:blue",  # Value for whiskers will be tableau blue
                    #         fontsize=fontsize,
                    #    )

                    else:
                        ax.text(
                            x_line_center + fontspacing,
                            y_line_center,  # Position
                            numformat % y,  # Value (3f = 3 decimal float)
                            verticalalignment="center",  # Centered vertically with line
                            fontsize=fontsize,
                        )

        fryers = bp[
            "fliers"
        ]  # Fliers are the 'outliers'. We want the values for these too!
        # Iterate over it!
        if flyers == True:
            for fly in fryers:
                fdata = fly.get_xydata()
                if fdata.any() == False:
                    pass
                else:
                    for btuple in fdata:
                        x, y = btuple
                        if not np.isnan(y):
                            # Settings the appearance of the outliers and its value
                            fly.set(
                                marker="o",
                                markerfacecolor="tab:orange",
                                markeredgecolor="tab:orange",
                            )
                            ax.text(
                                x - fontspacing,
                                y,
                                numformat % y,
                                verticalalignment="center",
                                horizontalalignment="left",
                                color="tab:orange",
                                fontsize=fontsize,
                            )

    # Iterate through the test parameters and save a boxplot grouped by cycle time for each
    for label in testlabels:
        fig, axes = plt.subplots(1, figsize=(16, 10))
        boxplot = test_dataframe.boxplot(
            column=[label],
            by=["Hours"],
            grid=True,
            figsize=(8, 6),  # previously 12x8
            ax=axes,
            return_type="dict",
        )
        bp_dict = series_values_as_dict(boxplot)
        median_x, median_y, fontspacing = find_values(bp_dict, axes)
        add_values(bp_dict, axes, fontspacing)
        if drift == False:
            plt.title("Boxplot grouped by Hours under {}".format(stress))
        else:
            plt.title("Boxplot of Drift for {}".format(stress))
        plt.plot(median_x, median_y)
        plt.suptitle("")
        plt.xlabel("Hours", fontsize=18)  # previously 16
        plt.ylabel(label, fontsize=18)
        plt.xticks(fontsize=14)  # previously 12
        plt.yticks(fontsize=14)
        # Save the boxplots in save_location
        if drift == False:
            plt.savefig(save_location + label + "_boxplot.png", transparent=True)
        else:
            plt.savefig(save_location + label + "_Drift_boxplot.png", transparent=True)
        plt.close()

# default_open_location = r"\\fstpdata\Team\Quality\Reliability\"


def build_database():
    """
    Invoked by the 'Compile Files to Database' button in the GUI.
    Takes a list of files for a single RTO and filters them based on the 
    appearance of the stress_test keywords 'HTOL, THB, TH, TC, HTSL' 
    followed by the measurement_type keywords 'NFT, LIV, FFT'.
    
    If there are any files that are singular SN measurements, these measurement
    values will be replace any older measurements made (based on measurement time/date)
    If any files are excel files, sheets with sheet names from 0 - 1000 will be
    processed into the dataset with empty sheets being ignored.

    Data is saved in .csv files stored in the same folder with the following folder_name structure:
    '[relative path] > [RTO Number] > [Stress_Test] > RTO-number_MeasurementType_Data.csv'.
    An example of this folder_name structure would be 
    'C:/Datalogs/RTO-4149/HTSL/RTO-4149_NFT_Data.csv'
    """
    folderpath = askdirectory(
        parent=root, initialdir="/", title="Please select an RTO folder"
    )

    # This prevents the program from hanging if the task is cancelled
    if folderpath == "":
        return root.update()

    print("Building Database...")

    stress_list = find_stress(folderpath)

    print("Processing {}".format(stress_list))

    stress_test_pair = [[stress, test] for stress in stress_list for test in ("FFT", "LIV", "NFT")]
    processes = []
    
    for pair in stress_test_pair:
        p = multiprocessing.Process(target=call_build_database, args=(folderpath, pair[0], pair[1],))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print("RTO Database Build Completed")

def call_build_database(folderpath, stress_type, measurement_type):
    list_of_files = glob.glob(
            folderpath + "/{}/**/*{}.csv".format(stress_type, measurement_type),
            recursive=True,
        )
        # Determine RTO number of the folder

    if len(list_of_files) == 0:
        print(
            "Folder for Stress: {} + Test: {} not found".format(
                stress_type, measurement_type
            )
        )
        pass

    else:
        m = re.search(r"RTO.(\d{1,})", list_of_files[0], flags=re.IGNORECASE)
        rto_num = str(m.group(1))

        # Define the location to save the files to
        savepath = folderpath + "/{}/RTO-{}_{}_Database.csv".format(
            stress_type, rto_num, measurement_type
        )

        try:
            main_df = combinecsv(list_of_files)
            main_df.dropna(subset=["PART_INDEX"], inplace=True)
            main_df.to_csv(savepath)
        except PermissionError:
            print(
                "[ERROR]: Please close existing RTO Database file 'RTO-{}_{}_Database.csv' before building database".format(
                    rto_num, measurement_type
                )
            )

def generate_drift_statistics(dataframe, savelocation):
    """    
    Calculates the following drift statistics: Average Drift, Absolute Average Drift, Maximum Absolute Drift,
    Mininum Absolute Drift, Raw Average Drift, Raw Average Drift, Maximum Raw Drift
    and Mininum Raw Drift.

    Takes a dataframe read from a database.csv file and a save location. 
    Saves the calculated drift.xlsx in the designated save location
    """
    # Sorting is now done in the database file creation stage but
    # we stll do it here as a safety check as files might manually amended
    dataframe.sort_values(by=["Hours", "PART_INDEX", "TIMESTAMP"], inplace=True)
    # Labels for calculation
    label_raw = dataframe.columns.values.tolist()
    labels = label_raw[9:]

    s = dataframe.PART_INDEX.unique()
    s = np.append(s, ["Min", "Max", "Mean", "Std"])
    s_df = pd.DataFrame(s, columns=["PART_INDEX"])

    hour_range = dataframe.Hours.unique().tolist()
    cols = ["PART_INDEX"]
    cols.extend(hour_range)
    # print("Cycles Detected: ", cols[1:])
    dataframe.set_index(["Hours", "PART_INDEX"], inplace=True)

    # We save the data to an excelwriter object
    with pd.ExcelWriter(savelocation + "RawDrift.xlsx") as rawwriter, pd.ExcelWriter(
        savelocation + "AbsoluteDrift.xlsx"
    ) as abswriter:
        try:      
            dict_of_raw_drift = {label : s_df.copy() for label in labels}
            dict_of_abs_drift = dict_of_raw_drift.copy()
 
            for label in labels:
                baseline = dataframe[label][0]

                for hour in hour_range[1:]:
                    # Calculate Raw Drift values
                    curr_value = dataframe[label][hour]
                    raw_drift = ((curr_value - baseline) / baseline) * 100

                    # Calculate Raw Drift Summary statistics
                    describe_raw_drift = pd.Series(
                        data=[
                            raw_drift.min(),
                            raw_drift.max(),
                            raw_drift.mean(),
                            raw_drift.std(),
                        ],
                        index=["Min", "Max", "Mean", "Std"],
                    )
                    all_raw_drift = raw_drift.append(
                        describe_raw_drift
                    )  # Append Summary Statistics to Raw Values
                    dict_of_raw_drift["{}".format(label)][
                        hour
                    ] = all_raw_drift.values  # Add values to Dataframe in Dictionary

                    abs_drift = abs(raw_drift)  # Calculate Absolute Drift Values
                    # Calculate Abs Drift Summary Statistics
                    describe_abs_drift = pd.Series(
                        data=[
                            abs_drift.min(),
                            abs_drift.max(),
                            abs_drift.mean(),
                            abs_drift.std(),
                        ],
                        index=["Min", "Max", "Mean", "Std"],
                    )

                    # abs_drift.sort_index(inplace=True, na_position="last")

                    all_abs_drift = abs_drift.append(
                        describe_abs_drift
                    )  # Append Summary Statistics to dataframe of Absolute Values

                    dict_of_abs_drift["{}".format(label)][
                        hour
                    ] = all_abs_drift.values  # Add values to Dataframe in Dictionary

                # Stack Dataframes in excelwriter objects
                dict_of_raw_drift["{}".format(label)].to_excel(
                    rawwriter, sheet_name=label[:30], index=False
                )
                dict_of_abs_drift["{}".format(label)].to_excel(
                    abswriter, sheet_name=label[:30], index=False
                )
            # Save excelwriter objects to Excel Files with each Excel Sheet generated from one Dataframe
            rawwriter.save()
            abswriter.save()
        except ValueError:
            print(
                "More than 30 values detected for {} hours, \nplease check data for {}".format(
                    hour, savelocation
                )
            )
     


def drift_calculation_select():
    """
    Invoked by the 'Compute Drift' button in the GUI.
    Reads database .csv file generated using build_database() 
    for a single Reliability Test Order and calculates drift statistics
    using generate_drift_statistics()

    After calculation, a save prompt is invoked. Saves drift statistics as an excel file.
    """
    stringoffiles = askopenfilenames(
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )

    # This prevents the program from hanging if the task is cancelled
    if stringoffiles == "":
        return root.update()

    print("Calculating Drift...")

    listoffiles = root.tk.splitlist(stringoffiles)

    for file in listoffiles:
        # try:
        m = re.search(r"RTO.(\d{1,})", file, flags=re.IGNORECASE)
        rto_num = str(m.group(1))
        measurement_type = findtesttype(file)
        savepath = (
            os.path.dirname(file)
            + "/Drift Calculation/"
            + "RTO-{}_{}_".format(rto_num, measurement_type)
        )

        if not os.path.exists(os.path.dirname(file) + "/Drift Calculation/"):
            os.makedirs(os.path.dirname(file) + "/Drift Calculation/")

        print("Saving calculations to: ", os.path.dirname(file) + "/Drift Calculation/")

        main_df = pd.read_csv(file)
        
        generate_drift_statistics(main_df, savepath)
        print("Drift Calculations Saved")
     
    # except:
    #     print('calc failed')

    sys.stdout.flush()

def call_generate_drift_statistics(file):
        m = re.search(r"RTO.(\d{1,})", file, flags=re.IGNORECASE)
        rto_num = str(m.group(1))
        measurement_type = findtesttype(file)
        savepath = (
            os.path.dirname(file)
            + "/Drift Calculation/"
            + "RTO-{}_{}_".format(rto_num, measurement_type)
        )

        if not os.path.exists(os.path.dirname(file) + "/Drift Calculation/"):
            os.makedirs(os.path.dirname(file) + "/Drift Calculation/")

        # print("Saving calculations to: ", os.path.dirname(file) + "/Drift Calculation/")

        main_df = pd.read_csv(file)

        generate_drift_statistics(main_df, savepath)

def drift_calculation():
    """
    Invoked by the 'Compute Drift' button in the GUI.
    Reads database .csv files generated using build_database() 
    for a single Reliability Test Order and calculates drift statistics
    using generate_drift_statistics()

    After calculation, a save prompt is invoked. Saves drift statistics as an excel file.
    """

    folderpath = askdirectory(
        parent=root, initialdir="/", title="Please select an RTO folder"
    )

    # This prevents the program from hanging if the task is cancelled
    if folderpath == "":
        return root.update()

    stress_list = find_stress(folderpath)

    print("Processing Drift Calculation for {}".format(stress_list))
    # We create a separate list for each test type + stress type pair as we will save

    start = time.time()

    listoffiles = glob.glob(folderpath + "/**/*_Database.csv", recursive=True)

    # Create list of processes to multiprocess
    processes = []

    for file in listoffiles:
        # Create processes and add them to the list of processes
        # call_generate_drift_statistics has to be a global function
        p = multiprocessing.Process(target=call_generate_drift_statistics, args=(file,))
        processes.append(p)
        p.start()
    
    for process in processes:
        process.join()

    end = time.time()
    print('Took {} seconds'.format(end-start))  
    # except:
    #     print('calc failed')

    sys.stdout.flush()


def file_plot_interactive():
    """
    Invoked by the 'Select Files to Plot (interactive)' button in the GUI.
    Reads a database .csv file generated using build_database() 
    for a single Reliability Test Order. 
    
    Generates an interactive plot
    with plotly and serves it via localhost. Automatically opens in
    default browser
    """
    stringoffiles = askopenfilenames(
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )

    # This prevents the program from hanging if the task is cancelled
    if stringoffiles == "":
        return root.update()

    print(stringoffiles)
    listoffiles = root.tk.splitlist(stringoffiles)
    for i in listoffiles:
        main_df = pd.read_csv(i)
        plotMPIdata(main_df)

    sys.stdout.flush()

def call_generate_raw_img(folderpath, stress_type, measurement_type):
    database_files = glob.glob(
        folderpath
        + "/{}/*_{}_Database.csv".format(stress_type, measurement_type),
        recursive=True,
    )

    listlen = len(database_files)

    if listlen == 0:
        tqdm.write(
            "Stress: {} and Test: {} not found".format(
                stress_type, measurement_type
            )
        )
        pass
    
    else:
        # database_files = glob.glob(folderpath+'/**/*Database.csv', recursive=True)
        for file in database_files:

            main_df = pd.read_csv(file)

            save_location = folderpath + "/{}/{}_boxplot/".format(
                stress_type, measurement_type
            )
            if not os.path.exists(save_location):
                os.makedirs(save_location)
            saveMPIdata_universal(main_df, save_location, stress_type)
            del main_df  # Garbage Collect main_df to free up memory


def folder_save_img():
    """
    Invoked by the "Plot All Files in Folder" button in the GUI.
    Reads multiple database .csv files of the format generated by 
    the build_database() function. Groups files by identifying
    folder structure. Groups first by RTO number, 
    followed by stress test type 'HTOL, THB, TH, TC, HSTL' 
    and finally by measurement type 'NFT, LIV, FFT'.

    Saves files in the second lowest folder ie.
    '[relative path] > [RTO Number] > [Stress_Test_Plot] > [Measurement_Type Plot Folder]'
    An example of this folder_name structure would be 
    'C:/Datalogs/RTO-4149/HTSL/NFT_boxplot'
    """
    folderpath = askdirectory(
        parent=root, initialdir="/", title="Please select a folder_name"
    )

    start = time.time()
    # This prevents the program from hanging if the task is cancelled
    if folderpath == "":
        return root.update()

    stress_list = find_stress(folderpath)

    print("Starting Raw Data Batch Plotting.\nProcessing data for {}".format(stress_list))

    processes = []

    stress_test_pair = [[stress, test] for stress in stress_list for test in ("FFT", "LIV", "NFT")]

    for pair in stress_test_pair:
        p = multiprocessing.Process(target=call_generate_raw_img, args=(folderpath, pair[0], pair[1],))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    tqdm.write("Complete")
    end = time.time()
    print('Took {} seconds'.format(end-start))
    sys.stdout.flush()


def merge_drift_calc(dict_of_df):
    """
    This function takes a dictionary of dataframes (dict_of_df) and iterates over
    the entries in the dictionary. Each dataframe corresponds to one sheet in the drift_calculation
    excel file. reshape_df() is used to transform
    the dataframe into the form read by plotMPIdata() and saveMPIdata_universal().
    """

    def reshape_df(label):
        """
        reshape_df() transposes the input dataframe while retaining "PART_INDEX" as a column value
        """
        working_df = dict_of_df[label][:-4].drop(columns="PART_INDEX")
        # print(working_df.head(40))
        s1 = working_df.loc[0]
        s1.name = "{}".format(label)
        num_cycles = len(s1)
        SN = [1] * num_cycles
        for i in range(len(working_df))[1:]:
            additional = working_df.loc[i]
            s1 = s1.append(additional)
            SN.extend([i + 1] * num_cycles)
        s2 = pd.DataFrame(SN, index=s1.index)
        main_df = pd.concat([s2, s1], axis=1)
        main_df.index.name = "Hours"
        main_df.columns = ["PART_INDEX", label]
        main_df.set_index(main_df.index, "PART_INDEX")
        return main_df

    for label in dict_of_df:
        if label == list(dict_of_df.keys())[0]:
            first = reshape_df(label)
        else:
            other = reshape_df(label)
            # first = pd.merge(first, other, on='PART_INDEX',ignore_index = True)
            first = pd.merge(first, other, on=["Hours", "PART_INDEX"])
            # first.join(other, how = 'outer', on = ['Hours', 'PART_INDEX'])
    return first


def drift_plot_interactive():
    print("ReliabilityDriftProgram_support.drift_plot_interactive")

    stringoffiles = askopenfilenames(
        filetypes=(("Excel Files", "*.xlsx"), ("All files", "*.*"))
    )

    # This prevents the program from hanging if the task is cancelled
    if stringoffiles == "":
        return root.update()

    print(stringoffiles)
    listoffiles = root.tk.splitlist(stringoffiles)
    for i in listoffiles:
        dict_of_df = pd.read_excel(i, sheet_name=None)
        drift_dataframe = merge_drift_calc(dict_of_df)
        plotMPIdata(drift_dataframe, drift=True)

    sys.stdout.flush()


def folder_drift_save_img():
    """
    Reads data from DriftCalculation.xlsx files in the selected directory.
    Iterates through each sheet in the .xlsx file (corresponding to each test parameter), 
    followed by using saveMPIdata_universal() to plot boxplots for the sheet data.
    Saves images in a '[Test_Type]_Drift_Boxplot' folder
    """
    folderpath = askdirectory(
        parent=root, initialdir="/", title="Please select a RTO folder"
    )

    start = time.time()
    # This prevents the program from hanging if the task is cancelled
    if folderpath == "":
        return root.update()

    stress_list = find_stress(folderpath)

    print("Starting Drift Data Batch Plotting.\nProcessing data for {}".format(stress_list))
    
    stress_test_pair = [[stress, test] for stress in stress_list for test in ("FFT", "LIV", "NFT")]

    processes = []

    for pair in stress_test_pair:
        p = multiprocessing.Process(target=call_generate_raw_img, args=(folderpath, pair[0], pair[1],))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    end = time.time()
    print('Drift Plotting Complete.\nTook {} seconds'.format(end-start)) 
    sys.stdout.flush()

def call_drift_plot(folderpath, stress_type, measurement_type   ):
    database_files = glob.glob(
                folderpath
                + "/{}/Drift Calculation/*_{}_AbsoluteDrift.xlsx".format(
                    stress_type, measurement_type
                ),
                recursive=True,
            )

    listlen = len(database_files)

    if listlen == 0:
        tqdm.write(
            "Drift Calculation for  {} + {} not found".format(
                stress_type, measurement_type
            )
        )
        pass

    else:
        dict_of_df = pd.read_excel(database_files[0], sheet_name=None)
        # Passing sheet_name = None tells the read_excel function to read all sheets in the excel file

        save_location = folderpath + "/{}/{}_Drift_boxplot/".format(
            stress_type, measurement_type
        )
        if not os.path.exists(save_location):
            os.makedirs(save_location)
        drift_dataframe = merge_drift_calc(dict_of_df)
        saveMPIdata_universal(
            drift_dataframe, save_location, stress_type, drift=True
        )

        del dict_of_df  # Garbage Collect main_df to free up memory


def DoAll():
    print("ReliabilityDriftProgram_support.DoAll")
    sys.stdout.flush()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


if __name__ == "__main__":
    import ReliabilityDriftProgram
    ReliabilityDriftProgram.vp_start_gui()
