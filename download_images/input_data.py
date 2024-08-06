import inquirer

from utils import checkInputDateValidation, checkDateRangeValidation, createPoint, createGeometryFromGeoJSON, getBoundingBox, getCloudCoverage, createDateRange, checkIfSentinelTileIsValid


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
    elif inputChooice == 'Boundary Box':
        geometry = getBoundingBox()
    elif inputChooice == 'Tile name':
        tilename = checkIfSentinelTileIsValid()

    cloudCoverage = getCloudCoverage()
    
    query = None
    if cloudCoverage:
        query = {
            "eo:cloud_cover":{"lt":cloudCoverage}
        }
    
    return [dateRange, geometry, query, tilename]
