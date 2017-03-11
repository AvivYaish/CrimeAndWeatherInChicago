"""
Names: Yuval Shavit, David Barda, Aviv Yaish
Filename: hypothesis_test.py
Description: Performs various hypotheses tests on the data.
Usage: python hypothesis_test.py
"""

from scipy.stats.distributions import chi2
from scipy.stats import chisquare

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import numpy as np

import project_commons as pc


# A delimiter for the various text prints
TEXT_DELIMITER = "========================================="

# The minimal frequency for each expected category for the chi-squared test
MINIMAL_EXPECTED_FREQUENCY = 5


def print_header(header):
    """
    Prints a header with the given text.
    :param header: the header to print.
    """
    print("\n\n" + TEXT_DELIMITER + "\n" + header + "\n" + TEXT_DELIMITER)


def pretty_graph(data, column, title, xlabel, ylabel, hue=None):
    """
    Plots a pretty graph.
    :param data: the data to visualize.
    :param column: either the column of the dataframe to visualize, or None if data is a value counts object.
    :param title: the title of the graph.
    :param xlabel: the xlabel of the graph.
    :param ylabel: the ylabel of the graph.
    :param hue: the column name for the hue.
    :return: the axes of the graph.
    """
    plt.figure()
    ax = plt.axes()

    if column is not None:
        if hue is None:
            sns.countplot(x=column, data=data)
            total = len(data)
        else:
            sns.countplot(x=column, hue=hue, data=data)
    else:
        sns.barplot(x=data.index, y=data)
        total = sum(data)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if hue is None:
        for p in ax.patches:
            x = p.get_bbox().get_points()[:, 0]
            y = p.get_bbox().get_points()[1, 1]
            ax.annotate('{:.1f}%'.format(100 * p.get_height() / total), (x.mean(), y), ha='center', va='bottom')

    plt.tight_layout()
    return ax


def hypothesis_test(observed_no_treatment_data, observed_treatment_data, treatment_name, alpha=0.05, graph=True):
    """
    Performs an hypothesis test to check if a given treatment changes distributions.
    :param observed_no_treatment_data: observed value counts for the distribution when there is no treatment.
    :param observed_treatment_data: observed value counts for the distribution when there is a treatment.
    :param treatment_name: the name of the treatment.
    :param alpha: the alpha of the test.
    """
    # We've chosen chi-squared as the hypothesis test
    print_header("Hypothesis testing for the treatment: %r\n"
                 "We will perform the chi-squared test with alpha = %r" % (treatment_name, alpha))

    no_treatment_percent = observed_no_treatment_data / sum(observed_no_treatment_data)
    expected_treatment_data = sum(observed_treatment_data) * no_treatment_percent

    # check if the expected frequencies are large enough for the chi-squared test
    can_use_chi_squared = sum(expected_treatment_data > MINIMAL_EXPECTED_FREQUENCY) == len(expected_treatment_data)
    print("Are the expected frequencies enough for the chi-squared test? %r" % can_use_chi_squared)
    if not can_use_chi_squared:
        print("Frequencies not high enough for this treatment.")
        return

    # the decision rule
    critical_value = chi2.isf(q=alpha, df=len(expected_treatment_data) - 1)
    print("The critical value is: %r" % critical_value)

    # perform the test
    chisq, p_value = chisquare(f_obs=observed_treatment_data, f_exp=expected_treatment_data)
    rejection = (chisq > critical_value) and (p_value < alpha)
    print("The chi-squared value is %r, the p-value is %r.\nShould we reject H0? %r" % (chisq, p_value, rejection))
    print("Note: H0 is the hypothesis that the treatment makes no change to the observed "
          "distribution of the untreated data.")

    # Supporting graphs and data
    if graph:
        # Value counts for patients who had no treatment
        pretty_graph(observed_no_treatment_data, None, 'Value counts, without treatment: ' + treatment_name,
                     'Readmission CHANGE THIS', 'Crime count')

        # Value counts for patients who had the treatment
        pretty_graph(observed_treatment_data, None, 'Value counts, with treatment: ' + treatment_name,
                     'Readmission CHANGE THIS', 'Crime count')

    # Various relevant values
    # Note that of course that the first two percentages should be the same
    print("Some supporting statistics:")
    print("Observed percentages without treatment:\n%r" % no_treatment_percent)
    print("Expected percentages with treatment (should be the same as above):\n%r" %
          (expected_treatment_data / sum(expected_treatment_data)))
    print("Observed percentages with treatment:\n%r" % (observed_treatment_data / sum(observed_treatment_data)))


def main():
    """
    Performs the various hypotheses tests
    """
    # Load data
    crime_data = pd.read_csv(pc.PROCESSED_CRIME_DATA)

    temperatures = crime_data['Temp'].unique()
    crime_days = crime_data['Day'].astype('category')
    crime_types = crime_data['Primary Type'].astype('category')
    crime_values = crime_types.unique()

    # for each temperature in our data, perform the following hypotheses tests
    for temperature in temperatures:
        above_temperatures = crime_data['Temp'] > temperature
        below_temperatures = np.logical_not(above_temperatures)

        # test if being above/below a certain temperature affects the distribution of crimes among days
        hypothesis_test(crime_days[above_temperatures].value_counts().sort_index(),
                        crime_days[below_temperatures].value_counts().sort_index(),
                        'temperature below ' + str(temperature) + ', for days', graph=False)

        # test if being above/below a certain temperature affects the distribution of crimes among crime types
        hypothesis_test(crime_types[above_temperatures].value_counts().sort_index(),
                        crime_types[below_temperatures].value_counts().sort_index(),
                        'temperature below ' + str(temperature) + ', for crime types', graph=False)

        # test if being above/below a certain temperature affects the distribution of a single crime type
        crime_percent_diff_dict = {}
        for cur_crime in crime_values:
            cur_crime_indices = crime_types == cur_crime
            other_crimes_indices = np.logical_not(cur_crime_indices)

            crime_types_above = crime_types[above_temperatures]
            above_data = pd.Series({cur_crime: len(crime_types_above[cur_crime_indices]),
                                    "All other crimes": len(crime_types_above[other_crimes_indices])})

            crime_types_below = crime_types[below_temperatures]
            below_data = pd.Series({cur_crime: len(crime_types_below[cur_crime_indices]),
                                    "All other crimes": len(crime_types_below[other_crimes_indices])})

            hypothesis_test(above_data, below_data,
                            'temperature below ' + str(temperature) + ', for crime type: ' + cur_crime, graph=False)

            above_percent = (above_data / sum(above_data))[cur_crime]
            below_percent = (below_data / sum(below_data))[cur_crime]
            percent_diff = np.absolute(above_percent - below_percent)
            crime_percent_diff_dict[cur_crime] = percent_diff
            print("Percentage difference for %r: %r" % (cur_crime, percent_diff))

        print_header("Crime with biggest difference for current temperature")
        max_diff_crime = max(crime_percent_diff_dict, key=crime_percent_diff_dict.get)
        print("The crime with biggest percentage difference for temperature %r is %r and the difference is %r." %
              (temperature, max_diff_crime, crime_percent_diff_dict[max_diff_crime]))

    plt.show()
    return

if __name__ == "__main__":
    main()
