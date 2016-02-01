# -*- coding: utf-8 -*-
"""
Test script to connect to SQL Server Database
Philips.PatientData, pull out waveform data,
and decode it
"""

# Inputs to SQL Query
patientId = '01e97c88-9241-435d-bdaa-2ae0bacd2230'
startDateTime = '2016-01-28 00:00:00.000 -05:00'
endDateTime = '2016-01-29 00:00:00.000 -05:00'
label = 'aVR'
myInputs = [patientId, label, startDateTime, endDateTime]

# Create SQL query and retreive all rows
# Use triple quotes to easily read SQL Query
myQuery = """
SELECT ews.SequenceNumber, ews.TimeStamp, 
       CONVERT(varchar(max), ews.WaveSamples, 1) AS WaveSamples,
       ews.UnavailableSamples, ews.InvalidSamples, ews.PacedPulses, 
	 ew.SamplePeriod, ew.IsSlowWave, ew.IsDerived, 
	 ew.LowEdgeFrequency, ew.HighEdgeFrequency, ew.ScaleLower, ew.ScaleUpper,
	 ew.CalibrationScaledLower, ew.CalibrationScaledUpper,
	 ew.CalibrationAbsLower, ew.CalibrationAbsUpper, 
	 CASE WHEN ew.CalibrationType = 0 THEN 'Bar' ELSE
	   CASE WHEN ew.CalibrationType = 1 THEN 'Stair' ELSE 'Unknown' END END AS CalibrationType, 
	 ew.UnitLabel, 
	 CASE WHEN ew.EcgLeadPlacement = 0 THEN 'Standard' ELSE 
	   CASE WHEN ew.EcgLeadPlacement = 1 THEN 'EASI' ELSE
	     CASE WHEN ew.EcgLeadPlacement = 2 THEN 'Hexad' ELSE 'Not ECG' END END END AS EcgLeadPlacement
FROM External_WaveSample ews
LEFT JOIN External_Wave ew
ON ews.WaveId = ew.Id
WHERE ews.PatientId = ?
  AND ew.Label = ?
  AND ews.TimeStamp >= ?
  AND ews.TimeStamp < ?
ORDER BY ews.SequenceNumber, ews.TimeStamp
    """
    
# Run query and retrieve data (numpy recarray)
import dbio
waveData = dbio.getquery(myQuery, myInputs)

# Export to csv file
isWritten = dbio.exportarray(waveData, file="waveData.csv")

# Function to decode a single row of encoded waveforms
def decodewaves(x):
    
    import numpy    
    
    waveLength = len(x)
    wavePrefix = x[0:2]
    byteSize = 4
    nSamp = int((waveLength - 2)/byteSize)    
    
    startNum = list(range(2, waveLength-byteSize+1, byteSize))
    stopNum = list(range((startNum[0] + byteSize-1), (startNum[-1] + byteSize), byteSize))
    
    values = numpy.zeros(nSamp, dtype=numpy.int)
    for i in range(nSamp):
        bytei = list(x)[startNum[i]:stopNum[i]+1]
        bytei = bytei[2:4] + bytei[0:2]
        values[i] = int(wavePrefix + ''.join(bytei),0)
        
    return(values)
    
# Function to grab a single column from output SQL query
# and return numpy array
def grabcolumn(x, colname):
    
    import numpy
    
    nRow = len(x)
    nCol = len(x[0])

    colList = []
    for j in range(nCol): colList.append(x[0].cursor_description[j][0])
    colInd = colList.index(colname)
    
    xCol = []
    for i in range(nRow): xCol.append(x[i][colInd])
        