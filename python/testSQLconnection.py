# -*- coding: utf-8 -*-
"""
Test script to connect to SQL Server Database
Philips.PatientData
"""

# Import modules
import pyodbc

# Create ODBC connection string and create a connection
# Then ask it for a cursor
myServer = 'HSTSPIICDW'
myDB = 'Philips.PatientData'
connStr = "Driver=SQL Server; Server=" + myServer + \
          "; Database=" + myDB + "; Trusted_Connection=yes;"
connX = pyodbc.connect(connStr)
cursor = connX.cursor()

# Create SQL query and retreive all rows
# Use triple quotes to easily read SQL Query
myQuery = """
    SELECT BedLabel, TimeStamp
    FROM External_BedTag
    """
cursor.execute(myQuery)
bedTagTab = cursor.fetchall()

# Data stored as Row object; similar to tuples,
# but can access columns by name
# For each row separately
print('BedLabel:', bedTagTab[0].BedLabel)
print('TimeStamp:', bedTagTab[0].TimeStamp)

# Supports query parameters via ?'s as placeholders
myQuery2 = """
    SELECT BedLabel, TimeStamp
    FROM External_BedTag
    WHERE BedLabel NOT LIKE ?
    """
cursor.execute(myQuery2, ['Biomed%'])
bedTagTab2 = cursor.fetchall()

# Close connections
connX.close()