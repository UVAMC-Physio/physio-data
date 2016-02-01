# -*- coding: utf-8 -*-
"""
dbio.py

Functions to handle connection to SQL Server, reading a query
into python, and writing the query to another database

Created on Mon Jan 25 15:32:59 2016

@author: kss5x
"""

# Import modules
import pyodbc
import numpy
from astropy.io import ascii
import os

# Connect to SQL Server database, execute query, and return
# the results as a numpy recarray
def getquery(query, inputs = []):
    
    # Create ODBC connection string and create a connection
    # Then ask it for a cursor
    myServer = "HSTSPIICDW"
    myDB = "Philips.PatientData"
    connStr = "Driver=SQL Server; Server=" + myServer + \
              "; Database=" + myDB + "; Trusted_Connection=yes;"
    connX = pyodbc.connect(connStr)
    cursor = connX.cursor()
    
    # Execute query and close connection
    cursor.execute(query, inputs)
    queryResults = cursor.fetchall()
    connX.close()
    
    # Get column names, and create a numpy recarray
    colDesc = queryResults[0].cursor_description
    colNames = [row[0] for row in colDesc]
    queryResults = numpy.rec.fromrecords(queryResults, names=colNames)
    
    # Return results
    return(queryResults)

# Export numpy array or recarray to file
# Currently supports only csv
def exportarray(array, file="exported_data.csv"):
    
    # Write csv file
    ascii.write(array, file, format='csv')
    
    # Return true if successful
    return(os.path.isfile(file))