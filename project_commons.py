"""
Names: Yuval Shavit, David Barda, Aviv Yaish
Filename: project_commons.py
Description: Various useful constants.
"""

# Time patterns for the various date columns of the datasets
time_pattern_weather = "%Y-%m-%d %H:%M"
time_pattern_crime = "%m/%d/%Y %I:%M:%S %p"

# The column name for the epoch time column in both the crime and weather datasets
EPOCH_TIME_COL = 'EpochTime'

# Paths for the datasets
WEATHER_DATA = "./data/weather_data.csv"
ORIGINAL_CRIME_DATA = "./data/crime_data_original.csv"
PROCESSED_CRIME_DATA = "./data/crime_data_with_temp.csv"

# Paths for the pickle files
CLASSIFIER_PKL = "./persistence/classifier.pkl"
PRIMARY_TYPE_LABEL_ENCODER_PKL = "./persistence/primary_type_label_encoder.pkl"

DATE_LEARNING_FORMAT = "%j"

OPEN_WEATHER_API_KEY = "5edb76490a9921956839527a1b49f2d4"