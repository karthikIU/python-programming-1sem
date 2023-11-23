# execute this file to run unit test or use command : 
# python -m unittest iu_python_unittest.py

from unittest import TestCase, main
import pandas as pd
from main import PredictAndMapIdeal

class Test(TestCase):
    def setUp(self):
        """
        Set up a test instance of PredictAndMapIdeal with sample CSV files.

        This method initializes a test instance of the PredictAndMapIdeal class
        using sample CSV files for testing purposes. It is called before each
        individual test method.

        """
        self.test_instance = PredictAndMapIdeal("train.csv", "ideal.csv")

    def test_predict_ideal_functions(self):
        """
        Test the predict_ideal_functions method.

        This method tests the predict_ideal_functions method of the
        PredictAndMapIdeal class. shows predicted y columns from ideal

        """
        self.test_instance.predict_ideal_functions()
        # x column is wanteldy inserted for refering with 
        # row wise x, y copule values
        self.assertEqual(self.test_instance.selected_ideal_col_names,
                          ['x', 'y42', 'y41', 'y11', 'y48'])

    def test_predictAndMapIdealInstance(self):
        """
        Test the map_ideal_to_individual_test method.

        This method tests the map_ideal_to_individual_test method of the
        PredictAndMapIdeal class. It checks if the method correctly maps
        ideal to  test data points and returns the expected results in tuple.

        """
        self.test_instance.predict_ideal_functions()
        self.assertAlmostEqual(
            self.test_instance.map_ideal_to_individual_test(17.5, 34.16104), 
            (17.5, 34.16104, 0.351148000000002, 'N41'))
        self.assertAlmostEqual(
            self.test_instance.map_ideal_to_individual_test(0.3, 1.2151024), 
            (0.3, 1.2151024, 0.4673422999999999, 'N41'))
        self.assertAlmostEqual(
            self.test_instance.map_ideal_to_individual_test(0.8, 1.4264555), 
            (0.8, 1.4264555, 0.5322224999999998, 'N41'))
        self.assertAlmostEqual(
            self.test_instance.map_ideal_to_individual_test(-15.0, -0.20536347), 
            (-15.0, -0.20536347, 0.45237137, 'N48'))
if __name__ == '__main__':
    main()

