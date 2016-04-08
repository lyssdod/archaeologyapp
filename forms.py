# -*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, FloatField, DecimalField, SelectField, BooleanField
from wtforms.validators import Length, NumberRange, DataRequired

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
    chron = StringField('chron', [Length(min=3,max=50)])
    nadijnist = SelectField("Датування", choices=[("Ненадійне", "Ненадійне"), ("Розвідки", "Розвідки"), ("Професійні розвідки", "Професійні розвідки"), ("Розкопки", "Розкопки")]) 
    rozkop = BooleanField('rozkop')
    dospl = IntegerField('dospl', [NumberRange(min=0, max=10000)])
    zvit = StringField('zvit', [Length(min=3,max=50)])
    publicacii = StringField('publicacii', [Length(min=3,max=350)])
    kartograph = BooleanField('kartograph')
    latd = FloatField('latd')
    longt = FloatField('longt')
    tochkart = SelectField("Точність", choices=[("Точно", "Точно"), ("За прив'язкою", "За прив'язкою"), ("Гіпотетично", "Гіпотетично")]) 
    basejn = SelectField("Річки", choices=[("Сейм", "Сейм"), ("Десна", "Десна"), ("Дон", "Дон"), ("Псел", "Псел"), ("Ока", "Ока"), ("Сула", "Сула"), ("Ворскла", "Ворскла")]) 
    toppotype = SelectField("Тип", choices=[("Дюна", "Дюна"), ("Тераса", "Тераса"), ("2-га тераса", "2-га тераса"), ("Висока тераса", "Висока тераса"), ("Корінний берег", "Корінний берег")]) 
    geomorform = StringField('geomorform', [Length(min=3,max=350)])
    vysotnadrm = IntegerField('vysotnadrm', [NumberRange(min=0, max=10000)])
    ploshch = IntegerField('ploshch', [NumberRange(min=0, max=10000)])
    dovz = IntegerField('dovz', [NumberRange(min=0, max=10000)])
    shyr = IntegerField('shyr', [NumberRange(min=0, max=10000)])


