import re
import os
import openpyxl
from django.conf import settings
from archapp.geo import GeoCoder
from django.utils import translation
from archapp.models import Site, Filter, ValueType, Property, User

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

def populate_from_excel(path, user = 'admin'):
    wb = openpyxl.load_workbook(path)
    geo = GeoCoder(GeoCoder.Type.google)
    user = User.objects.all().get(username = user)
    sheet = wb.active
    filters = Filter.objects.filter(basic = True)

    for row in sheet.rows:
        lat = formatted(row[0].value)
        lng = formatted(row[1].value)
        name = row[2].value
        newsite = Site(name = name, user = user)
        newsite.save()

        print ("adding '{}'".format(name))

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

            # search for string values first
            if instance.oftype == ValueType.string:
                # let's remember missing translations...
                missing = []

                # we want these values to be explicitly translated
                if name in geo.filters():
                    for lang, etc in settings.LANGUAGES:
                        # try to get geo data in specified language
                        with translation.override(lang):
                            geocoded = geo.reverse(lat, lng, lang, name)
                            geocoded = geocoded or translation.ugettext('Unknown') # maybe try another provider here?

                        # let's search for it
                        try:
                            prop = Property.objects.language(lang).get(instance = instance, string = geocoded)
                        except Property.DoesNotExist:
                            missing.append( (lang, geocoded) )
                else:
                    # for plain string properties just copy provided text to all translations
                    missing = [(code, args['string']) for code, full in settings.LANGUAGES]

                # if no translations available, create property without translation
                if prop is None:
                    prop = Property.objects.create(instance = instance)
                    prop.save(update_fields = ['instance'])

                # finally fill missing translations
                for lang, translated in missing:
                    prop.translate(lang)
                    prop.string = translated

                    try:
                        prop.save()
                    except:
                        pass
            else:
                # fill position
                if name == "latitude":
                    prop = Property.objects.create(instance = instance, double = lat)
                elif name == "longtitude":
                    prop = Property.objects.create(instance = instance, double = lng)
                else:
                    prop = Property.objects.create(**args)

            newsite.props.add(prop)

        newsite.data = [{'Bibliography': ""}]
        newsite.save()

