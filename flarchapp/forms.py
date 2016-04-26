# -*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, FloatField, DecimalField, SelectField, BooleanField, FileField
#from flask_wtf.file import FileField, FileAllowed
#from flask.ext.uploads import UploadSet 
from wtforms.validators import Length, Optional, NumberRange, DataRequired
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
#images = UploadSet('images', IMAGES)

class newSiteForm(Form):
    name = StringField('name', [Length(min=3,max=30)])
    toponim = StringField('toponim', [Length(min=3,max=30)])
    type_of_site = SelectField("Тип пам'ятки", choices=[("Городище", "Городище"), ("Поселення", "Послення"), ("Поховання", "Поховання")]) 
    oblast = StringField('oblast', [Length(min=3,max=50)])
    rajon = StringField('rajon', [Length(min=3,max=50)])
    krajina = StringField('rajon', [Length(min=3,max=50)])
    punkt = StringField('punkt', [Length(min=3,max=50)])
    pryvjazka = StringField('pryvjazka', [Length(min=3,max=50)])
    prymitky = StringField('prymitky')
    skiph = BooleanField('skiph')
    juhn= BooleanField('juhn')
    pjuhn = BooleanField('pjuhn')
    verok = BooleanField('verok')
    dvosh = BooleanField('dvosh')
    drz = BooleanField('drz')
    localgr = SelectField("Локальна група", choices=[("Західне посем'я", "Західне Посем'я"), ("Східне посем'я", "Східне посем'я"), ("Посулля", "Посулля"), ("Середньопсілська", "Середньопсілська"), ("Верхньопсілська", "Верхньопсілська"), ("Скіфське Подесення", "Скіфське Подесення"), ("Новгород-Сіверське Подесення", "Новгород-Сіверське Подесення"), ("Брянське Подесення", "Брянське Подесення"), ("Верхня Ока", "Верхня Ока"), ("Пізньоюхнівська", "Пізньоюхнівська"), ("Невстановлено", "Невстановлено")]) 
    chron = StringField('chron')
    nadijnist = SelectField("Датування", choices=[("Ненадійне", "Ненадійне"), ("Розвідки", "Розвідки"), ("Професійні розвідки", "Професійні розвідки"), ("Розкопки", "Розкопки")]) 
    rozkop = BooleanField('rozkop')
    dospl = IntegerField('dospl', [Optional()])
    zvit = StringField('zvit')
    publicacii = StringField('publicacii')
    kartograph = BooleanField('kartograph')
    latd = FloatField('latd')
    longt = FloatField('longt')
    tochkart = SelectField("Точність", choices=[("Точно", "Точно"), ("За прив'язкою", "За прив'язкою"), ("Гіпотетично", "Гіпотетично")]) 
    basejn = SelectField("Річки", choices=[("Сейм", "Сейм"), ("Десна", "Десна"), ("Дон", "Дон"), ("Псел", "Псел"), ("Ока", "Ока"), ("Сула", "Сула"), ("Ворскла", "Ворскла")]) 
    toppotype = SelectField("Тип", choices=[("Дюна", "Дюна"), ("Тераса", "Тераса"), ("2-га тераса", "2-га тераса"), ("Висока тераса", "Висока тераса"), ("Корінний берег", "Корінний берег")]) 
    geomorform = StringField('geomorform')
    vysotnadrm = IntegerField('vysotnadrm', [Optional()])
    ploshch = IntegerField('ploshch', [Optional()])
    dovz = IntegerField('dovz', [Optional()])
    shyr = IntegerField('shyr', [Optional()])
    foto = BooleanField('foto')
    plans = BooleanField('plans')
    znahidky = BooleanField('znahidky')
    kistka = BooleanField('kistka')
    zalizo = BooleanField('zalizo')
    kamin = BooleanField('kamin')
    glyna = BooleanField('glyna')
    photo = FileField('photo_up', [FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

