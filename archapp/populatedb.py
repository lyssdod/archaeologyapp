import re
import os
import openpyxl
from .models import Site, Filter, ValueType, Property, User

#Populate db with value from excel
cwd = os.getcwd()
wb = openpyxl.load_workbook(cwd + '/archapp/' + '465.xlsx')
sheet = wb.get_sheet_by_name('465')
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
    dd = dms2dd(degrees, minutes, seconds, direction)
    return dd 

def Populate_from_xlsx(sheet):
    user = User.objects.all().get(username='populatedb')
    filters = Filter.objects.filter(basic = True)

    for row in sheet['A1':'C11']:
        lat = row[0].value
        lat = formatted(lat)
        longt = row[1].value
        longt = formatted(longt)
        name = row[2].value
        newsite = Site(name=name, user = user)
        newsite.save()

        for instance in filters:
            prop = None
            args = {'instance': instance}
            name = instance.name.lower()
            data = None 
            # populate missing fields to escape errors on editting
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

            prop = Property.objects.create(**args)
            # add lat and lon props to the site
            if name == "latitude":
                prop = Property.objects.create(instance=instance, double=longt)
            if name == "longtitude":
                prop = Property.objects.create(instance=instance, double=lat)
            newsite.props.add(prop)

        newsite.data = [{'Bibliography': ""}]
        newsite.save()

    return print("Database has been populated")
