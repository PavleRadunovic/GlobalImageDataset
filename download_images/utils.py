import os
from datetime import datetime, date
import fiona
import geojson
from shapely.geometry import Point

def checkInputDateValidation (title):
    while True:
        date_str = input(f"{title} yyyy-mm-dd: ")
        if date_str == '':
            break
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid yyyy-mm-dd string, '{date_str}', try again")
    return date_str

def checkDateRangeValidation(dateFrom, dateTo):
    if dateFrom and dateTo:
        if dateFrom and dateTo and datetime.strptime(dateFrom, '%Y-%m-%d') < datetime.strptime(dateTo, '%Y-%m-%d'):
            pass
        else:
            print("Invalid date range, date to can not be smaller than date from, try again!")
            dateTo = checkInputDateValidation('Date to')

def createDateRange(dateFrom, dateTo):
    if dateFrom and dateTo:
       return dateFrom + "/" + dateTo
    elif dateFrom and dateTo == '':
        return dateFrom
    elif dateFrom == '' and dateTo:
        return dateTo
    else:
        return date.today().strftime('%Y-%m-%d')


def createPoint():
    point = None
    while True:
        try:
            pointString = input("Enter the point lon,lat: ")
            point = Point(pointString.split(',')[0], pointString.split(',')[1])
            return point
        except:
            print("Bad format for point lon,lat, '{lon}/{lat}', try again!")


def createGeometryFromGeoJSON ():
    while True:
        try:
            path = input("Enter the file path: ")
            if not os.path.exists(path):
                raise
            else:
                break
        except:
            print("File don't exist, try again!")
    
    try:
        src = fiona.open(path)
        profile = src.profile
        if profile['driver'] not in ['ESRI Shapefile', 'GeoJSON']:
            raise
    except Exception as e:
        print(f"Invalid File format. {e}")
        return
    
    try:
       for feature in src:
            if not geojson.Feature(feature).is_valid or not src.validate_record_geometry(feature):
                raise
    except:
        print("Feature is not valid")
        return
    
    try:
       if profile['schema']['geometry'] not in ['Polygon', 'MultiPolygon']:
                raise
    except:
        print("Feature must be Polygon")
        return
    
    try:
        return fiona.model.to_dict(src[0]['geometry'])
    except:
        print(f"File {path} has invalid geometry or something wrong with attributes!")
        return


def getBoundingBox():
    while True:
        try:
            bboxString = input("Enter the BBOX: ")
            bboxArray = bboxString.replace(' ', '').split(',')
            if len(bboxArray) != 4:
                raise
            if all([isinstance(float(coord), float) or isinstance(float(coord), int) for coord in bboxArray]):
                pass
            else:
                raise
            minLong = bboxArray[0]
            maxLong = bboxArray[1]
            minLat = bboxArray[2]
            maxLat = bboxArray[3]
            return {
                "coordinates": [
                    [
                        [minLong, minLat],
                        [minLong, maxLat],
                        [maxLong, maxLat],
                        [maxLong, minLat],
                        [minLong, minLat]
                    ]
                ],
                "type": "Polygon",
            }
        except:
            print("Boundary box is not right!")


def getCloudCoverage ():
    while True:
        try:
            cloudString = input('Cloud coverage (0.0 - 1): ').replace(' ', '')
            if cloudString == '':
                return None
            cloudCoverage = float(cloudString)
            if 0 <= cloudCoverage <= 1:
                return cloudCoverage
            else:
                raise
        except:
            print('Bad cloud coverage!')


def checkIfSentinelTileIsValid():
    tilename = input("Enter the tile name: ")
    band = input("Enter the band name: ")
    tileParts = tilename.split('_')
    print(tileParts[2][4: 6])
    if int(tileParts[2][4: 6]) < 10:
        month = int(tileParts[2][4: 6])
    else:
        month = tileParts[2][4, 6]
    return f"https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/{tileParts[1][0:2]}/{tileParts[1][2]}/{tileParts[1][3:5]}/{tileParts[2][0:4]}/{month}/{tilename}/{band}.tif"
