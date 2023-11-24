
from sqlalchemy import create_engine, inspect, text
import sys
from sqlalchemy.exc import SQLAlchemyError
from user_defined_exceptions import TableNotExistException, ColumnsNotExistException



# In Python, class names should follow CapWords or PascalCase.
class DatabaseHandler:
    # this class initializes db connection
    def __init__(self, db_path):
        """
        A class for initializing and managing database connections.

        Args:
            db_path (str): The file path to the SQLite database.

        This class initializes a database connection using SQLAlchemy and provides
        methods for inserting data into tables.
        """
        try:
            engine_url = f"sqlite:///{db_path}"
            self.db_engine = create_engine(engine_url)
        except Exception as e:
            print(f"DatabaseHandler initializing Error: {e}")
            sys.exit(1)
    # insert data from dictionary object using table name(no need table object)
    def insert_data(self, table_name, column_names, data):
        """
        Insert data into a table.
        Args:
            table_name (str): The name of the table in which data needs to add.
            column_names (str): A string containing the column names in 
                                parentheses.
            data (tuple): A tuple containing the values to be inserted.

        This method inserts data into the specified table using SQLAlchemy.
        """
        # Create a schema inspector
        inspector = inspect(self.db_engine)

        # Check whether the specified table exists in the database
        if table_name not in inspector.get_table_names():
            raise TableNotExistException
            (f"Table '{table_name}' does not exist in the database")
        
        # Get the columns of the specified table
        table_columns = inspector.get_columns(table_name)
        column_names_set = set(column['name'] for column in table_columns)
        # converting inserting column names to set to check whether 
        # they are in table columns or not with issubset function
        # we can raise user defined exception if failed
        specified_columns = set(each_col.strip(" ") for each_col in column_names)
        if not specified_columns.issubset(column_names_set):
                missing_columns = specified_columns - column_names_set
                raise ColumnsNotExistException(
                    f"Columns {', '.join(missing_columns)} do not exist in the table")

        try:
            # Create an INSERT statement using the columns and placeholders
            insert_sql = text(
                f"INSERT INTO {table_name} {column_names} VALUES {data}")

            # Establish a connection
            connection =  self.db_engine.connect()
            # Execute the INSERT statement
            connection.execute(insert_sql)
            connection.commit()
        # sqlalchemyError to catch & handle errors on database
        except SQLAlchemyError as e:
            print(f"Error inserting data: {e}")

        finally:
            # Always close the connection, even in case of an exception
            connection.close()
# using class inheritance here
class DatabaseWithDataframeOperations(DatabaseHandler):
    """
    A subclass of DatabaseHandler for working with Pandas DataFrames and databases.

    This class inherits from DatabaseHandler and provides a method for inserting
    Pandas DataFrames into database tables.
    """
     # Insert pandas DataFrame using just table_name(no need table object)
    def df_to_sql(self, df, table_name):
        """
        Insert a Pandas DataFrame into a database table.
        Args:
            df (pandas.DataFrame): The DataFrame to be inserted.
            table_name (str): The name of the table in which data needs to add.

        This method inserts a Pandas DataFrame into the specified table
        """
        # Create a schema inspector
        inspector = inspect(self.db_engine)

        # Check whether the specified table exists in the database
        if table_name not in inspector.get_table_names():
            raise TableNotExistException(
                f"Table '{table_name}' does not exist in the database")
        try:
            df.to_sql(table_name, con=self.db_engine,
                      if_exists='replace', index=False)
        except Exception as e:
            print(f"insterting dataframe to sql table Error: {e}")
            sys.exit(1)


# write commands to check sqlite table data