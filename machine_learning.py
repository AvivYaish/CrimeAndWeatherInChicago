"""
Names: Yuval Shavit, David Barda, Aviv Yaish
Filename: machine_learning.py
Description: Compares the various classifiers and pickles the Random Forest one.
Usage: python machine_learning.py
"""

import pandas as pd
import datetime
import project_commons
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

FEATURE_NAMES = ["Temp", "Latitude", "Longitude", "Date Day and Month"]


def get_day_of_year_by_date(date):
    """
    Get a day of the year(day from 365 days in year) by a given date.
    :param date: The date to get the day by.
    """
    return int(datetime.datetime.strptime(date, project_commons.time_pattern_crime).strftime(
        project_commons.DATE_LEARNING_FORMAT))


def get_learning_data_from_data_set(crime_data):
    """
    Creating a label encoder for the crime primary type.
    :param crime_data: The relevant fields of the dataset.
    """
    crime_data["Date Day and Month"] = crime_data["Date"].apply(get_day_of_year_by_date)
    return crime_data[["Temp", "Latitude", "Longitude", "Date Day and Month"]], crime_data["Primary Type"]


def create_label_encoder_for_crime_primary_type(primary_crime_types):
    """
    Creating a label encoder for the crime primary type.
    :param crime_data: The relevant fields of the dataset.
    """
    le = preprocessing.LabelEncoder()
    le.fit(primary_crime_types)
    return le


def print_important_features(clf, x):
    """
    Prints the feature importances for the given classifier.
    :param clf: a tree based classifier.
    :param x: the training data the classifier was fitted on.
    :param title: title for the various prints.
    """
    importances = clf.feature_importances_
    indices = pd.np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")
    for f in range(x.shape[1]):
        print("%d. feature %r (%f)" % (f + 1, FEATURE_NAMES[indices[f]], importances[indices[f]]))


def finalize_using_random_forest_classifier(X, y):
    """
    After we chose RandomForestClassifier, we train it over all the dataset,
    we print the relevance of the features(which is retrieved by the algorithm)
    and finally we store the hypothesis.
    :classifier: the classifier to train
    :param X: the training samples.
    :param y: the training labels.
    """
    classifier = RandomForestClassifier()
    classifier.fit(X, y)
    print_important_features(classifier, X)

    joblib.dump(classifier, project_commons.CLASSIFIER_PKL, 3)


if __name__ == "__main__":
    crime_data = pd.read_csv(project_commons.PROCESSED_CRIME_DATA)

    # Create primary crime type label encoder, encode and store in a pickle for later usage.
    primary_type_label_encoder = create_label_encoder_for_crime_primary_type(crime_data["Primary Type"])
    crime_data["Primary Type"] = primary_type_label_encoder.transform(crime_data["Primary Type"])
    joblib.dump(primary_type_label_encoder, project_commons.PRIMARY_TYPE_LABEL_ENCODER_PKL, 9)

    # Test multiple learners, we finally chose Random forest classifier as it gave the best prediction.
    X, y = get_learning_data_from_data_set(crime_data)
    training_X, test_X, training_Y, test_Y = train_test_split(X, y, test_size=0.30)

    print("---Starting to test learners---")
    learners = {"DecisionTreeClassifier": DecisionTreeClassifier(),
                "BernoulliNB": BernoulliNB(), "GaussianNB": GaussianNB(),
                "RandomForest": RandomForestClassifier()}
    for name, learner in learners.items():
        print("---Learning using " + name + "---")
        learner.fit(training_X, training_Y)
        result = pd.np.mean(learner.predict(test_X) == test_Y)
        print("Score: " + str(result))

    finalize_using_random_forest_classifier(X, y)


