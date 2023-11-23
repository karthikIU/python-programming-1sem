import pandas as pd
import os

# using pandas library to convert csv to dataframe
class CSVToPd:
    @staticmethod
    def convert(csv_path):
        """
            Takes csv file path as input
            returns dataframe of that csv file

        """
        try:
            csv_path = os.path.join(csv_path)
            return pd.read_csv(csv_path)
        except Exception as e:
                print(f"Error converting to dataframe: {e}")