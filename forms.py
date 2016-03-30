# -*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from flask.ext.wtf import Form
from wtforms import StringField, SelectField 
from wtforms.validators import Length, DataRequired

class newSiteForm(Form):
    name=StringField('name', [Length(min=3,max=30)])
    toponim=StringField('toponim', [Length(min=3,max=30)])
    type_of_site= SelectField("Тип пам'ятки", choices=[("Городище", "Городище"), ("Поселення", "Послення"), ("Поховання", "Поховання")]) 
    oblast=StringField('oblast', [Length(min=3,max=50)])
    rajon=StringField('rajon', [Length(min=3,max=50)])

