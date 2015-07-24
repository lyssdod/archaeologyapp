#import os
#import sys
#from sqlalchemy import Column, ForeignKey, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship
#from sqlalchemy import create_engine
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.whooshalchemy as whooshalchemy
#from archaeologyProject import app

#from whooshalchemy import IndexService
db = SQLAlchemy(app)
#Base = declarative_base()

class Site(db.Model):
    __tablename__ = 'site'
    __searchable__= ['name', 'toponim']

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), nullable=False)
    toponim = db.Column(String(250))
    type_of_site= db.Column(String(250), nullable=False)
    oblast = db.Column(String(250), nullable=False)
    rajon = db.Column(String(250), nullable=False)
    punkt = db.Column(String(250), nullable=False)
    prymitky = db.Column(String(3000))
    kultnal = db.Column(String(250), nullable=False)
    chron = db.Column(String(250), nullable=False)
    nadijnist = db.Column(String(250), nullable=False)
    rozkop = db.Column(String(1000), nullable=False)
    zvit = db.Column(String(1000), nullable=False)
    publicacii = db.Column(String(1500), nullable=False)
    kartograph = db.Column(String(20), nullable=False)
    coord = db.Column(String(50), nullable=False)
    tochkart = db.Column(String(20), nullable=False)
    toppoltype = db.Column(String(30), nullable=False)
    geomorform = db.Column(String(250), nullable=False)
    vysotnadrm = db.Column(String(250), nullable=False)
    ploshch = db.Column(String(50), nullable=False)
    dovz = db.Column(String(50), nullable=False)
    shyr = db.Column(String(50), nullable=False)


    @property #i might have to change this to __init__
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'name': self.name,
                'id': self.id,
                'toponim': self.toponim,
                'type_of_site': self.type_of_site,
                'oblast': self.oblast,
                'rajon': self.rajon,
                'punkt': self.punkt,
                'prymitky': self.prymitky,
                'kultnal': self.kultnal,
                'chron': self.chron,
                'nadijnist': self.nadijnist,
                'rozkop': self.rozkop,
                'zvit': self.zvit,
                'publicacii': self.publicacii,
                'kartograph': self.kartograph,
                'coord': self.coord,
                'tochkart': self.tochkart, 
                'toppoltype': self.toppoltype,
                'geomorform': self.geomorform,
                'vysotnadrm': self.vysotnadrm,
                'ploshch': self.ploshch,
                'dovz': self.dovz,
                'shyr': self.shyr
                }
    def __repr__(self):
        return '{0}(name={1})'.format(self.__class__.__name__, self.name)
    
#engine = create_engine('sqlite:///thesite.db')
#with app.app_context():
#    flask.ext.whooshalchemy.whoosh_index(app, Site)
#Base.metadata.create_all(engine)
