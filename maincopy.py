import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression as lr
import statsmodels.api as sm
from database_migration import upgrade_migrations
from iu_python_db import DatabaseWithDataframeOperations
from utils import CSVToPd
from bokeh_data_visual import bokeh_train_ideal_plot, bokeh_test_mapped_ideal
from bokeh.layouts import gridplot
from bokeh.io import output_file, show

train_csv_path = "train.csv"
ideal_csv_path = "ideal.csv"
db_path = "iu_python.db"
test_csv_path = "test.csv"
train_table_name = "train_data"
ideal_table_name = "ideal_data"
test_mapping_table_name = "test_mapping"


# for convenient purpose placing all files in same/single project directory
# files are not organized for easiness

# upgrade all migrations that creates train_data, ideal_data & test_mapping tables
upgrade_migrations()


class PredictAndMapIdeal:
    def __init__(
        self,
        train_csv_path,
        ideal_csv_path,
    ):
        """
        Initialize a PredictAndMapIdeal instance.

        Args:
            train_csv_path (str): The file path to the CSV containing training
            data.
            ideal_csv_path (str): The file path to the CSV containing ideal data.

        The PredictAndMapIdeal class is used for performing predictions and
        mapping of ideal data based on the provided training data and ideal data and test
        CSV files.It allows you to load the data from CSV files and perform various
        operations for prediction and mapping.
        """
        # converting csv to df with CSVToPd class static method
        self.train_df = CSVToPd.convert(train_csv_path)
        self.ideal_df = CSVToPd.convert(ideal_csv_path)

    def setDbInstanceProperty(self, dbPath):
        """
        Initialize and set the database connection property.

        Args:
            dbPath (str): The file path to the SQLite database.

        This method creates a DatabaseWithDataframeOperations instance and sets it
        as a property of the current object. It allows you to establish a database
        connection for performing operations on DataFrames.
        """
        # initializing db_connection instance & set property
        self.db_connection = DatabaseWithDataframeOperations(dbPath)

    def insert_train_ideal(self, train_table, ideal_table):
        """
        Inserts DataFrames into the database for training and ideal data.

        This method takes two DataFrames, `train_df` and `ideal_df`, and inserts them
        into the corresponding database tables specified by `train_table_name` and
        `ideal_table_name` using the `df_to_sql` method of the `db_connection` object.

        Parameters:
        - self: The instance of the class containing this method.

        Returns:
        None
        """
        self.db_connection.df_to_sql(self.train_df, train_table)
        self.db_connection.df_to_sql(self.ideal_df, ideal_table)

    # criteria 1: predict/select 4 ideal functions out of 50 based on train data
    def predict_ideal_functions(self):
        """
        calculates selected ideal fns dataframe & largest deviation of them
        """
        try:

            # merging the ideal_df and train_df1 dataframes
            # to remove naming conflicts with ideal y1, y2, y3, y4 columns with train y1, y2, y3, y4 columns
            # added suffixes to columns in train
            train_ideal_merged_df = pd.merge(
                self.train_df, self.ideal_df, on="x", suffixes=("_train", "")
            )

            # Provide 'suffixes' as a tuple.
            # These suffixes are used to disambiguate columns with the same name in the original DataFrames train_df and ideal_df.

            # When you merge DataFrames based on a common column (in your case, "x"),
            # the common column used for the merge (i.e., "x") will not get the suffixes added

            columns_to_exclude = ["x"]
            # just column names of predicted/selected ideal functions
            selected_ideal_column_names = []
            # Create dataframes for deviations
            selected_ideal_deviations_df = pd.DataFrame()
            plots = []
            # iterating on column names y1, y2, y3, y4
            for train_col in self.train_df.columns:
                deviation_df = pd.DataFrame()
                if train_col not in columns_to_exclude:
                    # iterating on column names y1...y50 in ideal
                    for ideal_col in self.ideal_df.columns:
                        if ideal_col not in columns_to_exclude:
                            # since suffixes used only for train df columns in merged df
                            # storing with same column names y1...y50 in deviation_df
                            deviation_df[ideal_col] = (
                                train_ideal_merged_df[f"{train_col}_train"]
                                - train_ideal_merged_df[ideal_col]
                            )

                    # here used square deviation & summed & later we use absolute deviation in 2nd criteria
                    sum_values = deviation_df.apply(lambda x: (x**2).sum())

                    # since have same no of rows or length we can use sum or mean of deviations to predict ideal functions

                    lowest_sum_index = (
                        sum_values.idxmin()
                    )  # finds the index, index==coloumn name

                    # storing the lowest sum column name in selected_ideal_column_names
                    selected_ideal_column_names.append(lowest_sum_index)

                    # storing the absolute deviation of (train - ideal_ to find largest deviation for criteria 2
                    selected_ideal_deviations_df[lowest_sum_index] = deviation_df[
                        lowest_sum_index
                    ].abs()

                    # creating individual deviation plots for each train_y and selected ideal_y
                    plot = bokeh_train_ideal_plot(
                        train_ideal_merged_df["x"],
                        train_ideal_merged_df[f"{train_col}_train"],
                        train_ideal_merged_df[lowest_sum_index],
                        label_1="train_{}".format(train_col),
                        label_2="ideal_{}".format(lowest_sum_index),
                    )
                    # appending each deviation plot for each selected ideal(4 selected)
                    plots.append(plot)

            # vizualizing each deviation between selected ideal & respective train as 2 plots in a row
            grid = gridplot([plots[:2], plots[2:]])

            # Output the grid of plots to an HTML file
            output_file("selected_ideal_deviations.html")
            show(grid)

            # added selected_ideal_col_names to self for unittest to compare
            self.selected_ideal_col_names = selected_ideal_column_names
            # in selected ideal cols names added x, we need x col for further usage
            selected_ideal_column_names.insert(0, "x")
            # based on selected ideal column names fetching df
            self.selected_ideal_df = train_ideal_merged_df.loc[
                :, selected_ideal_column_names
            ]
            # calculating max/largest deviation of selected ideal  cols
            max_devs_of_selected_ideal = selected_ideal_deviations_df.max()
            # returning selected ideal function dataframe & largest deviation of selected ideal cols
            # self.selected_ideal_df=selected_ideal_df
            self.max_devs_of_selected_ideal = max_devs_of_selected_ideal
            # return selected_ideal_df , max_devs_of_selected_ideal
        except Exception as e:
            print(f"predict ideal functions Error:{e}")

    def map_ideal_to_individual_test(self, x_test, y_test):
        """
        maps ideal function to each (x,y) test data points
        returns tuple of (x,y, delta_y, mapped_ideal)
        """
        # since x_test read as string by csv.reader, convert df[x] as string with as.type(str) just for comparing
        row = self.selected_ideal_df[
            self.selected_ideal_df["x"].astype(str) == str(x_test)
        ]  # this row is df with col names and row matched
        # Exclude the 'x' column by name

        deviations = row.drop(columns="x").sub(float(y_test)).abs()
        # Find the column name with the lowest deviation
        # df.idxmin() gives the pandas series with index & value
        # to get just the value we use values method series.values[0]
        lowest_deviation_column = deviations.idxmin(axis=1).values[0]

        # df.min() gives the pandas series with index & value
        # to get just the value we use values method series.values[0] since series.values gives value in array
        lowest_deviation_value = deviations.min(axis=1).values[0]

        # tolerance=e largest deviation between training dataset (A) and
        # the ideal function (C) chosen for it by more than factor sqrt(2)
        tolerance = (
            np.sqrt(2) * self.max_devs_of_selected_ideal[lowest_deviation_column]
        )
        no_of_ideal_function = (
            lowest_deviation_column if lowest_deviation_value <= tolerance else "pass"
        )
        # storing delta_y as lowst deviation value
        delta_y = lowest_deviation_value

        # Safely access the column values by df[column_name].values
        # after getting value it wil be in array eg: [4.536] so using index[0] to access value
        mapped_ideal_value = (
            row[no_of_ideal_function].values[0]
            if no_of_ideal_function in row.columns
            else None
        )

        data_values_dict = {
            "x_test": x_test,
            "y_test": y_test,
            "delta_y": delta_y,
            "no_of_ideal_function": no_of_ideal_function,
            "mapped_ideal": mapped_ideal_value,
        }
        return data_values_dict

    # criteria 2
    # after traindata & ideal data loaded to db, now test data must be loaded line-by-line
    # dont use pd.read converts to df, instead read line by line with csv module/package
    # assuming read line by line as read & insert in to db line by line (row by row from csv)
    def map_ideal_to_all_test_and_insert(
        self, test_csv_path, test_mapping_table_name, table_col_names
    ):
        """
        Takes input table name & column names
        maps the ideal functions that satisifes criteria 2
        i.e.. lowest ideal deviation(test-ideal) must be less than
        sqrt 2 * max dev(train-ideal)
        """
        # Open the CSV file for reading line by line
        # and also inserting each row in db as per requirement (but how ever we can save all in df & insert df in table at once)
        # print(selected_ideal_df) # x, y ,y9, y18, y21, y11

        # with statement auto-closes file after operation/if exception occured
        x_test_var = []
        y_test_var = []
        mapped_ideal = []
        with open(test_csv_path, "r", newline="\n") as csv_file:
            csv_reader = csv.reader(csv_file)
            # reads CSV values as strings by default.

            # Skip the first row (header with column names)
            next(csv_reader)

            for row in csv_reader:
                # Convert values to float since read happens in string
                x_test = float(row[0])
                y_test = float(row[1])
                # data_values=self.map_ideal_to_individual_test(x_test, y_test)
                data_values_dict = self.map_ideal_to_individual_test(x_test, y_test)
                x_test_var.append(data_values_dict["x_test"])
                y_test_var.append(data_values_dict["y_test"])
                mapped_ideal.append(data_values_dict["mapped_ideal"])
                data_values_tuple = (
                    data_values_dict["x_test"],
                    data_values_dict["y_test"],
                    data_values_dict["delta_y"],
                    data_values_dict["no_of_ideal_function"].replace("y", "N"),
                )

                # inserting to db line by line, instead can insert bulk also
                # passing 2 arguments table name & data in dictionary format
                self.db_connection.insert_data(
                    test_mapping_table_name, table_col_names, data_values_tuple
                )
        bokeh_test_mapped_ideal(
            x_test_var,
            y_test_var,
            mapped_ideal,
            label_1="Test Data",
            label_2="Mapped Ideal functions",
        )


# create instance of PredictAndMapIdeal class
predictAndMapIdealInstance = PredictAndMapIdeal(train_csv_path, ideal_csv_path)

# setting the dbInstance as property to the above instance
predictAndMapIdealInstance.setDbInstanceProperty(db_path)

# inserting the train and ideal in database
predictAndMapIdealInstance.insert_train_ideal(train_table_name, ideal_table_name)

# this predict_ideal_functions predicts the ideal functions
predictAndMapIdealInstance.predict_ideal_functions()


table_col_names = (
    "X (test func)",
    "Y (test func)",
    "Delta Y (test func)",
    "No. of ideal func",
)
predictAndMapIdealInstance.map_ideal_to_all_test_and_insert(
    test_csv_path, test_mapping_table_name, table_col_names
)
