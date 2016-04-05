# -*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from flask.ext.wtf import Form
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import Length, DataRequired

class newSiteForm(Form):
    name = StringField('name', [Length(min=3,max=30)])
    toponim = StringField('toponim', [Length(min=3,max=30)])
    type_of_site = SelectField("Тип пам'ятки", choices=[("Городище", "Городище"), ("Поселення", "Послення"), ("Поховання", "Поховання")]) 
    oblast = StringField('oblast', [Length(min=3,max=50)])
    rajon = StringField('rajon', [Length(min=3,max=50)])
    krajina = StringField('rajon', [Length(min=3,max=50)])
    punkt = StringField('punkt', [Length(min=3,max=50)])
    pryvjazka = StringField('pryvjazka', [Length(min=3,max=50)])
    skiph = BooleanField('skiph')
    juhn= BooleanField('juhn')
    pjuhn = BooleanField('pjuhn')
    verok = BooleanField('verok')
    dvosh = BooleanField('dvosh')
    drz = BooleanField('drz')
    localgr = SelectField("Локальна група", choices=[("Західне посем'я", "Західне Посем'я"), ("Східне посем'я", "Східне посем'я"), ("Посулля", "Посулля"), ("Середньопсілська", "Середньопсілська"), ("Верхньопсілська", "Верхньопсілська"), ("Скіфське Подесення", "Скіфське Подесення"), ("Новгород-Сіверське Подесення", "Новгород-Сіверське Подесення"), ("Брянське Подесення", "Брянське Подесення"), ("Верхня Ока", "Верхня Ока"), ("Пізньоюхнівська", "Пізньоюхнівська"), ("Невстановлено", "Невстановлено")]) 


