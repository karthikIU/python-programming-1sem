from bokeh.plotting import figure, output_file, show
from bokeh.layouts import  gridplot
from bokeh.models import  ColumnDataSource
import pandas as pd



def bokeh_train_ideal_plot(variable_x, variable_y1, variable_y2, label_1, label_2):
        """
        Create a Bokeh plot displaying the deviation of one variable from another.

        Parameters:
        variable_x (list): X-axis data values.
        variable_y1 (list): Y1-axis data values.
        variable_y2 (list): Y2-axis data values.
        label_1 (str): Label for the first variable (y1).
        label_2 (str): Label for the second variable (y2).

        Returns:
        figure: A Bokeh figure object displaying the deviation plot.
        """

        data = {
        'x': variable_x,
        'y1': variable_y1,
        'y2': variable_y2,
        }
        
        # Create a ColumnDataSource using the data dictionary
        source = ColumnDataSource(data)
        # Create a Bokeh figure
        p = figure(title=f"Deviation of {label_2} from {label_1}",
            x_axis_label='x', y_axis_label='y')

        # Create a patch glyph for y1 
        p.patch(x='x', y='y1', source=source, fill_color='red', 
                line_color='red', fill_alpha=0.5, legend_label=label_1)

        # Create a patch glyph for y2 
        p.patch(x='x', y='y2', source=source, fill_color='blue', 
                line_color='blue', fill_alpha=0.5, legend_label=label_2)

        return p

def bokeh_test_mapped_ideal(x_test, y_test, mapped_ideal, label_1, label_2):
        """
        Create a Bokeh plot displaying the comparison between test data, 
        mapped ideal data.

        Parameters:
        x_test (list): X-axis data values for the test data.
        y_test (list): Y-axis data values for the test data.
        mapped_ideal (list): Y-axis data values for the mapped ideal data.

        Returns:
        None
        Generates and displays an HTML file containing 
        the 2 Bokeh plots represents same data.
        1.scatter & line of test data, scatter of mapped ideal
        2.scatter of test data, scatter of mapped ideal
        """
        data = {
        'x': x_test,
        'y1': y_test,
        'y2': mapped_ideal,
        }

        df = pd.DataFrame(data)

        # Sort the DataFrame in ascending order based on the 'x' column
        df_sorted = df.sort_values(by='x')

        # Create a Bokeh figure with scatter & line of test data 
        # & scatter of mapped ideal
        p = figure(title=f"{label_2} deviations from {label_1} (line & scatter)",
                x_axis_label='x', y_axis_label='y')

        # Create a ColumnDataSource using the sorted DataFrame
        source = ColumnDataSource(df_sorted)

        # Add a line glyph for 'y1'
        p.line('x', 'y1', source=source, color="green")

        # use only scatter for y2 because some values are 
        # not mapped in mapping ideal

        # Add a scatter glyph for 'y1'
        p.scatter('x', 'y1', source=source, color="green", 
                  marker="circle", legend_label=label_1)


        p.scatter('x', 'y2', source=source, color="red", 
                  marker="circle", legend_label=label_2)
        # Display the legend
        p.legend.click_policy = "hide"  
        # Click on the legend to hide/show corresponding plots

        


        # 2nd plot with scatter of test data & scatter of mapped ideal 
        # for clear understanding
        p2 = figure(title=f"{label_2} deviations from {label_1} (only scatter)",
                x_axis_label='x', y_axis_label='y')
        # Add a line glyph for 'y2'

        # Add a scatter glyph for 'y1'
        p2.scatter('x', 'y1', source=source, color="green", 
                   marker="circle", legend_label=label_1)

        # Add a scatter glyph for 'y1'
        p2.scatter('x', 'y2', source=source, color="red", 
                   marker="circle", legend_label=label_2)

        # Display the legend
        p2.legend.click_policy = "hide"  
        # Click on the legend to hide/show corresponding plots


        # vizualizing each deviation between selected ideal & 
        # respective train  2 in a row
        grid = gridplot([[p,p2]])

        # Output the grid of plots to an HTML file
        output_file("mapped_ideal_deviations.html")
        show(grid)

