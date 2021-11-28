# Crime and Weather in Chicago
## Authors: Aviv Yaish, David Barda, Yuval Shavit

A project exploring the relationship between crime and weather in Chicago.


https://user-images.githubusercontent.com/12000894/143773513-5ba620b8-3bee-4437-916d-37269588ad70.mp4



### Installation and Usage
1. Install libraries:

    a. Install Anaconda 4.3.0:

        https://www.continuum.io/downloads

    b. Install folium 0.3:

        https://github.com/python-visualization/folium

    c. Install branca:

        pip install branca

    d. Install pyowm:

        pip install pyowm

2. Make sure you have the datasets:

    a. Crime dataset:

        Export as CSV from:

            https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2

        Put in:

            ./data/crime_data_original.csv

    b. Weather dataset:

        Requires authorization from NOAA.

        Put in:

            ./data/weather_data.csv

3. Prepare the data:

        python prepare_data.py

4. Visualizations:

    a. Make sure this folder exists:

        ./static/maps

    b. Create the map visualizations:

        python viz.py

    c. Now you can access the heatmap in:

        ./static/heatmap.html

5. Crime prediction:

    a. Create the crime predictor:

        python machine_learning.py

    b. Run the server:

        python server.py

    c. Now you can access the crime predictor in:

        http://localhost:3000/predict.html

6. The index (including the PDF) is in:

        http://localhost:3000/index.html



### Acknowledgments
The City of Chicago Data Portal for publishing their data.

NOAA, for giving us access to their weather data.

The creators of Anaconda, folium, scikit, numpy, and all the other libraries we used, for producing excellent and useful libraries.
