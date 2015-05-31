import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Site(Base):
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    toponim = Column(String(250))
    type_of_site= Column(String(250), nullable=False)
    oblast = Column(String(250), nullable=False)
    rajon = Column(String(250), nullable=False)
    punkt = Column(String(250), nullable=False)
    prymitky = Column(String(3000))
    kultnal = Column(String(250), nullable=False)
    chron = Column(String(250), nullable=False)
    nadijnist = Column(String(250), nullable=False)
    rozkop = Column(String(1000), nullable=False)
    zvit = Column(String(1000), nullable=False)
    publicacii = Column(String(1500), nullable=False)
    kartograph = Column(String(20), nullable=False)
    coord = Column(String(50), nullable=False)
    tochkart = Column(String(20), nullable=False)
    toppoltype = Column(String(30), nullable=False)
    geomorform = Column(String(250), nullable=False)
    vysotnadrm = Column(String(250), nullable=False)
    ploshch = Column(String(50), nullable=False)
    dovz = Column(String(50), nullable=False)
    shyr = Column(String(50), nullable=False)

    
    @property
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

engine = create_engine('sqlite:///thesite.db')

Base.metadata.create_all(engine)
