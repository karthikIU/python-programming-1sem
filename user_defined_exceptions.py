class TableNotExistException(Exception):
    """
    Exception class for handling errors related to database Table.

    This custom exception is raised when accessing database Table.
    Attributes:
        message (str): A custom error message describing the Database Error.

    """
    def __init__(self, message="Table does not exist"):
        self.message = message
        super().__init__(self.message)

class ColumnsNotExistException(Exception):
    """
    Exception class for handling errors related to database Table Columns.

    This custom exception is raised when accessing database TableColumns.
    Attributes:
        message (str): A custom error message describing 
        the Database Table Columns Error.

    """
    def __init__(self, message="Columns does not exist"):
        self.message = message
        super().__init__(self.message)