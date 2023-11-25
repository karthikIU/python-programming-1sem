# python-programming-1sem
programming with python 1st assignment

To start/run this project execute this command:
1.activate virtual env: zPython_env\scripts\activate
2.Run main file: python main.py

used virtual environment zPython_env directory

1.Packages used:
Alembic, bokeh, matplotlib, numpy, pandas, sqlalchemy, sys (module inbuilt in python), unittest, 
Sklearn.
2.These migrations files or code to be placed in versions folder in alembic direction, these migration files are generated with alembic command, then you need to paste code above in each file respec-tively.
3.Created function to make run migration in “database_migration.py” file, this function will be called from “main.py”.
4.Due to these migrations, tables gets created.
5.command to create/generation database schema migration:
alembic revision --autogenerate -m "file name"
6.Access sqlite database table & check data with sqlite commands:
a. Go to directory that has database.
b. In terminal/cmd prompt : sqlite3 database.db
(you should have installed sqlite3 command line tool in your pc)
c. Command to view tables: .tables
d. Use queris to view data in table like SELECT * FROM test_mapping

1. Description of the task:
We have (A) 4 training datasets and (B) one test dataset, as well as (C) datasets for 50 ideal functions. 
All data respectively consists of x-y-pairs of values.

Python-program that uses training data to choose the four ideal functions 
which are the best fit out of the fifty provided (C) *.
i) Afterwards, the program uses the test data provided (B) to determine for each and 
every x-ypair of values whether or not they can be assigned to the four chosen ideal 
functions**; if so, the program also needs to execute the mapping and save it together with 
the deviation at hand 
ii) All data  visualized logically 
iii)created/ compiled suitable unit-test

 * The criterion for choosing the ideal functions for the training function is how they minimize the 
sum of all ydeviations squared (Least-Square) 
** The criterion for mapping the individual test case to the four ideal functions is that the existing 
maximum deviation of the calculated regression does not exceed the largest deviation between 
training dataset (A) and the ideal function (C) chosen for it by more than factor sqrt(2) 

2. Details
You are given four training datasets in the form of csv-files.This Python program is able to 
independently compile a SQLite database (file) ideally via sqlalchemy and load the training data into 
a single fivecolumn spreadsheet / table in the file. Its first column depicts the x-values of all 
functions. Table 1, at the end of this subsection, shows you which structure your table is expected to 
have. The fifty ideal functions, which are also provided via a CSV-file, loaded into another 
table. Likewise, the first column depicts the x-values, meaning there will be 51 columns overall. 
Table 2, at end of this subsection, schematically describes what structure is expected. 
After the training data and the ideal functions have been loaded into the database, the test data (B) 
must be loaded line-by-line from another CSV-file and – if it complies with the compiling criterion – 
matched to one of the four functions chosen under i (subsection above). Afterwards, the results  saved into another fourcolumn-table in the SQLite database. In accordance with table 3 
X Y
X1 Y1
… …
Xn Yn
at end of this subsection, this table contains four columns with x- and y-values as well as the 
corresponding chosen ideal function and the related deviation. 
Finally, the training data, the test data, the chosen ideal functions as well as the corresponding / 
assigned datasets are visualized under an appropriately chosen representation of the deviation.
Please create a Python-program which also fulfills the following criteria: −
✓ Its design is sensibly object-oriented 
✓ It includes at least one inheritance 
✓ It includes standard- und user-defined exception handlings –
✓ For logical reasons, it makes use of Pandas’ packages as well as data visualization via Bokeh, 
sqlalchemy, as well as others 
✓ Write unit-tests for all useful elements 
✓ Your code needs to be documented in its entirety and also include Documentation Strings, 
known as ”docstrings”.


Note:
used alembic migrations to make database schema migrations
