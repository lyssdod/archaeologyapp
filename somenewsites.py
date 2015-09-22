from myapp import db
from models import Site

#db.create_all()
hey = Site('name', 'toponim')
db.session.add(hey)
db.session.commit()

