from flask.ext.wtf import Form
from wtforms import StringField 
from wtforms.validators import Length, DataRequired

class newSiteForm(Form):
    name=StringField('name', [Length(min=3,max=30)])
    toponim=StringField('toponim', [Length(min=3,max=30)])

