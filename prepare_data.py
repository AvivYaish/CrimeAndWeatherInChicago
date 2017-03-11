"""
Names: Yuval Shavit, David Barda, Aviv Yaish
Filename: prepare_data.py
Description: Prepares the data set for further use.
Usage: python prepare_data.py
"""

import project_commons as pc
import pandas as pd
import numpy as np
import time


def main():
    """
    This script prepares the dataset used in the project out of the two input datasets.
    """
    # Load data
    crime_data = pd.read_csv(pc.ORIGINAL_CRIME_DATA).dropna()
    weather_data = pd.read_csv(pc.WEATHER_DATA, low_memory=False)

    # convert types to the correct ones
    weather_data['HOURLYDRYBULBTEMPC'] = pd.to_numeric(weather_data['HOURLYDRYBULBTEMPC'], errors='coerce')
    weather_data['HOURLYPrecip'].replace(['T'], [0], inplace=True)
    weather_data['HOURLYPrecip'] = pd.to_numeric(weather_data['HOURLYPrecip'], errors='coerce')

    # remove empty weather data
    weather_data = weather_data[np.isfinite(weather_data['HOURLYDRYBULBTEMPC'])]
    # weather_data = weather_data[np.isfinite(weather_data['HOURLYPrecip'])]

    # convert times to epoch time
    crime_data[pc.EPOCH_TIME_COL] = crime_data['Date'].apply(
        lambda input_time: time.mktime(time.strptime(input_time, pc.time_pattern_crime)))
    weather_data[pc.EPOCH_TIME_COL] = weather_data['DATE'].apply(
        lambda input_time: time.mktime(time.strptime(input_time, pc.time_pattern_weather)))
    crime_data.sort_values(pc.EPOCH_TIME_COL, inplace=True)
    # weather is already sorted

    # drop crimes without weather data
    crime_length = len(crime_data)
    weather_pointer, crime_pointer = 0, 0
    while (crime_pointer < crime_length - 1) and \
            (crime_data.iloc[crime_pointer][pc.EPOCH_TIME_COL] < weather_data.iloc[weather_pointer][pc.EPOCH_TIME_COL]):
        crime_pointer += 1

    # According to our first run, crime_pointer should be 1918205
    # (if this takes too long and you want the code to finish running,
    # simply comment out the previous loop and use the above value)
    crime_data.drop(crime_data.index[range(crime_pointer)], inplace=True)
    crime_data.reset_index(inplace=True)

    # adding day of crime and hour of crime (0 - 23) for each crime
    crime_data['Day'] = crime_data[pc.EPOCH_TIME_COL].apply(
        lambda input_time: time.strftime("%A", time.localtime(input_time)))
    crime_data['Hour'] = crime_data[pc.EPOCH_TIME_COL].apply(
        lambda input_time: time.strftime("%H", time.localtime(input_time)))

    # add temperature to crime data
    def find_nearest(value):
        idx = (np.abs(weather_data[pc.EPOCH_TIME_COL] - value)).argmin()
        return weather_data.iloc[idx]['HOURLYDRYBULBTEMPC']

    crime_data['Temp'] = crime_data[pc.EPOCH_TIME_COL].apply(find_nearest)

    # save the new dataset
    crime_data.to_csv(pc.PROCESSED_CRIME_DATA)

    # plot
    # plotting crimes by hour
    # crime_data['Hour'].value_counts().sort_index().plot()
    #
    #
    # crime_data.groupby(['Day', 'Hour']).size().reset_index()

    # plt.show()
    return

if __name__ == "__main__":
    main()
