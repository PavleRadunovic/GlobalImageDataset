import inquirer
import sys
from utils import checkInputDateValidation, checkDateRangeValidation, createPoint, createGeometryFromGeoJSON, getBoundingBox, getCloudCoverage, createDateRange, checkIfSentinelTileIsValid

def exit_program():
    print("Exiting the program...")
    sys.exit(0)

'''
    TODO add description
'''
def getInputData():
    dateFrom = checkInputDateValidation('Datum od')
    dateTo = checkInputDateValidation('Datum do')
    newDateTo = checkDateRangeValidation(dateFrom, dateTo)
    if newDateTo:
        dateTo = newDateTo
    dateRange = createDateRange(dateFrom, dateTo)

    questions = [
      inquirer.List('geometryType',
                    message="Choose type of geometry?",
                    choices=['Point', 'Geojson file', 'Boundary Box', 'Tile name'],
                ),
    ]
    answers = inquirer.prompt(questions)
    inputChooice = answers["geometryType"]
    geometry = None
    tilename = None
    if inputChooice == 'Point':
        geometry = createPoint()
    elif inputChooice == 'Geojson file':
        geometry = createGeometryFromGeoJSON()
        if geometry is None:
            exit_program()
    elif inputChooice == 'Boundary Box':
        geometry = getBoundingBox()
        if geometry is None:
            exit_program()
    elif inputChooice == 'Tile name':
        tilename = checkIfSentinelTileIsValid()

    cloudCoverage = getCloudCoverage()
    
    query = None
    if cloudCoverage:
        query = {
            "eo:cloud_cover":{"lt":cloudCoverage}
        }
    
    return [dateRange, geometry, query, tilename]
