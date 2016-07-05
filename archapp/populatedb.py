import re
import os
import openpyxl
from archapp.models import Site, Filter, ValueType, Property, User

def opensheet(path, name):
    wb = openpyxl.load_workbook(path)
    return wb.get_sheet_by_name(name)

# Convert DMS latlon format to DD
def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd;

def formatted(coord):
    degrees = int(coord[0:2])
    minutes = int(coord[4:6])
    seconds = float(re.search('\' (.*)"', coord).group(1))
    direction = coord[-1]
    return dms2dd(degrees, minutes, seconds, direction)

def populate_from_excel(sheet, user = 'admin'):
    user = User.objects.all().get(username = user)
    filters = Filter.objects.filter(basic = True)

    for row in sheet['A1':'C11']:
        lat = formatted(row[0].value)
        lng = formatted(row[1].value)
        name = row[2].value
        newsite = Site(name = name, user = user)
        newsite.save()

        for instance in filters:
            prop = None
            args = {'instance': instance}
            name = instance.name.lower()
            data = None 

            # populate missing fields to escape errors on editing
            if data is None:
                data = False

            if instance.oftype == ValueType.integer:
                args['integer'] = int(data)
            elif instance.oftype == ValueType.boolean:
                args['boolean'] = bool(data)
            elif instance.oftype == ValueType.double:
                args['double'] = float(data)
            elif instance.oftype == ValueType.string:
                args['string'] = data

            # fill position
            if name == "latitude":
                prop = Property.objects.create(instance = instance, double = lng)
            elif name == "longtitude":
                prop = Property.objects.create(instance = instance, double = lat)
            else:
                prop = Property.objects.create(**args)

            newsite.props.add(prop)

        newsite.data = [{'Bibliography': ""}]
        newsite.save()

    return print("Database has been populated")
